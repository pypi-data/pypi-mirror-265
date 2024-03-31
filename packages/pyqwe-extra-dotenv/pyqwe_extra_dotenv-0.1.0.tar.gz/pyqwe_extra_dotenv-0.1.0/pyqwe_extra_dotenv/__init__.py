import os

try:
    import pyqwe
except ImportError:
    raise ImportError("pyqwe not found")

__version__ = "0.1.0"


class EnvVarNotFound(Exception):
    pass


class Colr:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def _import_python_dotenv() -> bool:
    try:
        import dotenv

        dotenv.load_dotenv()

        return True

    except ImportError:
        return False


def _extract_env_vars(r: str) -> list[str]:
    if "{{" and "}}" in r:
        return [i.split("}}")[0].replace(" ", "") for i in r.split("{{") if "}}" in i]
    return []


def _replace_env_vars(r: str) -> str:
    python_dotenv_import_attempted = False

    for env_var in _extract_env_vars(r):
        if not os.getenv(env_var):
            # if env_var is not found
            if not python_dotenv_import_attempted:
                # if the import of python-dotenv has not been attempted
                if not _import_python_dotenv():
                    # if the import of python-dotenv failed
                    raise EnvVarNotFound(
                        "\n\r\n\r"
                        f"{Colr.FAIL}Environment variable {env_var} was not found.{Colr.END}"
                        "\n\r"
                        "An attempt to load environment variables using python-dotenv was made, "
                        "but the python-dotenv library was not found."
                        "\n\r"
                        "\n\r"
                        "To install python-dotenv, run: pip install python-dotenv"
                        "\n\r\n\r"
                        "For more information about python-dotenv, visit: "
                        "https://pypi.org/project/python-dotenv/"
                        "\n\r"
                    )

            python_dotenv_import_attempted = True

            if not os.getenv(env_var):
                # if env_var is still not found
                raise EnvVarNotFound(
                    "\n\r\n\r"
                    f"{Colr.FAIL}Environment variable {env_var} was not found.{Colr.END}"
                    "\n\r"
                    "An attempt to load environment variables using python-dotenv was made, "
                    "but the environment variable was still not found."
                    "\n\r"
                )

        r = r.replace(f"{{{{{env_var}}}}}", os.getenv(env_var))

    return r
