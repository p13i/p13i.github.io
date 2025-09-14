from typing import List
import requests
from io import BytesIO
from PIL import Image
import html
import math


def MakeWebTiles(image_urls: List[str]) -> str:
    """
    Downloads the images (in-memory), reads their dimensions, and returns an HTML string
    containing a justified tiled gallery with constant spacing = 42px.
    The HTML contains a server-side computed layout for a default container width,
    plus client-side JS that recalculates layout responsively on the browser.
    """
    SPACING = 42  # px, constant spacing requested
    DEFAULT_CONTAINER_PX = 1200  # used to compute a server-side fallback layout
    TARGET_ROW_HEIGHT = 250  # ideal row height (px) used by the packing algorithm
    MIN_ROW_HEIGHT = 120
    MAX_ROW_HEIGHT = 400

    # --- Download images and gather intrinsic sizes ---
    images = []
    for url in image_urls:
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            img = Image.open(BytesIO(resp.content))
            w, h = img.size
            if w <= 0 or h <= 0:
                continue
            images.append(
                {"url": url, "w": int(w), "h": int(h), "ratio": float(w) / float(h)}
            )
        except Exception:
            # skip broken/unreachable images silently
            continue

    # If no valid images, return a minimal HTML page
    if not images:
        return (
            "<!doctype html>\n"
            "<html><head><meta charset='utf-8'><title>No images</title></head>"
            "<body><p>No valid images were provided.</p></body></html>"
        )

    # --- Server-side row packing (fallback rendering) ---
    def pack_rows(imgs, container_width):
        """Greedy packing: accumulate images until they fill a row at TARGET_ROW_HEIGHT."""
        rows = []
        row = []
        sum_ratio = 0.0
        for im in imgs:
            row.append(im)
            sum_ratio += im["ratio"]
            total_spacing = SPACING * (len(row) - 1)
            expected_width = sum_ratio * TARGET_ROW_HEIGHT + total_spacing
            # If we've reached or exceeded container width, finalize this row
            if expected_width >= container_width:
                row_height = (container_width - total_spacing) / sum_ratio
                row_height = max(MIN_ROW_HEIGHT, min(MAX_ROW_HEIGHT, row_height))
                rows.append((row, row_height))
                row = []
                sum_ratio = 0.0
        # Last row: show at TARGET_ROW_HEIGHT or scaled down to avoid overflow
        if row:
            total_spacing = SPACING * (len(row) - 1)
            if sum_ratio > 0:
                last_height = min(
                    TARGET_ROW_HEIGHT,
                    max(MIN_ROW_HEIGHT, (container_width - total_spacing) / sum_ratio),
                )
            else:
                last_height = TARGET_ROW_HEIGHT
            rows.append((row, last_height))
        return rows

    rows = pack_rows(images, DEFAULT_CONTAINER_PX)

    # --- Build HTML ---
    # CSS: container is responsive (max-width at DEFAULT_CONTAINER_PX), spacing enforced via gaps
    css = f"""
    :root {{ --jg-spacing: {SPACING}px; --jg-max-width: {DEFAULT_CONTAINER_PX}px; }}
    html,body{{height:100%;margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,"Helvetica Neue",Arial;}}
    .jg-wrap{{max-width:var(--jg-max-width);margin:20px auto;padding:12px;box-sizing:border-box;}}
    .jg-row{{display:flex;gap:var(--jg-spacing);margin-bottom:var(--jg-spacing);align-items:stretch;}}
    .jg-row:last-child{{margin-bottom:0;}}
    .jg-row img{{display:block;object-fit:cover;--intrinsic-w:auto;--intrinsic-h:auto;}}
    /* make images non-selectable while dragging */
    .jg-row img {{ user-select: none; -webkit-user-drag: none; }}
    """

    # Build server-side rows markup (fallback if JS disabled) using computed widths/heights
    rows_html_parts = []
    for row_imgs, row_h in rows:
        rows_html_parts.append('<div class="jg-row">')
        for im in row_imgs:
            scaled_w = max(1, int(round(im["ratio"] * row_h)))
            scaled_h = max(1, int(round(row_h)))
            safe_url = html.escape(im["url"], quote=True)
            alt = html.escape(safe_url.split("/")[-1] or "image", quote=True)
            # Also include data attributes for client-side layout (data-w, data-h)
            rows_html_parts.append(
                f'<img src="{safe_url}" '
                f'width="{scaled_w}" height="{scaled_h}" '
                f'data-w="{im["w"]}" data-h="{im["h"]}" alt="{alt}" loading="lazy" />'
            )
        rows_html_parts.append("</div>")

    rows_html = "\n".join(rows_html_parts)

    # --- Client-side JS: recompute layout responsively using intrinsic sizes ---
    # It removes server-side rows and rebuilds rows using the actual container width.
    js = f"""
    (function() {{
      const SPACING = {SPACING};
      const TARGET_ROW_HEIGHT = {TARGET_ROW_HEIGHT};
      const MIN_ROW_HEIGHT = {MIN_ROW_HEIGHT};
      const MAX_ROW_HEIGHT = {MAX_ROW_HEIGHT};

      function gatherImgs(container) {{
        // collect all imgs with data-w,data-h in document order
        const imgs = Array.from(container.querySelectorAll('img[data-w][data-h]'));
        return imgs.map(img => {{
          return {{
            el: img,
            iw: parseInt(img.getAttribute('data-w'), 10),
            ih: parseInt(img.getAttribute('data-h'), 10),
            ratio: parseInt(img.getAttribute('data-w'), 10) / parseInt(img.getAttribute('data-h'), 10)
          }};
        }});
      }}

      function packRowsForWidth(imgs, containerWidth) {{
        const rows = [];
        let row = [];
        let sumRatio = 0;
        for (const im of imgs) {{
          row.push(im);
          sumRatio += im.ratio;
          const totalSpacing = SPACING * (row.length - 1);
          const expectedWidth = sumRatio * TARGET_ROW_HEIGHT + totalSpacing;
          if (expectedWidth >= containerWidth) {{
            let rowH = (containerWidth - totalSpacing) / sumRatio;
            rowH = Math.max(MIN_ROW_HEIGHT, Math.min(MAX_ROW_HEIGHT, rowH));
            rows.push({{ row: row.slice(), height: rowH }});
            row = [];
            sumRatio = 0;
          }}
        }}
        if (row.length) {{
          const totalSpacing = SPACING * (row.length - 1);
          const rowH = Math.min(TARGET_ROW_HEIGHT, Math.max(MIN_ROW_HEIGHT,
                      sumRatio > 0 ? (containerWidth - totalSpacing) / sumRatio : TARGET_ROW_HEIGHT));
          rows.push({{ row: row.slice(), height: rowH }});
        }}
        return rows;
      }}

      function clearChildren(el) {{
        while (el.firstChild) el.removeChild(el.firstChild);
      }}

      function relayout() {{
        const container = document.getElementById('justified-gallery-container');
        if (!container) return;
        // pull all imgs (they are initially inside server-side rows)
        const imgs = gatherImgs(container);
        if (!imgs.length) return;
        const containerWidth = Math.max(200, container.clientWidth); // avoid degenerate widths
        const rows = packRowsForWidth(imgs, containerWidth);

        // build new DOM
        clearChildren(container);
        for (let i = 0; i < rows.length; ++i) {{
          const r = rows[i];
          const rowDiv = document.createElement('div');
          rowDiv.className = 'jg-row';
          rowDiv.style.display = 'flex';
          rowDiv.style.gap = SPACING + 'px';
          rowDiv.style.marginBottom = SPACING + 'px';
          for (let j = 0; j < r.row.length; ++j) {{
            const im = r.row[j];
            const w = Math.max(1, Math.round(im.ratio * r.height));
            const h = Math.max(1, Math.round(r.height));
            // re-use existing img element (preserves src, lazy status)
            const imgEl = im.el;
            imgEl.style.width = w + 'px';
            imgEl.style.height = h + 'px';
            imgEl.setAttribute('width', String(w));
            imgEl.setAttribute('height', String(h));
            rowDiv.appendChild(imgEl);
          }}
          container.appendChild(rowDiv);
        }}
      }}

      // debounce helper
      function debounce(fn, wait) {{
        let t = null;
        return function() {{
          const args = arguments;
          clearTimeout(t);
          t = setTimeout(() => fn.apply(null, args), wait);
        }};
      }}

      // Run after DOM ready and on resize
      document.addEventListener('DOMContentLoaded', relayout);
      window.addEventListener('resize', debounce(relayout, 120));
      // also run just in case images are cached
      window.addEventListener('load', relayout);
    }})();    
    """

    # Full HTML assembly
    html_out = [
        "  <style>",
        css,
        "  </style>",
        "  <div class='jg-wrap'>",
        "    <!-- Server-side fallback rows (JS will reflow into responsive layout at runtime) -->",
        "    <div id='justified-gallery-container'>",
        rows_html,
        "    </div>",
        "  </div>",
        "  <script>",
        js,
        "  </script>",
    ]

    return "\n".join(html_out)


import re
from typing import List


def ExtractImageUrlsFromYaml(filename: str) -> List[str]:
    """
    Extract all image URLs from a YAML file using regex, without any dependencies.
    Specifically looks for lines with 'url:' followed by a string.

    Args:
        filename: Path to the YAML file.

    Returns:
        A list of URLs (strings).
    """
    urls: List[str] = []
    url_pattern = re.compile(
        r'^\s*-\s*url:\s*(["\']?)(https?://[^\s#]+)\1', re.IGNORECASE
    )

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            match = url_pattern.search(line)
            if match:
                urls.append(match.group(2))

    return urls


# Example usage:
# html_string = MakeWebTiles([
#     "https://example.com/photo1.jpg",
#     "https://example.com/photo2.jpg",
#     ...
# ])
# with open("gallery.html","w",encoding="utf8") as f:
#     f.write(html_string)

if __name__ == "__main__":
    # Example usage
    example_urls = ExtractImageUrlsFromYaml("_data/pix.yaml")
    html_output = MakeWebTiles(example_urls)
    path = "_includes/_gallery.html"
    with open("_includes/_gallery.html", "w", encoding="utf8") as f:
        f.write(html_output)
    print(f"HTML gallery generated: {path}")

# python scripts/make_web_tiles.py
# python3 -m http.server --bind 127.0.0.1 8080
