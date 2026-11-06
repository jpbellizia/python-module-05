import os
import site
import sys


def in_virtual_env() -> bool:
    # sys.prefix is where python is working now
    # sys.base_prefix is where original python of system is working from
    return sys.prefix != sys.base_prefix


def global_site_packages() -> str:
    # build the global path by hand, using the original python
    version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    return os.path.join(sys.base_prefix, "lib", version, "site-packages")


def show_outside() -> None:
    print("LABORATORY STATUS: You are working in the open")
    print()
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()
    print("WARNING: You are in the global environment!")
    print("Every reagent you install here leaks into the whole system.")
    print()
    print("Global reagent installation path:")
    print(global_site_packages())
    print()
    print("To seal the laboratory, run:")
    print("python3 -m venv lab_env")
    print("source lab_env/bin/activate # On Unix")
    print("lab_env\\Scripts\\activate # On Windows")
    print()
    print("Then run this program again.")


def show_inside() -> None:
    # get the path
    env_path = sys.prefix
    # get the venv name
    env_name = os.path.basename(env_path)
    print("LABORATORY STATUS: The laboratory is sealed")
    print()
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {env_name}")
    print(f"Environment Path: {env_path}")
    print()
    print("SUCCESS: You are working in an isolated environment!")
    print("Safe to install reagents without affecting")
    print("the global system.")
    print()
    print("Reagent installation path:")
    for path in site.getsitepackages():
        print(path)
    print()
    print("Global installation path (not touched by the venv):")
    print(global_site_packages())


def main() -> None:
    print()
    if in_virtual_env():
        show_inside()
    else:
        show_outside()


if __name__ == "__main__":
    main()
