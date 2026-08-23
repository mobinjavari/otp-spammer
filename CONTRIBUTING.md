# Contributing

We'd love for you to get involved in developing this repository!

## Setup Workflow

Clone the repository, create a virtual environment, and install the dependencies:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the tool with `python main.py`. There is no automated test suite or linter configured yet.

## Schema Workflow

- `main.py` is the entry point; it starts the console loop defined in `Spammer.run()`.
- `spammer/` is the package holding the core logic: `console.py` renders console styling and ASCII art, `messages.py` builds user-facing prompts, and `core.py` collects phone number/repetition input and dispatches requests.
- `spammer/data/` holds one JSON file per service type (`sms_services.json`, `call_services.json`) describing the third-party endpoints targeted for each channel.

## Contribution Workflow

Contributions go through pull requests opened against `main`. Commit messages follow Conventional Commits.
