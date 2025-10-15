# 📚 Cheatsheet Management System

A complete and elegant system for creating, managing, and consulting quick reference sheets (cheatsheets) directly from your terminal.

> 🌐 **[Versión en español / Spanish version](README.md)**

## 📑 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
  - [View a Cheatsheet](#view-a-cheatsheet)
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
- 📝 **Markdown Format**: Cheatsheets in Markdown format with elegant visualization using `glow`
- 🔄 **Live Aliases**: Create aliases that work both as documentation and real shell commands
- 📁 **Category Organization**: Interactive category selection when adding commands
- ⌨️ **Automatic Shortcut Detection**: Automatically formats keyboard combinations (Ctrl+C, Cmd+Shift+N, etc.)
- 🎨 **Smart Emojis**: Automatic emoji assignment based on command type
- 🔍 **Easy Search**: Lists all available cheatsheets and allows quick search
- 🔧 **Automatic Synchronization**: Aliases automatically sync with Fish shell

## 🔧 Requirements

- **Fish Shell**: The system is designed to work with Fish shell
- **Python 3**: For management scripts
- **glow**: For elegant Markdown visualization in terminal
  ```bash
  brew install glow
  ```
- **tree** (optional): For directory visualization aliases

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/jalmosquera/chatsManager.git ~/.cheatsheets
   ```

2. **Make scripts executable**:
   ```bash
   chmod +x ~/.cheatsheets/cs*
   chmod +x ~/.cheatsheets/*.py
   ```

3. **Configure Fish shell**:

   Copy or merge the aliases file content with your Fish configuration:
   ```bash
   # Create directory if it doesn't exist
   mkdir -p ~/.config/fish/conf.d/

   # Copy or merge aliases
   cp ~/.cheatsheets/fish_aliases_example.fish ~/.config/fish/conf.d/aliases.fish
   ```

4. **Reload Fish**:
   ```bash
   exec fish
   ```

5. **Verify installation**:
   ```bash
   cs
   ```

## 📖 Usage

### View a Cheatsheet

To view an existing cheatsheet:

```bash
cs <tool-name>
```

If you run `cs` without arguments, you'll see the main menu with all available commands and a list of existing cheatsheets.

**Examples**:
```bash
cs git          # View git cheatsheet
cs docker       # View docker cheatsheet
cs nvim         # View nvim cheatsheet
```

### Create New Cheatsheet

Create a new cheatsheet from scratch:

```bash
csnew <tool-name>
```

The system will ask you to:
1. Enter commands (format: `command - description`)
2. Press Ctrl+D when finished
3. It will automatically categorize and create the file

**Example**:
```bash
csnew kubectl
# Then enter:
kubectl get pods - List all pods
kubectl describe pod <name> - Show pod details
kubectl logs <pod> - Show pod logs
# Press Ctrl+D
```

### Add Commands

Add commands to an existing cheatsheet:

```bash
csadd <tool-name>
```

**Interactive flow**:
1. Enter commands (format: `command - description`)
2. Press Ctrl+D when finished
3. Select category for each command:
   - Choose an existing category (by number)
   - Or create a new category (option 0)

**Example**:
```bash
csadd git
# Enter:
git stash - Save changes temporarily
git stash pop - Restore saved changes
# Press Ctrl+D
# Then select category
```

### Edit Commands

Edit existing commands in a cheatsheet:

```bash
csedit <tool-name>
```

The system will display all numbered commands. Select the one you want to edit and modify the command and/or description.

**Example**:
```bash
csedit docker
# Select command number to edit
# Modify command and description
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

**Input format**:
```
name='command' - description
```

**Example**:
```bash
csalias
# Enter:
ll='ls -lah' - Detailed list with hidden files
gst='git status' - Git status
# Press Ctrl+D
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
├── cs                          # Main command: view cheatsheets
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
└── *.md                       # Cheatsheet files
```

## 🚀 Advanced Features

### Interactive Categorization

When adding commands with `csadd`, you can:
- View all existing categories with command counts
- Select an existing category by number
- Create a new category on the fly

### Automatic Keyboard Shortcut Formatting

The system automatically detects and formats keyboard combinations:

**Input**:
```
ctrl c - Copy
cmd shift n - New window
```

**Output**:
```
Ctrl + C - Copy
Cmd + Shift + N - New window
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

All cheatsheets are visualized with `glow`, which provides:
- Syntax highlighting
- Rendered Markdown format
- Colored code blocks
- Easy navigation

## 💡 Usage Examples

### Example 1: Create Docker Cheatsheet

```bash
# Create the cheatsheet
csnew docker

# Enter commands
docker ps - List running containers
docker images - List available images
docker run <image> - Run a container
docker stop <id> - Stop a container
docker rm <id> - Remove a container
# Press Ctrl+D

# View the result
cs docker
```

### Example 2: Add More Commands to Git

```bash
# Add commands
csadd git

# Enter new commands
git cherry-pick <commit> - Apply a specific commit
git rebase -i HEAD~3 - Interactive rebase last 3 commits
# Press Ctrl+D

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

# Enter aliases
gco='git checkout' - Switch branch
gpl='git pull' - Update branch
gps='git push' - Push changes
dc='docker-compose' - Docker compose shortcut
# Press Ctrl+D

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
