#!/usr/bin/env python3
import os
import shutil
import subprocess
import argparse
import sys

# --- ANSI Color Codes for printing ---
COLOR_CYAN = "\033[1;36m"
COLOR_GREEN = "\033[1;32m"
COLOR_YELLOW = "\033[1;33m"
COLOR_RED = "\033[1;31m"
COLOR_RESET = "\033[0m"


def print_step(msg):
    """Prints a formatted step message in bold cyan."""
    print(f"{COLOR_CYAN}==> {msg}{COLOR_RESET}")


def print_success(msg):
    """Prints a formatted success message in bold green."""
    print(f"\n{COLOR_GREEN}{msg}{COLOR_RESET}")


def print_warning(msg):
    """Prints a formatted warning message in bold yellow."""
    print(f"{COLOR_YELLOW}Warning: {msg}{COLOR_RESET}")


def print_error(msg):
    """Prints a formatted error message in bold red and exits."""
    print(f"{COLOR_RED}Error: {msg}{COLOR_RESET}", file=sys.stderr)
    sys.exit(1)


def run_command(command, error_msg):
    """Runs a command and handles potential errors."""
    try:
        # We use capture_output=True to hide the command's stdout/stderr
        # unless an error occurs.
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        # If the command fails, print its output for debugging
        print_error(f"{error_msg}\n--- Details ---\n{e.stderr.strip()}")
    except FileNotFoundError:
        print_error(
            f"Command '{command[0]}' not found. Is git installed and in your PATH?"
        )


def main():
    """Main function to initialize the GitHub repository."""
    parser = argparse.ArgumentParser(
        description=(
            "Initialize a new GitHub repository in a specified directory.\n\n"
            "This script will:\n"
            "  - Initialize a git repo\n"
            "  - Add a .gitignore (from ignore.txt if present)\n"
            "  - Add all files and make the first commit\n"
            "  - Set the branch to main\n"
            "  - Add a remote origin\n"
            "  - Push to GitHub\n\n"
            "Use --current to skip the directory prompt and use the current directory."
        ),
        # Use RawTextHelpFormatter to preserve newlines in the description
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--current",
        action="store_true",
        help="Use the current working directory instead of prompting for a directory.",
    )
    args = parser.parse_args()

    # --- 1. Determine Repository Directory ---
    if args.current:
        repo_dir = os.getcwd()
        print_step(f"Using current working directory: {repo_dir}")
    else:
        print_step("Choose the directory for the new git repo")
        repo_dir_input = input("Enter the directory path: ").strip()
        if not repo_dir_input:
            print_error("Directory path cannot be empty.")

        repo_dir = os.path.abspath(repo_dir_input)
        if not os.path.isdir(repo_dir):
            print_error(f"Directory does not exist: {repo_dir}")

    # Change to the target directory
    os.chdir(repo_dir)
    print_step(f"Changed to directory: {repo_dir}")

    # --- 2. Initialize Git and Create .gitignore ---
    print_step("Initializing git repository")
    run_command(["git", "init"], "Failed to initialize git.")

    gitignore_path = os.path.join(repo_dir, ".gitignore")

    # Create an empty .gitignore file
    with open(gitignore_path, "a"):
        pass
    print_step("Created .gitignore file")

    # Copy ignore.txt from script's directory to .gitignore if it exists
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ignore_txt_path = os.path.join(script_dir, "ignore.txt")

        if os.path.exists(ignore_txt_path):
            shutil.copyfile(ignore_txt_path, gitignore_path)
            print_step("Copied ignore.txt to .gitignore successfully")
        else:
            print_warning(
                f"ignore.txt not found in {script_dir}, so .gitignore is empty."
            )
    except Exception as e:
        print_warning(f"Could not process ignore.txt. Error: {e}")

    # --- 3. Git Commit and Branch ---
    print_step("Adding all files to git")
    run_command(["git", "add", "."], "Failed to add files.")

    print_step("Creating initial commit")
    run_command(
        ["git", "commit", "-m", "first commit"],
        "Failed to create initial commit. Are there any files to commit?",
    )

    print_step("Renaming branch to 'main'")
    run_command(["git", "branch", "-M", "main"], "Failed to rename branch.")

    # --- 4. Git Remote and Push ---
    repo_url = input(
        "Enter the GitHub repository URL (e.g., https://github.com/user/repo.git): "
    ).strip()
    if not repo_url.startswith("https://") and not repo_url.startswith("git@"):
        print_error("Invalid repository URL format.")

    print_step(f"Adding remote origin: {repo_url}")
    run_command(
        ["git", "remote", "add", "origin", repo_url],
        "Failed to add remote 'origin'. Does it already exist?",
    )

    # This step is useful if the remote repo was created with a README or license.
    # It might fail if the remote is completely empty, which is fine.
    print_step("Attempting to pull and rebase from origin/main (if it exists)")
    try:
        # We also need to specify --allow-unrelated-histories for the initial pull
        subprocess.run(
            [
                "git",
                "pull",
                "--rebase",
                "origin",
                "main",
                "--allow-unrelated-histories",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        print_warning(
            "Could not pull from remote. This is normal for a brand new empty repository."
        )

    print_step("Pushing to GitHub and setting upstream")
    run_command(
        ["git", "push", "--set-upstream", "origin", "main"],
        "Failed to push to GitHub. Check your URL and permissions.",
    )

    repo_name = os.path.basename(repo_url.rstrip("/").replace(".git", ""))
    print_success(
        f"GitHub repository '{repo_name}' has been set up successfully in '{repo_dir}'!"
    )


if __name__ == "__main__":
    main()
