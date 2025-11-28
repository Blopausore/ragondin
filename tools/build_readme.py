import re

template = open("README.template.md").read()
snippets = {
    "intro": open("docs/introduction.md").read(),
    "install": open("docs/installation.md").read(),
    "quickstart": open("docs/quickstart.md").read(),
}

for key, content in snippets.items():
    template = template.replace(f"<!-- {key} -->", content)

open("README.md", "w").write(template)
print("README.md generated!")
