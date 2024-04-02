"""
whatdido grabs its configuration information from the .didorc file in the root of the git repository.
"""

import os
import json

from typer import Typer, prompt

app = Typer()


class Config:
    """
    The configuration class for the application.
    """

    def __init__(self) -> None:
        self.open_ai_api_key = os.environ.get("OPEN_AI_API_KEY")
        self.open_ai_model = os.environ.get("OPEN_AI_MODEL", "gpt-4-turbo-preview")
        self.temperature = 0.8
        self.instructions = [
            "You're a developer working on a project.",
            "You're about to commit some changes to the project.",
            "Explain the changes. Be as terse as possible. No line breaks, no more than 250 characters.",
        ]


def get_config_dir() -> str:
    return os.path.dirname(get_config_file())


def get_config_file() -> str:
    """
    Get the path to the .env file in the root of the git repository.
    """
    # recurse up from current directory to find the .dido directory
    cwd = os.getcwd()

    while not os.path.exists(os.path.join(cwd, ".dido")) and cwd != "/":
        cwd = os.path.dirname(cwd)

    # if we've reached the root directory, then we can't find the .dido directory
    # so we'll just use the current directory
    if cwd == "/":
        cwd = os.getcwd()

    return os.path.join(cwd, ".dido/config.json")


def validate_config_data(config: dict) -> tuple[bool, list[str]]:
    """
    Validate the configuration.
    """
    if not isinstance(config, dict):
        return (False, ["Configuration must be a dictionary."])

    if "open_ai_api_key" not in config:
        return (False, ["open_ai_api_key is required."])

    if "open_ai_model" not in config:
        return (False, ["open_ai_model is required."])

    return (True, [])


def load_config() -> Config:
    """
    Load configuration from the .env file.
    """
    config = Config()

    config_file = get_config_file()

    # Ensure the file exists
    if not os.path.exists(config_file):
        config = prompt_for_config()
        save_config(config)

    try:
        data = json.load(open(config_file, encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid configuration file: {config_file}") from e

    (valid, errors) = validate_config_data(data)

    if not valid:
        raise ValueError(f"Invalid configuration: {errors}")

    config.__dict__.update(data)
    return config


def save_config(config: Config):
    """
    Save configuration to the .env file.
    """
    config_file = get_config_file()

    # ensure folder exists
    os.makedirs(os.path.dirname(config_file), exist_ok=True)

    (valid, errors) = validate_config_data(config.__dict__)

    if not valid:
        raise ValueError(f"Invalid configuration: {errors}")

    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config.__dict__, f, indent=2)


@app.command("setup")
def prompt_for_config() -> Config:
    """
    Prompt the user for configuration information.
    """
    config = Config()

    config.open_ai_api_key = prompt("OpenAI API Key", default=config.open_ai_api_key)
    config.open_ai_model = prompt("OpenAI Model", default=config.open_ai_model)
    return config


@app.command("read")
def list_config() -> None:
    """
    List the configuration values.
    """
    config = load_config()
    print(json.dumps(config.__dict__, indent=2))


@app.command("get")
def get_config(key: str) -> None:
    """
    Get a configuration value.
    """
    config = load_config()

    if not hasattr(config, key):
        raise ValueError(
            f"Invalid key: {key}. Available keys: {list(config.__dict__.keys())}"
        )

    print(getattr(config, key))


@app.command("set")
def set_config(key: str, value: str) -> None:
    """
    Set a configuration value.
    """
    config = load_config()

    if not hasattr(config, key):
        raise ValueError(
            f"Invalid key: {key}. Available keys: {list(config.__dict__.keys())}"
        )

    setattr(config, key, value)
    save_config(config)


if __name__ == "__main__":
    app()
