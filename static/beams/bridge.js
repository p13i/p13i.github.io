(function () {
            "use strict";

            var doc = document;
            var docElement = doc.documentElement;
            var body = doc.body;
            var canvas = document.getElementById(
              "raytracer-canvas"
            );
            var gameShell = document.getElementById(
              "raytracer-game-shell"
            );
            var fullscreenButton = document.getElementById(
              "raytracer-fullscreen"
            );
            var resetButton = document.getElementById(
              "raytracer-reset"
            );
            if (
              !canvas ||
              !gameShell ||
              !fullscreenButton
            ) {
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
              drawEchogram(parsed.arrivals);
              syncUrlFromState();
            }

            var SOURCE_CSS_COLORS = [
              "#ffd05d",
              "#78f0ee",
              "#ff71ab"
            ];
            var ECHOGRAM_WINDOW_MS = 100;

            function drawEchogram(arrivals) {
              var echogram = document.getElementById(
                "raytracer-echogram"
              );
              if (!echogram || !echogram.getContext) {
                return;
              }
              var ctx = echogram.getContext("2d");
              if (!ctx) {
                return;
              }
              var w = echogram.width;
              var h = echogram.height;
              var baseline = h - 18;
              ctx.fillStyle = "#000000";
              ctx.fillRect(0, 0, w, h);
              ctx.strokeStyle = "#333333";
              ctx.fillStyle = "#888888";
              ctx.font = "11px monospace";
              ctx.lineWidth = 1;
              for (
                var ms = 0;
                ms <= ECHOGRAM_WINDOW_MS;
                ms += 10
              ) {
                var x =
                  (ms / ECHOGRAM_WINDOW_MS) * (w - 30) + 15;
                ctx.beginPath();
                ctx.moveTo(x, 8);
                ctx.lineTo(x, baseline);
                ctx.stroke();
                ctx.fillText(String(ms), x - 8, h - 5);
              }
              ctx.fillText("ms", w - 14, h - 5);
              ctx.strokeStyle = "#555555";
              ctx.beginPath();
              ctx.moveTo(15, baseline);
              ctx.lineTo(w - 15, baseline);
              ctx.stroke();
              for (var i = 0; i < arrivals.length; i++) {
                var arrival = arrivals[i];
                var ax =
                  ((arrival.d || 0) / ECHOGRAM_WINDOW_MS) *
                    (w - 30) +
                  15;
                if (ax > w - 15) {
                  continue;
                }
                var top =
                  baseline - arrival.g * (baseline - 12);
                ctx.strokeStyle =
                  SOURCE_CSS_COLORS[arrival.s] || "#ffffff";
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(ax, baseline);
                ctx.lineTo(ax, top);
                ctx.stroke();
                ctx.fillStyle =
                  SOURCE_CSS_COLORS[arrival.s] || "#ffffff";
                ctx.fillRect(ax - 2, top - 2, 4, 4);
              }
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
              if (ly >= 0) {
                applyLayerButtonClasses(ly);
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
              applyLayerButtonClasses(state.ly);
              reflectBeamformingOnLobeButton(state.bf);
            }

            var LAYER_BUTTON_BITS = [
              ["raytracer-toggle-rays", 1],
              ["raytracer-toggle-beams", 2],
              ["raytracer-toggle-paths", 4],
              ["raytracer-toggle-lobe", 8]
            ];

            function applyLayerButtonClasses(mask) {
              if (typeof mask !== "number" || mask < 0) {
                return;
              }
              for (
                var i = 0;
                i < LAYER_BUTTON_BITS.length;
                i++
              ) {
                var toggle = document.getElementById(
                  LAYER_BUTTON_BITS[i][0]
                );
                if (!toggle) {
                  continue;
                }
                toggle.classList.toggle(
                  "active",
                  (mask & LAYER_BUTTON_BITS[i][1]) !== 0
                );
              }
            }

            function reflectBeamformingOnLobeButton(bf) {
              var toggle = document.getElementById(
                "raytracer-toggle-lobe"
              );
              if (!toggle) {
                return;
              }
              toggle.classList.toggle("disabled", bf === 0);
            }

            var bridgeWaitTimer = window.setInterval(
              function () {
                if (applyStateFromUrl()) {
                  window.clearInterval(bridgeWaitTimer);
                }
              },
              200
            );

            function bindLayerButton(buttonId, layerName) {
              var toggle =
                document.getElementById(buttonId);
              if (!toggle) {
                return;
              }
              toggle.addEventListener("click", function () {
                if (!runtimeReady()) {
                  return;
                }
                window.Module.ccall(
                  "RaytracerToggleLayer",
                  null,
                  ["string"],
                  [layerName]
                );
                toggle.classList.toggle("active");
                focusCanvas();
              });
            }
            bindLayerButton(
              "raytracer-toggle-rays",
              "rays"
            );
            bindLayerButton(
              "raytracer-toggle-beams",
              "beams"
            );
            bindLayerButton(
              "raytracer-toggle-paths",
              "paths"
            );
            bindLayerButton(
              "raytracer-toggle-lobe",
              "lobe"
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

            function dispatchReset() {
              if (!hasBridge()) {
                return;
              }
              ensureAudioStarted();
              window.Module.ccall(
                "RaytracerOnKeyDown",
                null,
                ["string"],
                ["r"]
              );
              focusCanvas();
            }

            function currentFullscreenElement() {
              if (document.fullscreenElement) {
                return document.fullscreenElement;
              }
              if (document.webkitFullscreenElement) {
                return document.webkitFullscreenElement;
              }
              if (document.mozFullScreenElement) {
                return document.mozFullScreenElement;
              }
              if (document.msFullscreenElement) {
                return document.msFullscreenElement;
              }
              return null;
            }

            function shellIsFullscreen() {
              return (
                currentFullscreenElement() === gameShell
              );
            }

            function shellHasFallbackFullscreen() {
              return gameShell.classList.contains(
                "raytracer-game-immersive"
              );
            }

            function setScrollLock(active) {
              if (!docElement || !body) {
                return;
              }
              if (active) {
                docElement.classList.add(
                  "raytracer-game-scroll-lock"
                );
                body.classList.add(
                  "raytracer-game-scroll-lock"
                );
                return;
              }
              docElement.classList.remove(
                "raytracer-game-scroll-lock"
              );
              body.classList.remove(
                "raytracer-game-scroll-lock"
              );
            }

            function syncFullscreenButton() {
              var label = "Fullscreen";
              if (
                shellIsFullscreen() ||
                shellHasFallbackFullscreen()
              ) {
                label = "Exit Fullscreen";
              }
              fullscreenButton.textContent = label;
            }

            function enterFallbackFullscreen() {
              gameShell.classList.add(
                "raytracer-game-immersive"
              );
              setScrollLock(true);
              syncFullscreenButton();
            }

            function exitFallbackFullscreen() {
              gameShell.classList.remove(
                "raytracer-game-immersive"
              );
              if (!shellIsFullscreen()) {
                setScrollLock(false);
              }
              syncFullscreenButton();
            }

            function requestShellFullscreen() {
              if (gameShell.requestFullscreen) {
                return gameShell.requestFullscreen.bind(
                  gameShell
                );
              }
              if (gameShell.webkitRequestFullscreen) {
                return gameShell.webkitRequestFullscreen.bind(
                  gameShell
                );
              }
              if (gameShell.mozRequestFullScreen) {
                return gameShell.mozRequestFullScreen.bind(
                  gameShell
                );
              }
              if (gameShell.msRequestFullscreen) {
                return gameShell.msRequestFullscreen.bind(
                  gameShell
                );
              }
              return null;
            }

            function exitDocumentFullscreen() {
              if (document.exitFullscreen) {
                return document.exitFullscreen.bind(
                  document
                );
              }
              if (document.webkitExitFullscreen) {
                return document.webkitExitFullscreen.bind(
                  document
                );
              }
              if (document.mozCancelFullScreen) {
                return document.mozCancelFullScreen.bind(
                  document
                );
              }
              if (document.msExitFullscreen) {
                return document.msExitFullscreen.bind(
                  document
                );
              }
              return null;
            }

            function enterFullscreenMode() {
              var requestFullscreen =
                requestShellFullscreen();
              if (!requestFullscreen) {
                enterFallbackFullscreen();
                return;
              }

              var requestResult = null;
              try {
                requestResult = requestFullscreen();
              } catch (err) {
                enterFallbackFullscreen();
                return;
              }

              if (
                requestResult &&
                typeof requestResult.then === "function"
              ) {
                requestResult
                  .then(function () {
                    syncFullscreenButton();
                  })
                  .catch(function () {
                    enterFallbackFullscreen();
                  });
                return;
              }

              window.setTimeout(function () {
                if (!shellIsFullscreen()) {
                  enterFallbackFullscreen();
                  return;
                }
                syncFullscreenButton();
              }, 0);
            }

            function exitFullscreenMode() {
              var exitFullscreen = exitDocumentFullscreen();
              if (shellHasFallbackFullscreen()) {
                exitFallbackFullscreen();
                return;
              }
              if (!shellIsFullscreen() || !exitFullscreen) {
                syncFullscreenButton();
                return;
              }

              var exitResult = null;
              try {
                exitResult = exitFullscreen();
              } catch (err) {
                syncFullscreenButton();
                return;
              }

              if (
                exitResult &&
                typeof exitResult.then === "function"
              ) {
                exitResult
                  .then(function () {
                    syncFullscreenButton();
                  })
                  .catch(function () {
                    syncFullscreenButton();
                  });
                return;
              }

              window.setTimeout(function () {
                syncFullscreenButton();
              }, 0);
            }

            function toggleFullscreen() {
              if (
                shellIsFullscreen() ||
                shellHasFallbackFullscreen()
              ) {
                exitFullscreenMode();
                return;
              }
              enterFullscreenMode();
            }

            function handleFullscreenStateChange() {
              if (
                shellIsFullscreen() &&
                shellHasFallbackFullscreen()
              ) {
                gameShell.classList.remove(
                  "raytracer-game-immersive"
                );
                setScrollLock(false);
              }
              if (
                !shellIsFullscreen() &&
                !shellHasFallbackFullscreen()
              ) {
                setScrollLock(false);
              }
              syncFullscreenButton();
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
            fullscreenButton.addEventListener(
              "click",
              toggleFullscreen
            );
            document.addEventListener(
              "fullscreenchange",
              handleFullscreenStateChange
            );
            document.addEventListener(
              "webkitfullscreenchange",
              handleFullscreenStateChange
            );
            document.addEventListener(
              "mozfullscreenchange",
              handleFullscreenStateChange
            );
            document.addEventListener(
              "MSFullscreenChange",
              handleFullscreenStateChange
            );
            if (resetButton) {
              resetButton.addEventListener(
                "click",
                dispatchReset
              );
            }

            syncFullscreenButton();
            window.Module = { canvas: canvas };
          })();
