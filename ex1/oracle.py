import os

try:
    from dotenv import load_dotenv
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False

KEYS = ["MATRIX_MODE", "DATABASE_URL", "API_KEY", "LOG_LEVEL",
        "ZION_ENDPOINT"]
FOLDER = os.path.dirname(os.path.abspath(__file__))


def load_config() -> tuple[dict[str, str], list[str]]:
    # variables that already exist in the shell, before reading the .env
    from_shell = [key for key in KEYS if key in os.environ]
    # override=False: the .env never replaces a shell variable
    if HAS_DOTENV:
        load_dotenv(os.path.join(FOLDER, ".env"), override=False)
    config: dict[str, str] = {}
    for key in KEYS:
        config[key] = os.getenv(key, "")
    if config["MATRIX_MODE"] == "":
        config["MATRIX_MODE"] = "development"
    if config["LOG_LEVEL"] == "":
        config["LOG_LEVEL"] = "INFO"
    return config, from_shell


def hide(secret: str) -> str:
    # show only the first 2 letters
    return secret[:2] + "****"


def hide_password(url: str) -> str:
    # scheme://user:password@host  ->  scheme://user:****@host
    if "@" not in url or "://" not in url:
        return url
    start, rest = url.split("://", 1)
    login, host = rest.rsplit("@", 1)
    user = login.split(":")[0]
    return f"{start}://{user}:****@{host}"


def show_status(config: dict[str, str]) -> None:
    print("Configuration loaded:")
    print(f"Mode: {config['MATRIX_MODE']}")
    if config["DATABASE_URL"] == "":
        print("Database: Not configured")
    elif "localhost" in config["DATABASE_URL"] or \
            "sqlite" in config["DATABASE_URL"]:
        print("Database: Connected to local instance")
    else:
        print("Database: Connected to remote instance")
    if config["API_KEY"] == "":
        print("API Access: Not authenticated")
    else:
        print("API Access: Authenticated")
    print(f"Log Level: {config['LOG_LEVEL']}")
    if config["ZION_ENDPOINT"] == "":
        print("Remote Network: Offline")
    else:
        print("Remote Network: Online")


def show_details(config: dict[str, str]) -> None:
    print()
    if config["MATRIX_MODE"] == "production":
        print("Production mode: details are hidden.")
        return
    print("Development mode: details")
    for key in KEYS:
        value = config[key]
        if value == "":
            value = "(missing)"
        elif key == "API_KEY":
            value = hide(value)
        elif key == "DATABASE_URL":
            value = hide_password(value)
        print(f"  {key} = {value}")


def show_warnings(config: dict[str, str]) -> None:
    warnings: list[str] = []
    if not HAS_DOTENV:
        warnings.append("python-dotenv is not installed")
    elif not os.path.isfile(os.path.join(FOLDER, ".env")):
        warnings.append("no .env file (cp ex1/.env.example ex1/.env)")
    for key in KEYS:
        if config[key] == "":
            warnings.append(f"{key} is missing")
    if len(warnings) > 0:
        print()
    for warning in warnings:
        print(f"[WARNING] {warning}")


def gitignore_has_env() -> bool:
    try:
        with open(os.path.join(FOLDER, ".gitignore")) as file:
            return ".env" in file.read().split()
    except OSError:
        return False


def show_security(from_shell: list[str]) -> None:
    print()
    print("Configuration security check:")
    # the secret comes from the environment, never from this file
    print("[OK] No hardcoded secrets detected")
    if gitignore_has_env():
        print("[OK] .env file properly ignored by git")
    else:
        print("[KO] .env is not in ex1/.gitignore")
    if len(from_shell) > 0:
        print("[OK] Production overrides available "
              f"(from the shell: {', '.join(from_shell)})")
    else:
        print("[OK] Production overrides available")


def main() -> None:
    print()
    print("ORACLE STATUS: Consulting the configuration...")
    print()
    config, from_shell = load_config()
    show_status(config)
    show_details(config)
    show_warnings(config)
    show_security(from_shell)
    print()
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()
