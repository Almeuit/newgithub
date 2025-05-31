# newgithub.py

## Overview

`newgithub.py` is a Python script that automates the process of initializing a new Git repository in a specified directory, setting up a `.gitignore` file, making the initial commit, and pushing the repository to GitHub.

## Features

* Initializes a new Git repository in a user-specified directory.
* Copies a template `ignore.txt` (if present) to `.gitignore`.
* Adds all files and makes the first commit.
* Sets the default branch to `main`.
* Adds a remote GitHub repository.
* Pushes the initial commit to GitHub and sets the upstream branch.

---

## Usage

1.  **Prepare**: Place `newgithub.py` in a directory. Optionally, add an `ignore.txt` file in the same directory to serve as your `.gitignore` template.

2.  **Run the Script**: Open a terminal and execute:

    ```sh
    python3 newgithub.py
    ```

    You can also use the `--current` flag to initialize a repository in your current working directory without being prompted:

    ```sh
    python3 newgithub.py --current
    ```

3.  **Follow Prompts**:

    * Enter the path to the directory you want to initialize as a Git repository (if not using `--current`).
    * Enter the GitHub repository URL (e.g., `git@github.com:Almeuit/newrepo.git).

4.  **Result**: The script will:

    * Initialize the repository.
    * Copy `ignore.txt` to `.gitignore` (if available).
    * Add and commit all files.
    * Set the branch to `main`.
    * Add the GitHub remote.
    * Push the initial commit to GitHub.

---

## Notes

* If `ignore.txt` is not found in the same directory as the script, `.gitignore` will be created empty.
* This script requires **Git** to be installed and available in your system's PATH.
* You must have permission to push to the specified GitHub repository.

---

## Example

<details>
<summary>Click to view an example of script execution.</summary>

```sh
python3 newgithub.py
# ==> Step 1: Choose directory for new git repo
# Enter the directory to initialize as a git repo: /path/to/my/project
# ==> Step 2: Changed to directory /path/to/my/project
# ==> Step 3: Initializing git repository
# Initialized empty Git repository in /path/to/my/project/.git/
# ==> Step 4: Created .gitignore file
# Warning: ignore.txt not found in /path/to/script/directory, .gitignore will be empty.
# ==> Step 5: Adding all files to git
# ==> Step 6: Creating initial commit
# [main (root-commit) 6e4a2b9] first commit
#  2 files changed, 0 insertions(+), 0 deletions(-)
#  create mode 100644 .gitignore
#  create mode 100644 some_file.txt
# ==> Step 7: Setting branch to main
# ==> Step 8: Adding remote origin [https://github.com/username/my-project.git](https://github.com/username/my-project.git)
# Enter the GitHub repository URL: [https://github.com/username/my-project.git](https://github.com/username/my-project.git)
# ==> Step 9: Pushing to GitHub with upstream set
# Enumerating objects: 3, done.
# Counting objects: 100% (3/3), done.
# Delta compression using up to 8 threads
# Compressing objects: 100% (2/2), done.
# Writing objects: 100% (3/3), 273 bytes | 273.00 KiB/s, done.
# Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
# To [https://github.com/username/my-project.git](https://github.com/username/my-project.git)
#  * [new branch]      main -> main
# Branch 'main' set up to track remote branch 'main' from 'origin'.
#
# Github Repo my-project has been setup within /path/to/my/project
