# Visual Git (vg)

Visual Git is a command line tool that provides an intuitive interface for common Git operations. It simplifies the Git workflow through interactive menus and direct commands.

## Features

- 🖥️ **Interactive interface**: Easy-to-use menus for all common Git operations
- 🌿 **Branch management**: Create, delete, and merge branches with ease
- 🔄 **Remote repository operations**: Push, pull, and sync with remote repositories
- 🛠️ **Advanced operations**: Reset, stash, cherry-pick, and interactive rebase
- ⚡ **Quick actions**: Direct commands for frequent operations
- 🎨 **Colorful interface**: Clear visual feedback for all operations

## Requirements

- Python 3.6 or higher
- Git installed and configured on your system
- `simple_term_menu` library for the menu interface

## Installation

```bash
# Clone the repository
git clone https://github.com/alexaldearroyo/visualgit.git
cd visualgit

# Install the application
python3 -m pip install -e .
```

## Basic Usage

Simply run `vg` to start the interactive interface:

```bash
vg
```

This will display the main menu with the following options:
- Work in Main
- Work in Branches
- See Log
- New Configuration
- Quick Actions

## Command Line Usage

Visual Git supports two command styles:

### Traditional style (with dashes)

```bash
vg -a          # Add local repo
vg -b          # Add local branch
vg -c          # Commit to local repo
vg -p          # Commit & push in main
vg -f          # Merge branch with main
vg -n          # New configuration
vg -s          # See log
```

### Direct style (without dashes)

```bash
vg a           # Add local repo
vg b           # Add local branch
vg c           # Commit to local repo
vg p           # Commit & push in main
vg f           # Merge branch with main
vg n           # New configuration
vg s           # See log
```

## Advanced Operations

Visual Git includes advanced features for experienced users:

- **Reset**: Undo changes at different levels (soft, mixed, hard)
- **Clean**: Remove untracked files
- **Force push**: Force push changes
- **Stash**: Save changes temporarily
- **Cherry-pick**: Select specific commits
- **Interactive rebase**: Reorganize and edit commits

Access these operations from the menu:
`Work in Branches > Advanced operations`

## Examples

1. **Create a local repository**:
   ```bash
   vg add
   ```

2. **Create a branch and commit**:
   ```bash
   vg b            # Create branch
   vg c            # Make commit
   ```

3. **Merge branch with main**:
   ```bash
   vg f
   ```

## Help

To see all available options:

```bash
vg --help
```

## Contribution

Contributions are welcome. If you find a bug or have a suggestion, feel free to open an issue or submit a pull request.
