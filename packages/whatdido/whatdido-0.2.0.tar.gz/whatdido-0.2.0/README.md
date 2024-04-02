# Whatdido

No more "git commit -m "adsfkjaef"" in a fit of rage. Simply type `dido` to add your changes and write a simple and sane commit message.

**This package is in an exploratory beta state. Please use carefully and at your own risk.**

## Installation

```bash
pip install whatdido

cd <any repo>

echo "Here's a new file for Tony" > "tony.txt"

git add tony.txt

whatdido summary

> Added new file 'tony.txt' containing the text \"Here's a new file for Tony\".

```

Here's a bash helper function for quicker usage:

```bash
dido() {
    git add -A
    git commit -m "$(whatdido summary)"
}
```

## Usage

```
whatdido --help

 Usage: whatdido [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.  │
│ --show-completion             Show completion for the current shell, to  │
│                               copy it or customize the installation.     │
│ --help                        Show this message and exit.                │
╰──────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────╮
│ commit     Edit the summary and commit to the repo in one shot           |
│ config                                                                   │
│ diff       Get the terse diff of the staged changes.                     │
│ summary    Summarize the changes in the repository.                      │
╰──────────────────────────────────────────────────────────────────────────╯
```
