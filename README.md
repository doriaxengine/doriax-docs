# Doriax Engine Documentation

Official documentation for the [Doriax game engine](https://github.com/doriaxengine/doriax),
built with [MkDocs](https://www.mkdocs.org/).

Documentation content lives in [`docs/`](docs/). The site is organized into:

- `getting-started/` — orientation, installation, and first project pages
- `tutorials/` — step-by-step workflows
- `editor/` — editor panels, project workflow, resources, animation, code, and export
- `manual/` — engine concepts and subsystem guides
- `reference/` — API reference, enumerations, and build options
- `contributing/` — documentation and screenshot contribution notes

## Local development

Install the dependencies (MkDocs + PyMdown Extensions):

```bash
pip install -r requirements.txt
```

Serve the site locally with live reload:

```bash
mkdocs serve
```

Then open <http://127.0.0.1:8000>.

## Building

Produce a static site in the `site/` directory:

```bash
mkdocs build --strict
```

## License

Documentation content is licensed under
[CC&nbsp;BY&nbsp;4.0](https://creativecommons.org/licenses/by/4.0/).
