# Contributing

We'd love for you to get involved in developing this repository!

## Setup Workflow

| Command | Description |
| --- | --- |
| `python3 -m venv venv` | Create a virtual environment |
| `source venv/bin/activate` | Activate the virtual environment |
| `pip install -r requirements.txt` | Install dependencies |
| `python main.py` | Run the tool |

No automated test suite or linter is configured yet.

## Schema Workflow

- `main.py` is the entry point that starts the program.
- `spammer/` is the package holding the core logic: console styling, user-facing prompts, and the request-dispatching flow.
- `spammer/data/` holds the third-party service definitions, one JSON file per channel type.

## Contribution Workflow

Contributions go through pull requests opened against `main`. Commit messages follow Conventional Commits.
