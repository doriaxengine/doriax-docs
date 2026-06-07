# Doriax Engine Documentation

Official documentation for the [Doriax game engine](https://github.com/doriaxengine/doriax),
built with [MkDocs](https://www.mkdocs.org/) and a **custom theme** designed to match the
[Doriax website](https://doriax.org).

## Custom theme

This project does **not** use the MkDocs Material theme. Instead it ships a fully custom
theme under [`theme/`](theme/) that reuses the design language of the Doriax website
(colors, typography, gradients, and components):

- `theme/main.html` — page layout (header, sidebar, content, table of contents)
- `theme/partials/` — header, sidebar, TOC, and footer navigation
- `theme/css/doriax.css` — the complete theme stylesheet
- `theme/css/highlight.css` — Pygments syntax highlighting tuned to the Doriax palette
- `theme/js/doriax.js` — sidebar, collapsible nav, code copy buttons, scrollspy, and search

Documentation content lives in [`docs/`](docs/).

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
