{% include_relative jquery-3.3.1.slim.min.js %}
{% include_relative bootstrap.min.js %}
{% include_relative lazyload.min.js %}
{% include_relative google-analytics.js %}
{% include_relative gtag.js %}
{% include_relative gtag.myconfig.js %}
{% include_relative katex.min.js %}

lazyload();

(function() {
    renderMathInElement(document.body, 
        {
            'delimiters': [ 
                { left: '$$',   right: '$$',    display: true }, 
                { left: '\\[',   right: '\\]',    display: true }, 
                { left: '$',    right: '$',     display: false },
            ],
        });
})();