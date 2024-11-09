# SpeedCubeTimer-TUI (sctt)

![sctt_screenshot](https://github.com/user-attachments/assets/02c1d3c7-8ca8-4a6d-9970-903970fb2e07)

It's a TUI speed cube timer app. It can generate scrambles, measure time and display the cube's state as a cube net. It can also be used on the Linux console. (A color that cannot be displayed may change to a different color that can be displayed.)

**It must be run as root to detect keyboard events.**

## Usage
### Using uv
If you don't have uv installed, please install it.
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
---
```bash
uv tool install sctt
```
```bash
sudo -E $(which sctt)
```

### Using pipx
If you don't have pipx installed, please install it.
```bash
sudo apt update && sudo apt install pipx
```
---
```bash
pipx install sctt
```
```bash
sudo -E $(which sctt)
```
