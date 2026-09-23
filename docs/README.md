# PAMPAS Docs

This directory is dedicated to the wiki documentation of the project. Below you'll find instructions on how to locally build the wiki. It's important to always check how your contribution works in the MkDocs format before sending a PR.

## Requirements

- Python
- MkDocs and the Material style pluging for it

To locally build the documentation, at the project's root directory run:

```bash
$ mkdocs serve
```

It's easier with uv:

```bash
$ uv run --no-project mkdocs serve
```

This is gonna open the documentation website in `127.0.0.1:8000` (or in a similar port if that is being used).
