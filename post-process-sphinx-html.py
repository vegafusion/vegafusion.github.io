from pathlib import Path
import sys
import re

if __name__ == "__main__":
    base = Path(sys.argv[1])

    # Replace the title of the index.html page
    index_html = base / "index.html"
    index_html_text = index_html.read_text("utf-8")

    # Regular expression to match the contents of the title tag
    title_regex = re.compile(r'(<title>).*?(</title>)', re.DOTALL)

    # Replace the contents of the title tag
    new_title = 'VegaFusion'
    index_html_text = title_regex.sub(r'\g<1>' + new_title + r'\g<2>', index_html_text)
    index_html.write_text(index_html_text)
