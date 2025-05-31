#!/usr/bin/env python3
import os
import shutil
import subprocess
import argparse

def print_step(msg):
    print(f"\033[1;36m==> {msg}\033[0m")  # Bold cyan

def main():
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
            "Use --current to skip the directory prompt and use the current working directory."
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--current',
        action='store_true',
        help="Use the current working directory instead of prompting for a directory."
    )
    args = parser.parse_args()

    # Ask user for directory to create repo in, unless --current is set
    if args.current:
        repo_dir = os.getcwd()
        print_step(f"Step 1: Using current working directory {repo_dir}")
    else:
        print_step("Step 1: Choose directory for new git repo")
        repo_dir = input("Enter the directory to initialize as a git repo: ").strip()
        repo_dir = os.path.abspath(repo_dir)
        if not os.path.isdir(repo_dir):
            print(f"\033[1;31mDirectory does not exist: {repo_dir}\033[0m")
            return

    # Go to that directory
    os.chdir(repo_dir)
    print_step(f"Step 2: Changed to directory {repo_dir}")

    # git init
    print_step("Step 3: Initializing git repository")
    subprocess.run(["git", "init"], check=True)

    # touch .gitignore
    gitignore_path = os.path.join(repo_dir, ".gitignore")
    open(gitignore_path, "a").close()
    print_step("Step 4: Created .gitignore file")

    # Copy ignore.txt from script's directory to .gitignore
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ignore_txt_path = os.path.join(script_dir, "ignore.txt")
    if os.path.exists(ignore_txt_path):
        shutil.copyfile(ignore_txt_path, gitignore_path)
        print_step("Copied ignore.txt to .gitignore successfully")
    else:
        print(f"\033[1;33mWarning: ignore.txt not found in {script_dir}, .gitignore will be empty.\033[0m")

    # ga . (git add .)
    print_step("Step 5: Adding all files to git")
    subprocess.run(["git", "add", "."], check=True)

    # git commit -m "first commit"
    print_step('Step 6: Creating initial commit')
    subprocess.run(["git", "commit", "-m", "first commit"], check=True)

    # git branch -M main
    print_step('Step 7: Setting branch to main')
    subprocess.run(["git", "branch", "-M", "main"], check=True)

    # git remote add origin <url>
    repo_url = input("Enter the GitHub repository URL: ").strip()
    print_step(f"Step 8: Adding remote origin {repo_url}")
    subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)

    # gp --set-upstream origin main
    print_step("Step 9: Pushing to GitHub with upstream set")
    subprocess.run(["git", "push", "--set-upstream", "origin", "main"], check=True)

    repo_name = os.path.basename(repo_url.rstrip("/").replace(".git", ""))
    print(f"\n\033[1;32mGithub Repo {repo_name} has been setup within {repo_dir}\033[0m")

if __name__ == "__main__":
    main()
