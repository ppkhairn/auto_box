# Project Setup Guide 

## 1. Install `uv`

```bash
pip install uv
```

Verify installation:

```bash
uv --version
```

---

## 2. Create a Virtual Environment

From the root of the repository:

```bash
uv venv .venv
```

This will create a virtual environment in the `.venv/` directory.

---

## 3. Activate the Virtual Environment

On macOS / Linux:

```bash
source .venv/bin/activate
```

You should now see `(.venv)` in your terminal prompt.

---

## 4. Install Project Dependencies

Sync dependencies from the lock file:

```bash
uv sync
```

This will install all required packages into the virtual environment.

---

## Managing Dependencies

### View installed packages
```bash
uv pip list
```

### Add a new package
```bash
uv add <PACKAGE-NAME>
```

### Remove a package
```bash
uv remove <PACKAGE-NAME>
```

---

## Deactivating the Environment

When you're done:

```bash
source deactivate
```
