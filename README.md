![Python version](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue.svg)
![PyPi version](https://img.shields.io/badge/pypi%20package-v0.3.1-green.svg)
![OS support](https://img.shields.io/badge/OS-Linux%20%7C%20Windows-red.svg)

# SpeedCubeTimer-TUI (sctt)

![sctt_screenshot](https://github.com/user-attachments/assets/c2d3a16d-215f-4bb3-af2f-b39d0edffb59)

It's a TUI speed cube timer app. It can generate scrambles, measure time, save solve data, statistics feature, and display the cube's state as a cube net.

It can also be used on the Linux console. (A color that cannot be displayed may change to a different color that can be displayed.)

## Usage

### Linux

If you don't have uv installed, please install it.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

**It must be run as root to detect keyboard events.**

When run as root, `__pycache__` will be owned by root and cannot be updated or uninstalled as a normal user.
To prevent this, compile in advance `__pycache__` using the `--compile-bytecode` option so that the owner of `__pycache__` is the normal user.

```bash
uv tool install --compile-bytecode sctt
```

```bash
sudo -E $(which sctt)
```

or

```bash
sudo -E $(which uvx) -n sctt
```

### Windows

If you don't have uv installed, please install it.

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

```powershell
uv tool install sctt
```

```powershell
sctt
```

or

```powershell
uvx sctt
```

#### WSL2

sctt cannot be run because WSL2 cannot detect key release events.

Instead, run it via powershell as follows.

```bash
powershell.exe sctt
```

## Development

```bash
git clone https://github.com/sou-san/sctt
```

```bash
cd sctt
```

---

### Linux

```bash
uv sync --compile-bytecode
```

```bash
uv run pre-commit install
```

```bash
sudo -E $(which uv) run textual run --dev src/sctt/__main__.py
```

### Windows

```powershell
uv run textual run --dev .\src\sctt\__main__.py
```

## Screenshots

![session manager](https://github.com/user-attachments/assets/bfcd5fe4-2f10-4aab-be52-4fc9dd02fc84)

![time](https://github.com/user-attachments/assets/df505f8a-3d72-4d9d-88a0-ed8058640fba)

![time +2 penalty](https://github.com/user-attachments/assets/88166632-ab7d-4a0f-8de5-3b142abe7356)

![time DNF penalty](https://github.com/user-attachments/assets/bd4832c8-7863-4637-a2b3-21b89df7d5f6)

![ao5](https://github.com/user-attachments/assets/593fbf5b-0464-4d29-9753-334b86d69371)

![ao12](https://github.com/user-attachments/assets/97977e9a-1efa-4ae3-aa7d-67c2ded612ed)

![scramble option](https://github.com/user-attachments/assets/c67fa026-375e-4d59-9bf0-a31e4294dc83)

![input scramble](https://github.com/user-attachments/assets/071bfecc-e699-4af3-93d5-5c74f9f0763f)

![scramble events](https://github.com/user-attachments/assets/8f9cbce2-0b86-4e77-ae83-c0e254d5c5fa)

![7x7x7 scramble](https://github.com/user-attachments/assets/b68c7169-4a00-484e-ad93-bced436d29fc)
