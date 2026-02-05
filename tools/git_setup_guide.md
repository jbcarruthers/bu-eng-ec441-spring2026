# Git Setup Guide for EC 441

This guide will help you install Git and keep an up-to-date local copy of the course materials.

---

## Why Use Git?

Git allows you to:
- **Download all course materials** to your computer with a single command
- **Stay up-to-date** by pulling new lectures and updates as they're posted
- **Work offline** with all materials available locally
- **Track changes** to see what's new in each update

---

## Step 1: Install Git

### macOS

**Option 1: Using Homebrew (Recommended)**
```bash
# Install Homebrew first (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Git
brew install git
```

**Option 2: Install Xcode Command Line Tools**
```bash
xcode-select --install
```

**Option 3: Download the installer**
- Visit [git-scm.com/download/mac](https://git-scm.com/download/mac)
- Download and run the macOS installer

### Windows

**Option 1: Git for Windows (Recommended)**
1. Visit [git-scm.com/download/win](https://git-scm.com/download/win)
2. Download the Windows installer
3. Run the installer with default settings
4. Use "Git Bash" for running commands

**Option 2: GitHub Desktop (GUI)**
- Download from [desktop.github.com](https://desktop.github.com)
- Provides a graphical interface (no command line needed)

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install git
```

### Linux (Fedora/RHEL)

```bash
sudo dnf install git
```

### Verify Installation

After installation, verify Git is working:
```bash
git --version
```

You should see output like: `git version 2.x.x`

---

## Step 2: Clone the Course Repository

"Cloning" creates a local copy of the entire course repository on your computer.

### Using the Command Line

1. **Open a terminal** (Terminal on macOS/Linux, Git Bash on Windows)

2. **Navigate to where you want the course folder:**
   ```bash
   cd ~/Documents  # or wherever you keep your course materials
   ```

3. **Clone the repository:**
   ```bash
   git clone https://github.com/jbcarruthers/bu-eng-ec441-spring2026.git
   ```

4. **Enter the course directory:**
   ```bash
   cd bu-eng-ec441-spring2026
   ```

### Using GitHub Desktop (Windows/macOS)

1. Open GitHub Desktop
2. Click **File → Clone Repository**
3. Go to the **URL** tab
4. Enter: `https://github.com/jbcarruthers/bu-eng-ec441-spring2026`
5. Choose where to save it
6. Click **Clone**

---

## Step 3: Get Updates (Pull Changes)

Whenever new lectures or materials are posted, update your local copy:

### Using the Command Line

```bash
# Navigate to the course directory
cd ~/Documents/bu-eng-ec441-spring2026

# Pull the latest changes
git pull
```

**Output you'll see:**
```
From https://github.com/jbcarruthers/bu-eng-ec441-spring2026
 * branch            main       -> FETCH_HEAD
Updating abc1234..def5678
Fast-forward
 lecture04/lecture_04_notes.pdf | Binary file added
 lecture04/lecture_04_slides.pdf | Binary file added
 README.md | 15 +++++++++++++++
 3 files changed, 15 insertions(+)
```

### Using GitHub Desktop

1. Open GitHub Desktop
2. Select the `bu-eng-ec441-spring2026` repository
3. Click **Fetch origin** (top bar)
4. If updates are available, click **Pull origin**

---

## Quick Reference

### Most Common Commands

```bash
# Clone the repository (first time only)
git clone https://github.com/jbcarruthers/bu-eng-ec441-spring2026.git

# Update to latest version (run regularly)
cd bu-eng-ec441-spring2026
git pull

# Check status and see what changed
git status
git log --oneline -5  # See last 5 commits

# See what changed in the last update
git diff HEAD~1 HEAD --stat
```

### Recommended Workflow

1. **Before each class:** Run `git pull` to get the latest materials
2. **Weekly:** Check for updates even if no new lecture is announced
3. **Keep your workspace clean:** Don't modify files in the repository directly
   - If you want to experiment with Python scripts, copy them to a separate folder first

---

## Folder Structure

After cloning, your folder will look like:

```
bu-eng-ec441-spring2026/
├── README.md                  # Main page with all course links
├── lecture01/                 # Lecture 1 materials
│   └── lecture_01_intro.py
├── lecture02/                 # Lecture 2 materials
│   ├── lecture_02_notes.pdf
│   ├── lecture_02_slides.pdf
│   └── ...
├── lecture03/                 # Lecture 3 materials
├── lecture04/                 # Lecture 4 materials
└── tools/                     # Setup guides (like this one!)
    ├── git_setup_guide.md
    └── marimo_setup_guide.md
```

---

## Troubleshooting

### "git: command not found"

**Problem:** Git is not installed or not in your PATH.

**Solution:**
- Reinstall Git following Step 1
- On Windows, use "Git Bash" instead of Command Prompt
- Restart your terminal after installation

### "You have local changes that would be overwritten"

**Problem:** You modified files in the repository.

**Solution (if you want to keep your changes):**
```bash
# Move your changes to a different location
cp modified_file.py ~/Desktop/my_backup.py

# Discard local changes
git checkout -- modified_file.py

# Or reset everything (careful!)
git reset --hard HEAD

# Then pull
git pull
```

**Solution (if you don't care about your changes):**
```bash
git reset --hard HEAD
git pull
```

### "fatal: not a git repository"

**Problem:** You're not in the course directory.

**Solution:**
```bash
# Navigate to the correct directory
cd ~/Documents/bu-eng-ec441-spring2026

# Or find where you cloned it
cd ~/Desktop/bu-eng-ec441-spring2026
```

---

## Advanced Tips

### Create a Workspace Folder

Keep your experimental code separate from the course repository:

```bash
# Create a workspace folder for your experiments
mkdir ~/Documents/ec441-workspace
cd ~/Documents/ec441-workspace

# Copy a script to experiment with
cp ~/Documents/bu-eng-ec441-spring2026/lecture02/plot_entropy.py .

# Now modify plot_entropy.py in your workspace
# The original stays clean for git pull
```

### Set Up Aliases (Optional)

Make updating easier with shell aliases:

```bash
# Add to ~/.bashrc or ~/.zshrc
alias ec441-update="cd ~/Documents/bu-eng-ec441-spring2026 && git pull"

# Now just run:
ec441-update
```

### Get Notifications for Updates

**Option 1: Watch the repository on GitHub**
1. Visit [github.com/jbcarruthers/bu-eng-ec441-spring2026](https://github.com/jbcarruthers/bu-eng-ec441-spring2026)
2. Click **Watch** (top right)
3. Select **All Activity**

**Option 2: Check the README**
- The README shows "Last Updated: [date]" at the bottom
- Compare this to your local version after `git pull`

---

## Getting Help

### Git Documentation
- Official Git documentation: [git-scm.com/doc](https://git-scm.com/doc)
- GitHub's Git handbook: [guides.github.com/introduction/git-handbook](https://guides.github.com/introduction/git-handbook)

### Course Repository
- View online: [github.com/jbcarruthers/bu-eng-ec441-spring2026](https://github.com/jbcarruthers/bu-eng-ec441-spring2026)
- Course website: [jbcarruthers.github.io/bu-eng-ec441-spring2026](https://jbcarruthers.github.io/bu-eng-ec441-spring2026)

### Need More Help?
- Ask during office hours
- Post on the course discussion board
- Email the instructor

---

**Last Updated:** February 05, 2026
