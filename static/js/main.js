lazyload();

(function () {
  function renderMermaidBlocks() {
    if (!window.mermaid) {
      return;
    }

    var codeBlocks = document.querySelectorAll(
      "pre > code.language-mermaid, pre > code.mermaid, .language-mermaid pre code"
    );

    Array.prototype.forEach.call(
      codeBlocks,
      function (codeBlock) {
        var wrapper = codeBlock.closest(
          ".language-mermaid"
        );
        var pre = codeBlock.closest("pre");
        var replaceTarget = wrapper || pre;

        if (
          !replaceTarget ||
          replaceTarget.classList.contains("mermaid")
        ) {
          return;
        }

        var diagram = document.createElement("div");
        diagram.className = "mermaid";
        diagram.textContent = codeBlock.textContent.trim();
        replaceTarget.parentNode.replaceChild(
          diagram,
          replaceTarget
        );
      }
    );

    var diagrams = document.querySelectorAll(".mermaid");

    if (!diagrams.length) {
      return;
    }

    window.mermaid.initialize({
      startOnLoad: false,
      flowchart: {
        useMaxWidth: false
      },
      theme: "default"
    });
    window.mermaid.run({ nodes: diagrams });
  }

  if (document.body.dataset.katex !== "false") {
    renderMathInElement(document.body, {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "\\[", right: "\\]", display: true },
        { left: "$", right: "$", display: false }
      ]
    });
  }

  renderMermaidBlocks();
})();
