from html.parser import HTMLParser
import sys

class HTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.self_closing = {
            'meta', 'link', 'img', 'br', 'hr', 'input', 'area', 'base', 'col', 'embed', 'param', 'source', 'track', 'wbr'
        }
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() not in self.self_closing:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in self.self_closing:
            return
        if not self.stack:
            self.errors.append(f"Unexpected closing tag </{tag}> at line {self.getpos()[0]}")
            return
        last_tag, pos = self.stack.pop()
        if last_tag != tag:
            self.errors.append(f"Mismatched tag: expected </{last_tag}> (from line {pos[0]}), found </{tag}> at line {self.getpos()[0]}")

with open('templates/index.html', encoding='utf-8') as f:
    html_content = f.read()

validator = HTMLValidator()
validator.feed(html_content)

if validator.stack:
    for tag, pos in validator.stack:
        validator.errors.append(f"Unclosed tag <{tag}> from line {pos[0]}")

if validator.errors:
    print(f"Found {len(validator.errors)} HTML structural issues:")
    for err in validator.errors[:10]:
        print(f" - {err}")
else:
    print("SUCCESS: 100% of HTML tags in index.html are valid and properly balanced!")
