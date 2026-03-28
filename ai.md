# AI

## Gemini CLI

```bash
sudo npm install -g @google/gemini-cli
```

### Skills

You can explicitly invoke a skill by name using the `--skill` or `-s` flag with the `gemini` command:

```bash
gemini --skill <skill-name> "<your-prompt>"
```

Alternatively, if a skill is installed, Gemini CLI will automatically trigger it based on the description in the skill's `SKILL.md` file when your prompt matches the skill's purpose.

#### Listing and Reloading Skills

- **List installed skills**: `gemini skills list` (or `/skills list` in interactive mode)
- **Reload skills**: `/skills reload` (interactive mode only)

#### How to Trigger Skills

Skills are designed to be **automatic**. You don't usually need to call them by name; Gemini CLI will recognize the context of your request and activate the relevant skill.

**Example (Automatic):**
> "Add a note to linux.md about finding large files."
*Gemini sees the request involves notes and ~/GitRepos/book, then triggers the `note-taker` skill automatically.*

**Example (Manual/Explicit):**
If you want to ensure a specific skill is used, use the `-s` flag:

```bash
gemini -s note-taker "Add a section about kernel updates to linux.md"
```

## Obsidian

1. Recommended Method (Snap)
Run this command in your terminal:

```bash
sudo snap install obsidian --classic
```

2. Alternative Method (Official .deb package)
If you prefer standard system packages, you can download and install the .deb file:

```bash
# 1. Download the latest version (e.g., v1.6.7)
wget https://github.com/obsidianmd/obsidian-releases/releases/download/v1.6.7/obsidian_1.6.7_amd64.deb

# 2. Install the package
sudo apt install ./obsidian_1.6.7_amd64.deb
```

### Plugins

- Terminal
- Templater
- Calendar

### Themes

- Obsidianite
