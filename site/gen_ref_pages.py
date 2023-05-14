"""Generate the code reference pages and navigation."""

import os
from itertools import chain
from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

for path in sorted(
    chain.from_iterable(
        Path("src").rglob(pattern) for pattern in ["*.py", "*.md"]
    )
):
    module_path = path.relative_to(".").with_suffix("")
    doc_path = path.relative_to("src").with_suffix(".md")
    nav_path = path.relative_to("src").with_suffix("")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)
    nav_parts = tuple(nav_path.parts)
    print(os.path.splitext(path)[-1])

    if parts[-1] == "__init__" or (
        parts[-1] == "index" and os.path.splitext(path)[-1] == ".md"
    ):
        parts = parts[:-1]
        nav_parts = nav_parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    nav[nav_parts] = doc_path.as_posix()

    if os.path.splitext(path)[-1] == ".md":
        with open(path, "r") as f:
            index = f.read()

        with mkdocs_gen_files.open(full_doc_path, "w") as fd:
            fd.write(index)
    else:
        with mkdocs_gen_files.open(full_doc_path, "w") as fd:
            ident = ".".join(parts)
            fd.write(f"::: {ident}")

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
