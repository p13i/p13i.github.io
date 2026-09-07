(function () {
            "use strict";

            var canvas = document.getElementById(
              "raytracer-canvas"
            );
            if (!canvas) {
              return;
            }

            var CANVAS_WIDTH = 800;
            var CANVAS_HEIGHT = 800;
            var TOUCH_MOUSE_SUPPRESSION_MS = 700;
            var draggingPointer = false;
            var lastTouchAtMs = 0;

            function focusCanvas() {
              if (typeof canvas.focus !== "function") {
                return;
              }
              try {
                canvas.focus({ preventScroll: true });
                return;
              } catch (err) {}
              canvas.focus();
            }

            function hasBridge() {
              if (!window.Module) {
                return false;
              }
              if (!window.Module.ccall) {
                return false;
              }
              return true;
            }

            function runtimeReady() {
              // Module.ccall exists before the wasm exports are
              // bound; calledRun flips only after instantiation, so
              // a throw past this gate really means a missing
              // export rather than a not-yet-ready runtime.
              return (
                hasBridge() &&
                window.Module.calledRun === true
              );
            }

            var audioContext = null;
            var sourceBanks = [];
            var arrivalPollTimer = null;
            var SOURCE_TONES_HZ = [
              261.626, 329.628, 391.995
            ];
            var SLOTS_PER_SOURCE = 4;
            var SOURCE_MIX_GAIN = 0.22;
            var ARRIVAL_POLL_MS = 120;
            var ARRIVAL_RAMP_SECONDS = 0.06;

            function startSourceTones() {
              if (audioContext) {
                if (audioContext.state === "suspended") {
                  audioContext.resume();
                }
                return;
              }
              var AudioContextCtor =
                window.AudioContext ||
                window.webkitAudioContext;
              if (!AudioContextCtor) {
                return;
              }
              // Each scene sound source plays one note of a C major
              // chord (C4, E4, G4) as a Web Audio oscillator, so all
              // synthesis runs on the browser's audio thread and can
              // never stutter when the WASM main thread is busy. Each
              // source feeds a bank of arrival slots: one gain and
              // stereo pan per acoustic path reported by the module.
              // Slots start silent; each tone fades in only once the
              // module reports a connecting acoustic path for it.
              audioContext = new AudioContextCtor();
              for (
                var s = 0;
                s < SOURCE_TONES_HZ.length;
                s++
              ) {
                var oscillator =
                  audioContext.createOscillator();
                oscillator.type = "sine";
                oscillator.frequency.value =
                  SOURCE_TONES_HZ[s];
                var sourceMix = audioContext.createGain();
                sourceMix.gain.value = SOURCE_MIX_GAIN;
                oscillator.connect(sourceMix);
                oscillator.start();
                var slots = [];
                for (var k = 0; k < SLOTS_PER_SOURCE; k++) {
                  var slotGain = audioContext.createGain();
                  slotGain.gain.value = 0.0;
                  var slotDelay =
                    audioContext.createDelay(0.5);
                  slotGain.connect(slotDelay);
                  var slotOut = slotDelay;
                  var slotPan = null;
                  if (audioContext.createStereoPanner) {
                    slotPan =
                      audioContext.createStereoPanner();
                    slotDelay.connect(slotPan);
                    slotOut = slotPan;
                  }
                  slotOut.connect(audioContext.destination);
                  sourceMix.connect(slotGain);
                  slots.push({
                    gain: slotGain,
                    delay: slotDelay,
                    pan: slotPan
                  });
                }
                sourceBanks.push(slots);
              }
              if (audioContext.state === "suspended") {
                audioContext.resume();
              }
              startArrivalPolling();
            }

            function applyArrivals(arrivals) {
              if (!audioContext) {
                return;
              }
              var perSource = [];
              for (var s = 0; s < sourceBanks.length; s++) {
                perSource.push([]);
              }
              for (var i = 0; i < arrivals.length; i++) {
                var arrival = arrivals[i];
                var index = arrival.s | 0;
                if (
                  index < 0 ||
                  index >= perSource.length
                ) {
                  continue;
                }
                perSource[index].push(arrival);
              }
              var now = audioContext.currentTime;
              for (var b = 0; b < sourceBanks.length; b++) {
                var slots = sourceBanks[b];
                for (var k = 0; k < slots.length; k++) {
                  var slot = slots[k];
                  var gainValue = 0.0;
                  var panValue = 0.0;
                  var delaySeconds = 0.0;
                  if (k < perSource[b].length) {
                    gainValue = perSource[b][k].g;
                    panValue = perSource[b][k].p;
                    delaySeconds =
                      (perSource[b][k].d || 0) / 1000;
                  }
                  slot.gain.gain.setTargetAtTime(
                    gainValue,
                    now,
                    ARRIVAL_RAMP_SECONDS
                  );
                  slot.delay.delayTime.setTargetAtTime(
                    delaySeconds,
                    now,
                    ARRIVAL_RAMP_SECONDS
                  );
                  if (slot.pan) {
                    slot.pan.pan.setTargetAtTime(
                      panValue,
                      now,
                      ARRIVAL_RAMP_SECONDS
                    );
                  }
                }
              }
            }

            function pollArrivals() {
              if (!audioContext || !runtimeReady()) {
                return;
              }
              var json = "";
              try {
                json = window.Module.ccall(
                  "RaytracerAudioArrivalsJson",
                  "string",
                  [],
                  []
                );
              } catch (err) {
                // The loaded module predates the arrivals export.
                // Open slot zero of every bank so the chord is heard
                // unshaped, then stop polling.
                var now = audioContext.currentTime;
                for (
                  var b = 0;
                  b < sourceBanks.length;
                  b++
                ) {
                  sourceBanks[
                    b
                  ][0].gain.gain.setTargetAtTime(
                    1.0,
                    now,
                    ARRIVAL_RAMP_SECONDS
                  );
                }
                stopArrivalPolling();
                return;
              }
              var parsed = null;
              try {
                parsed = JSON.parse(json);
              } catch (err) {
                return;
              }
              if (!parsed || !parsed.arrivals) {
                return;
              }
              applyArrivals(parsed.arrivals);
              syncUrlFromState();
            }

            function startArrivalPolling() {
              if (arrivalPollTimer !== null) {
                return;
              }
              arrivalPollTimer = window.setInterval(
                pollArrivals,
                ARRIVAL_POLL_MS
              );
            }

            function stopArrivalPolling() {
              if (arrivalPollTimer === null) {
                return;
              }
              window.clearInterval(arrivalPollTimer);
              arrivalPollTimer = null;
            }

            var urlStateTimer = null;
            var lastPushedState = "";

            var urlStateApplied = false;

            function finiteOr(value, fallback) {
              if (isFinite(value)) {
                return value;
              }
              return fallback;
            }

            function applyStateFromUrl() {
              if (!runtimeReady()) {
                return false;
              }
              var params = new URLSearchParams(
                window.location.search
              );
              if (
                !params.has("scene") &&
                !params.has("px")
              ) {
                urlStateApplied = true;
                return true;
              }
              // The URL parameter is one-based to match the
              // on-canvas scene label; the module is zero-based.
              // Every numeric parameter is validated here and
              // clamped again inside the module.
              var scene = finiteOr(
                parseInt(params.get("scene") || "1", 10) -
                  1,
                0
              );
              var px = finiteOr(
                parseFloat(params.get("px") || "0"),
                0
              );
              var py = finiteOr(
                parseFloat(params.get("py") || "0"),
                0
              );
              var ax = finiteOr(
                parseFloat(params.get("ax") || "0"),
                0
              );
              var ay = finiteOr(
                parseFloat(params.get("ay") || "220"),
                220
              );
              var bf = finiteOr(
                parseInt(params.get("bf") || "1", 10),
                1
              );
              var ly = finiteOr(
                parseInt(params.get("ly") || "-1", 10),
                -1
              );
              try {
                window.Module.ccall(
                  "RaytracerApplyState",
                  null,
                  [
                    "number",
                    "number",
                    "number",
                    "number",
                    "number",
                    "number",
                    "number"
                  ],
                  [scene, px, py, ax, ay, bf, ly]
                );
              } catch (err) {
                return false;
              }
              urlStateApplied = true;
              return true;
            }

            function syncUrlFromState() {
              if (
                !urlStateApplied ||
                !runtimeReady() ||
                !window.history ||
                !window.history.replaceState
              ) {
                return;
              }
              var json = "";
              try {
                json = window.Module.ccall(
                  "RaytracerStateJson",
                  "string",
                  [],
                  []
                );
              } catch (err) {
                return;
              }
              if (json === lastPushedState) {
                return;
              }
              lastPushedState = json;
              var state = null;
              try {
                state = JSON.parse(json);
              } catch (err) {
                return;
              }
              var params = new URLSearchParams();
              params.set("scene", state.scene + 1);
              params.set("px", state.px);
              params.set("py", state.py);
              params.set("ax", state.ax);
              params.set("ay", state.ay);
              params.set("bf", state.bf);
              params.set("ly", state.ly);
              window.history.replaceState(
                null,
                "",
                window.location.pathname +
                  "?" +
                  params.toString()
              );
            }

            var bridgeWaitTimer = window.setInterval(
              function () {
                if (applyStateFromUrl()) {
                  window.clearInterval(bridgeWaitTimer);
                }
              },
              200
            );

            function ensureAudioStarted() {
              startSourceTones();
              if (!hasBridge()) {
                return false;
              }
              window.Module.ccall(
                "RaytracerEnsureAudioStarted",
                null,
                [],
                []
              );
              return true;
            }

            function getPrimaryEventSource(event) {
              if (
                event.touches &&
                event.touches.length > 0
              ) {
                return event.touches[0];
              }
              if (
                event.changedTouches &&
                event.changedTouches.length > 0
              ) {
                return event.changedTouches[0];
              }
              return event;
            }

            function pointerToCanvas(event) {
              var source = getPrimaryEventSource(event);
              if (!source) {
                return null;
              }

              var clientX = source.clientX;
              var clientY = source.clientY;
              if (
                typeof clientX !== "number" ||
                typeof clientY !== "number"
              ) {
                return null;
              }

              var rect = canvas.getBoundingClientRect();
              if (rect.width <= 0 || rect.height <= 0) {
                return null;
              }

              var x =
                (clientX - rect.left) *
                (CANVAS_WIDTH / rect.width);
              var y =
                (clientY - rect.top) *
                (CANVAS_HEIGHT / rect.height);
              return {
                x: Math.max(
                  0,
                  Math.min(CANVAS_WIDTH - 1, Math.floor(x))
                ),
                y: Math.max(
                  0,
                  Math.min(CANVAS_HEIGHT - 1, Math.floor(y))
                )
              };
            }

            function dispatchPointerDown(event) {
              if (!hasBridge()) {
                return;
              }

              var point = pointerToCanvas(event);
              if (!point) {
                return;
              }

              ensureAudioStarted();
              draggingPointer = true;
              window.Module.ccall(
                "RaytracerOnMouseDown",
                null,
                ["number", "number", "number"],
                [point.x, point.y, 0]
              );
              focusCanvas();
              event.preventDefault();
            }

            function dispatchPointerMove(event) {
              if (!draggingPointer || !hasBridge()) {
                return;
              }

              var point = pointerToCanvas(event);
              if (!point) {
                return;
              }

              window.Module.ccall(
                "RaytracerOnMouseMove",
                null,
                ["number", "number"],
                [point.x, point.y]
              );
              event.preventDefault();
            }

            function dispatchPointerUp(event) {
              draggingPointer = false;
              if (!hasBridge()) {
                return;
              }
              window.Module.ccall(
                "RaytracerOnMouseUp",
                null,
                [],
                []
              );
              if (event) {
                event.preventDefault();
              }
            }

            function dispatchTouchStart(event) {
              lastTouchAtMs = Date.now();
              dispatchPointerDown(event);
            }

            function dispatchMouseDown(event) {
              if (
                Date.now() - lastTouchAtMs <
                TOUCH_MOUSE_SUPPRESSION_MS
              ) {
                event.preventDefault();
                return;
              }
              dispatchPointerDown(event);
            }

            function dispatchMouseMove(event) {
              if (
                Date.now() - lastTouchAtMs <
                TOUCH_MOUSE_SUPPRESSION_MS
              ) {
                return;
              }
              dispatchPointerMove(event);
            }

            function dispatchKeyDown(event) {
              if (!hasBridge()) {
                return;
              }

              var key = event.key;
              if (
                key !== "ArrowLeft" &&
                key !== "ArrowRight" &&
                key !== "ArrowUp" &&
                key !== "ArrowDown" &&
                key !== "r" &&
                key !== "R" &&
                key !== "b" &&
                key !== "B" &&
                key !== "1" &&
                key !== "2" &&
                key !== "3" &&
                key !== "4" &&
                key !== "5" &&
                key !== "6" &&
                key !== "7" &&
                key !== "8" &&
                key !== "9"
              ) {
                return;
              }

              ensureAudioStarted();
              window.Module.ccall(
                "RaytracerOnKeyDown",
                null,
                ["string"],
                [key]
              );
              event.preventDefault();
            }

            if (window.PointerEvent) {
              canvas.addEventListener(
                "pointerdown",
                dispatchPointerDown,
                { passive: false }
              );
              window.addEventListener(
                "pointermove",
                dispatchPointerMove,
                { passive: false }
              );
              window.addEventListener(
                "pointerup",
                dispatchPointerUp,
                { passive: false }
              );
              window.addEventListener(
                "pointercancel",
                dispatchPointerUp,
                { passive: false }
              );
            } else {
              canvas.addEventListener(
                "touchstart",
                dispatchTouchStart,
                { passive: false }
              );
              window.addEventListener(
                "touchmove",
                dispatchPointerMove,
                { passive: false }
              );
              window.addEventListener(
                "touchend",
                dispatchPointerUp,
                { passive: false }
              );
              window.addEventListener(
                "mousedown",
                dispatchMouseDown
              );
              window.addEventListener(
                "mousemove",
                dispatchMouseMove
              );
              window.addEventListener(
                "mouseup",
                dispatchPointerUp
              );
            }
            canvas.addEventListener("click", focusCanvas);
            window.addEventListener(
              "keydown",
              dispatchKeyDown
            );
            window.Module = { canvas: canvas };
          })();
