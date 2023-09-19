# VisualGit: A Command Line Tool for Git and GitHub

VisualGit is a tool crafted to simplify and streamline the use of Git and GitHub directly from the terminal. Instead of remembering a multitude of commands, interact with a straightforward textual interface that guides you through the most common Git operations.

##  🌟 Features

- **Quick Operations on Local Repos**: Add a repo, commit changes, and more.
- **Efficient Branch Management**: Seamlessly switch between the main branch and other branches, commit, push, and more.
- **Easily Accessible Log**: Instantly view your Git log.
- **Quick Configuration**: Interact with an interface to swiftly configure your repositories.
- **Remote Operations with GitHub**: Beyond operations on local repositories, it facilitates remote operations on GitHub.

## 🛠️ Installation

> **Prerequisite**: You must have Python installed on your system to proceed with the installation. If it's not installed, visit the [official Python website](https://www.python.org/downloads/) to download and install it.

1. Once you've downloaded/cloned the project folder, navigate to the directory of the folder from your terminal.

2. Run the following commands to install `vigit` on your system:

   ```bash
   chmod +x vigit.py
   pip install pyinstaller
   pyinstaller --onefile vigit.py
   sudo mv dist/vigit /usr/local/bin/vigit
   sudo chmod +x /usr/local/bin/vigit

## 🚀 Getting Started

Once you've installed `vigit`, using it is straightforward:

1. Navigate to the directory where you want to work with Git using your terminal.
2. Simply type `vigit` and hit Enter.
3. The `vigit` interface will appear, allowing you to manage your Git operations visually.

For advanced operations or quick actions, make use of the [command-line options](#⚙️-command-line-options) as needed.

## ⚙️ Command-Line Options

`vigit` offers various command-line options to make your Git experience smoother:

- `-a, --create-local-repo`: Quick action to add a local repository.
  
- `-cp, --commit-push-main`: Quick action to commit your changes and push them to the `main` branch.

- `-cb, --commit-push-branch`: Quick action to commit your changes and push them to the current branch (other than `main`).

- `-m, --merge-branch-with-main`: Quick action to merge your current branch with the `main` branch.

Use these options when invoking `vigit` from the terminal to perform these operations immediately without going through the main menu.

## 🔑 Configuration with GitHub

To utilize `vigit` in tandem with GitHub, you'll need to sign in with Github. You'll be asked for your GitHub credentials. Rather than using a password, GitHub advocates using a personal access token:

1. Log into GitHub and go to `Settings`.
2. Navigate to `Developer settings`.
3. Click on `Personal access tokens`.
4. Click on `Tokens (classic)` and follow the instructions to generate your token.
5. When `vigit` prompts for your credentials while interacting with GitHub, use this token in place of your password.

## 💡 Wishlist: Ideas for Future Implementation

- **Enhance User Interface:** Implement the curses library for an enhanced user experience.
- **Add Modules Functionalities:** Allow users to interact with and manage Git modules.
- **Single File Management Functionalities:** Provide specific operations for individual files, such as `git add <filename>`.

## 🤝 Contributing

We welcome contributions from the community! If you've found a bug, have a suggestion, or want to add a new feature, please feel free to create an issue or submit a pull request. Let's make `vigit` even better together!

---

© 2023 Alex Arroyo. All Rights Reserved.
