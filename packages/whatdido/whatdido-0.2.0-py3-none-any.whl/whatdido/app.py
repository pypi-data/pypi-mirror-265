"""
The CLI entry point for the application.
"""

import re

import openai
import typer

from whatdido.config import load_config, app as config_app
from whatdido.repo import get_repo, assert_in_git_repo
from whatdido.editor import inline_edit

NO_CHANGES_MESSAGE = "No changes to commit. Run `git add` to stage changes."

DIFF_STAGED_SEGMENTS = [
    "HEAD",
    "--staged",
    "--unified=0",
    "--no-color",
    "--no-prefix",
    "--no-renames",
    "--no-ext-diff",
    "--no-textconv",
    "--text",
]
DIFF_CLEANERS = [
    [r"^\d+\s*", ""],  # Remove line numbers,
    [r"\s+", " "],  # Remove extra spaces,
    [r"^\s+", ""],  # Remove leading spaces,
]
MESSAGE_ESCAPERS = [
    ["\n", "\\n"],
    ["\r", "\\r"],
    ["\t", "\\t"],
    ["\v", "\\v"],
    ["\f", "\\f"],
    ['"', '\\"'],
]


config = load_config()

app = typer.Typer()
app.add_typer(config_app, name="config")


def get_terse_git_diff():
    """
    Pares down the git diff to a terse format
    which can be used as input to the OpenAI API.
    Without this function, the diff would be more likely to hit the API's token limit.
    """
    repo = get_repo()

    diff = repo.git.diff(*DIFF_STAGED_SEGMENTS)

    # We don't need all of the spacing, or the line numbers.
    # Use a series of "cleaning" regexes to remove
    # the line numbers and the first 9 spaces.
    for cleaner in DIFF_CLEANERS:
        diff = re.sub(cleaner[0], cleaner[1], diff)

    return diff


def get_ai_summary(diff: str, pst: str):
    """
    Get the AI summary of the changes.
    """

    client = openai.Client(api_key=config.open_ai_api_key)

    messages = [
        {
            "role": "system",
            "content": "\n".join([*config.instructions, pst]),
        }
    ]

    for diff_line in diff.split("\n"):
        messages.append(
            {
                "role": "user",
                "content": diff_line,
            }
        )

    response = client.chat.completions.create(
        model=config.open_ai_model,
        temperature=config.temperature,
        messages=messages,
    )

    message = response.choices[0].message.content
    return message


@app.command("diff")
def run_diff():
    """
    Get the terse diff of the staged changes.
    """
    print(get_terse_git_diff())


def get_summary(pst: str) -> str | None:
    """
    Get the commit message from the user.
    """

    assert_in_git_repo()

    diff = get_terse_git_diff()

    # if there are no changes, there is no need to summarize
    if not diff:
        return None

    commit_summary = get_ai_summary(diff, pst)

    for escaper in MESSAGE_ESCAPERS:
        commit_summary = commit_summary.replace(escaper[0], escaper[1])

    return commit_summary


@app.command("summary")
def run_summary(pst: str = ""):
    """
    Summarize the changes in the repository.
    """
    print(get_summary(pst) or NO_CHANGES_MESSAGE)


@app.command("commit")
def run_commit(pst: str = ""):
    """
    Edit the message using the user's preferred editor.
    """

    commit_summary = get_summary(pst)

    if not commit_summary:
        print(NO_CHANGES_MESSAGE)
        return

    commit_summary = inline_edit(commit_summary)

    repo = get_repo()

    repo.index.commit(commit_summary)


def main():
    """
    Main function to run the app.

    ```bash
    whatdido summarize
    """

    app()
