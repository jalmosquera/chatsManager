# 📚 Cheatsheet Management System

A complete and elegant system for creating, managing, and consulting quick reference sheets (cheatsheets) directly from your terminal.

> 🌐 **[Versión en español / Spanish version](README.md)**

## 📑 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
  - [View a Cheatsheet](#view-a-cheatsheet)
  - [Search Commands Globally](#search-commands-globally)
  - [Create New Cheatsheet](#create-new-cheatsheet)
  - [Add Commands](#add-commands)
  - [Edit Commands](#edit-commands)
  - [Delete Commands](#delete-commands)
  - [Add Live Aliases](#add-live-aliases)
  - [Help](#help)
- [Project Structure](#-project-structure)
- [Advanced Features](#-advanced-features)
- [Usage Examples](#-usage-examples)

## ✨ Features

- 🎯 **Intuitive Management**: Simple and consistent command system with `cs` prefix
- 📝 **Rich Rendering**: Markdown cheatsheets rendered as colored name, command, and description tables
- ▦ **Automatic Banners**: Each cheatsheet generates a compact banner from its title when opened
- 🔄 **Live Aliases**: Create aliases that work both as documentation and real shell commands
- 📁 **Category Organization**: Interactive category selection when adding commands
- ⌨️ **Literal Preservation**: Keeps the exact capitalization, symbols, and shortcuts you enter
- 🎨 **Smart Emojis**: Automatic emoji assignment based on command type
- 🔍 **Global Search**: `csfind` finds names, commands, and descriptions across every cheatsheet
- 🧭 **Interactive Hub**: `cs` shows a centered table selectable by number, name, or Tab
- 🎯 **Semantic Icons**: Each cheatsheet has an icon that matches its tool
- 🔧 **Automatic Synchronization**: Aliases automatically sync with Fish shell
- 🐧 **Portable Installation**: One installer prepares macOS and Linux with the same dependencies and configuration

## 🔧 Requirements

The installer detects and installs `fish`, `fzf`, `python3`, `less`, and Rich. It supports Homebrew on macOS and `apt`, `dnf`, `pacman`, or `apk` on Linux. macOS requires [Homebrew](https://brew.sh) in advance; Linux may ask for your `sudo` password.

## 📦 Installation

Clone and run one command:

```bash
git clone https://github.com/jalmosquera/chatsManager.git ~/.cheatsheets && ~/.cheatsheets/install.sh
```

The installer creates a local virtual environment at `~/.cheatsheets/.venv` and an isolated snippet at `~/.config/fish/conf.d/cheats_manager.fish`; it does not replace `config.fish` or your personal aliases file. Open a new Fish terminal or load it now:

```fish
source ~/.config/fish/conf.d/cheats_manager.fish
cs
```

Preview all actions without modifying the system:

```bash
~/.cheatsheets/install.sh --dry-run
```

## 📖 Usage

### View a Cheatsheet

To view an existing cheatsheet:

```bash
cs <tool-name>
```

Running `cs` without arguments opens a centered hub with a table of management actions and cheatsheets. Type `/` to open search, or type its number or name and press `Enter`; `Tab` completes the name and `Esc` cancels. CRUD actions show a breadcrumb and, after success, a summary that closes with `Enter` before returning to the hub. In a CRUD target selector, `q` or `Esc` cancel and return to the hub. When opening a cheatsheet from this menu, `q` returns to the hub. Each cheatsheet has a semantic icon, such as `⚡ warp`, `🪟 tmux`, `⌨️ nvim`, `🐳 docker`, and `🔀 git`.

**Examples**:
```bash
cs git          # View git cheatsheet
cs docker       # View docker cheatsheet
cs nvim         # View nvim cheatsheet
```

### Search Commands Globally

Search by cheatsheet name, section, entry name, command, or description without case sensitivity:

```bash
csfind
```

The right panel displays a preview. Once a `.md` cheatsheet is open, use `/` or `?` to search within it, `n`/`N` to navigate matches, and `q` to return to the hub.

### Create New Cheatsheet

Create a new cheatsheet from scratch:

```bash
csnew <tool-name>
```

For each entry, the system will ask for:
1. Name
2. Command
3. Description
4. It will automatically categorize and create the file

**Example**:
```bash
csnew kubectl
# Name: List pods
# Command: kubectl get pods
# Description: List all pods
```

### Add Commands

Add commands to an existing cheatsheet:

```bash
csadd <tool-name>
```

**Interactive flow**:
1. Enter name, command, and description separately
2. Select category for each command:
   - Choose an existing category (by number)
   - Or create a new category (option 0)

**Example**:
```bash
csadd git
# Name: Save changes
# Command: git stash
# Description: Save changes temporarily
# Then select a category
```

### Edit Commands

Edit existing commands in a cheatsheet:

```bash
csedit <tool-name>
```

The system will display all numbered entries. Select one and modify its name, command, and/or description.

**Example**:
```bash
csedit docker
# Select command number to edit
# Modify name, command, and description
# Confirm changes
```

### Delete Commands

Delete commands from a cheatsheet:

```bash
csdel <tool-name>
```

Displays all commands and lets you select which ones to delete.

### Add Live Aliases

**Live aliases** are aliases that work both as documentation in the cheatsheet and as real commands in your shell:

```bash
csalias
```

The flow asks for the alias name, the command to execute, and the description in separate fields.

**Example**:
```bash
csalias
# Alias name: ll
# Command to execute: ls -lah
# Description: Detailed list with hidden files
```

Aliases will be automatically added to:
- ✅ The `aliases.md` cheatsheet (documentation)
- ✅ Your Fish configuration (functionality)

### Help

View complete system help:

```bash
cshelp
```

## 📂 Project Structure

```
~/.cheatsheets/
├── README.md                    # Spanish documentation (primary)
├── README_EN.md                 # English documentation
├── fish_aliases_example.fish   # Fish functions: cs, csfind, and interactive hub
├── install.sh                  # macOS and Linux installer
├── requirements.txt            # Rich Python dependency
├── runtime_paths.py            # Portable installation paths
├── csnew                       # Create new cheatsheet
├── csadd                       # Add commands
├── csedit                      # Edit commands
├── csdel                       # Delete commands
├── csalias                     # Add live aliases
├── cshelp                      # View help
├── create_cheatsheet.py        # Script to create cheatsheets
├── add_to_cheat.py            # Script to add commands
├── edit_cheat.py              # Script to edit commands
├── delete_cheat.py            # Script to delete commands
├── add_alias.py               # Script to add aliases
├── sync_aliases.py            # Script to sync aliases with Fish
├── render_cheatsheet.py        # Rich renderer with tables and Tmux theme
├── index_cheatsheets.py        # Global search index for csfind
└── *.md                       # Cheatsheet files
```

## 🚀 Advanced Features

### Interactive Categorization

When adding commands with `csadd`, you can:
- View all existing categories with command counts
- Select an existing category by number
- Create a new category on the fly

### Command and Shortcut Preservation

The system saves commands exactly as you enter them. This prevents automatic changes to shortcuts, flags, capitalization, or symbols:

```
ctrl+a+n - Create session
git status --short - Show compact status
```

### Contextual Emojis

Commands automatically receive emojis based on their function:
- 📦 Install, add
- ⚙️ Config, setup
- 🆕 Create, new
- 🗑️ Delete, remove
- 📋 List, show
- ▶️ Start, run
- 🔨 Build
- 🚀 Deploy
- And many more...

### Alias Synchronization

When you edit the aliases cheatsheet with `csedit aliases` or `csadd aliases`, the system:
1. Detects that you're modifying aliases
2. Automatically runs the synchronization script
3. Updates your Fish configuration
4. Informs you of the changes

### Elegant Visualization

All cheatsheets are visualized with Rich, which provides:
- Separate name, command, and description columns
- Colors synchronized with the active Tmux theme, with Tokyo Night as fallback
- Centered tables with borders and row separators
- A pager compatible with `/`, `?`, `n`, `N`, and `q`

## 💡 Usage Examples

### Example 1: Create Docker Cheatsheet

```bash
# Create the cheatsheet
csnew docker

# Name: List containers
# Command: docker ps
# Description: List running containers

# View the result
cs docker
```

### Example 2: Add More Commands to Git

```bash
# Add commands
csadd git

# Name: Apply commit
# Command: git cherry-pick <commit>
# Description: Apply a specific commit

# Select category
# 1. Basic Commands (15 commands)
# 2. Branching (8 commands)
# 3. Advanced Commands (5 commands)
# 0. [Create new category]
# Which category? (1-3, 0 for new): 3
```

### Example 3: Add Custom Aliases

```bash
# Add aliases that work immediately
csalias

# Alias name: gco
# Command to execute: git checkout
# Description: Switch branch

# Aliases work right away:
gco main          # Switch to main branch
dc up -d          # Run docker-compose up -d
```

### Example 4: Edit an Existing Command

```bash
# Edit cheatsheet
csedit nvim

# View numbered command list
# 1. :w - Save file
# 2. :q - Quit
# 3. :wq - Save and quit
# ...

# Select command: 1

# Edit:
# New command [:w]: :w!
# New description [Save file]: Force save file
# Confirm changes? (y/n): y
```

## 🎯 Tips and Tricks

1. **Use clear descriptions**: Descriptions help remember what each command does
2. **Organize by categories**: Use logical categories to facilitate searching
3. **Short aliases**: For live aliases, use short and memorable names
4. **Update regularly**: Add new commands as you learn them
5. **Sync your configuration**: Keep the `.cheatsheets` directory in a repo to use across multiple machines

## 🤝 Contributing

This project is designed for personal use, but feel free to fork and adapt it to your needs.

## 📄 License

MIT License - Feel free to use and modify according to your needs.

---

*Created to keep your commands organized and accessible from any terminal* 🚀
