import tempfile
import subprocess


EDITOR_BIN = "vi"


def inline_edit(message: str):
    """Edit the message using vim and return the updated message."""

    outfile = tempfile.NamedTemporaryFile(
        suffix=".txt", mode="w+t", encoding="utf-8", delete=False
    )

    with outfile as f:
        f.write(message)
        f.flush()
        subprocess.run([EDITOR_BIN, f.name], check=True)

        with open(f.name, "r", encoding="utf-8") as f_updated:
            message = f_updated.read()

    return message
