# Setting Up Marimo with uv

This guide walks you through setting up [Marimo](https://marimo.io/) notebooks using [uv](https://docs.astral.sh/uv/), a fast Python package installer and environment manager.

## Why uv?

`uv` is a modern Python package and project manager that's:
- **Fast**: 10-100x faster than pip
- **Reliable**: Written in Rust with deterministic dependency resolution
- **Simple**: Easy commands for managing virtual environments

## Prerequisites

- A computer running macOS, Linux, or Windows
- Basic familiarity with the command line/terminal

---

## Step 1: Install uv

Visit the [Astral uv website](https://docs.astral.sh/uv/) and follow the installation instructions for your platform.

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Verify installation:**
```bash
uv --version
```

---

## Step 2: Create a Virtual Environment

Create a new virtual environment with a specific Python version:

```bash
uv venv --python=3.14.2 myenv
```

**What this does:**
- Creates a new directory called `myenv` containing an isolated Python environment
- Uses Python 3.14.2 specifically (uv will download it if needed)
- Keeps your project dependencies separate from system Python

**Activate the environment:**

**macOS/Linux:**
```bash
source myenv/bin/activate
```

**Windows:**
```powershell
myenv\Scripts\activate
```

You should see `(myenv)` in your terminal prompt, indicating the environment is active.

---

## Step 3: Install Marimo and Useful Tools

With your virtual environment activated, install Marimo:

```bash
uv pip install marimo
```

**Optional: Install additional useful packages:**

```bash
# For data science and visualization
uv pip install numpy pandas matplotlib seaborn plotly

# For scientific computing
uv pip install scipy scikit-learn

# For network analysis (relevant to this course)
uv pip install requests beautifulsoup4 scapy

# All at once:
uv pip install marimo numpy pandas matplotlib seaborn plotly scipy scikit-learn requests beautifulsoup4
```

**Verify Marimo installation:**
```bash
marimo --version
```

---

## Step 4: Run Your First Marimo Notebook

**Create a new notebook:**
```bash
marimo edit my_notebook.py
```

This will:
1. Create a new file called `my_notebook.py`
2. Open your browser with the Marimo editor
3. Display an interactive notebook interface

**Run an existing notebook:**
```bash
marimo edit lecture_01_intro.py
```

**Run in view-only mode:**
```bash
marimo run lecture_01_intro.py
```

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `uv venv --python=3.14.2 myenv` | Create virtual environment |
| `source myenv/bin/activate` | Activate (macOS/Linux) |
| `myenv\Scripts\activate` | Activate (Windows) |
| `uv pip install marimo` | Install Marimo |
| `uv pip install <package>` | Install any package |
| `uv pip list` | List installed packages |
| `marimo edit notebook.py` | Create/edit notebook |
| `marimo run notebook.py` | Run in view mode |
| `deactivate` | Deactivate virtual environment |

---

## Tips

1. **Always activate your environment** before running Marimo or installing packages
2. **Create one environment per project** to avoid dependency conflicts
3. **Use `uv pip list`** to see what's installed in your current environment
4. **Deactivate** when done: just type `deactivate` in your terminal

---

## Troubleshooting

**"Command not found: uv"**
- Make sure uv is installed and in your PATH
- Try closing and reopening your terminal
- On macOS/Linux, you may need to add uv to your shell profile

**"Python version not found"**
- uv will automatically download the requested Python version
- Make sure you have an internet connection
- You can also use `--python=3.13` or `--python=3.12` if 3.14.2 isn't available

**"Marimo won't start"**
- Ensure your virtual environment is activated
- Try `which marimo` (macOS/Linux) or `where marimo` (Windows) to verify it's found
- Reinstall with `uv pip install --force-reinstall marimo`

---

## Additional Resources

- [uv Documentation](https://docs.astral.sh/uv/)
- [Marimo Documentation](https://docs.marimo.io/)
- [Python Virtual Environments Explained](https://realpython.com/python-virtual-environments-a-primer/)
