import importlib
import sys
from types import ModuleType


def load_reagent(name: str) -> ModuleType | None:
    try:
        # instead of one import for each library
        return importlib.import_module(name)
    except ImportError:
        return None


def show_pip_vs_poetry() -> None:
    print("pip vs Poetry:")
    print("  pip: reads requirements.txt and installs the packages")
    print("       in the environment that is active.")
    print("  Poetry: reads pyproject.toml, creates its own venv and")
    print("          saves the exact versions in poetry.lock.")


def show_install_help(missing: list[str]) -> None:
    print("Missing reagents: " + ", ".join(missing))
    print()
    print("Install with pip (inside the venv):")
    print("  pip install -r ex0/requirements.txt")
    print()
    print("Install with Poetry:")
    print("  cd ex0")
    print("  poetry install")
    print("  poetry run python loading.py")


def main() -> None:
    reagents = ["pandas", "numpy"]
    missing: list[str] = []

    print()
    print("REAGENT STATUS: Loading reagents...")
    print()
    print(f"Python environment: {sys.prefix}")
    print()
    print("Checking dependencies:")
    for name in reagents:
        module = load_reagent(name)
        if module is None:
            print(f"[MISSING] {name} - not installed")
            missing.append(name)
        else:
            print(f"[OK] {name} ({module.__version__}) - ready")
    print()
    show_pip_vs_poetry()
    print()
    if len(missing) > 0:
        show_install_help(missing)
    else:
        print("All reagents are ready.")


if __name__ == "__main__":
    main()
