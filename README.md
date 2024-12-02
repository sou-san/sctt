# SpeedCubeTimer-TUI (sctt)

![sctt_screenshot](https://github.com/user-attachments/assets/d5e05bc7-801d-42ba-a8ee-752c30ad5313)

It's a TUI speed cube timer app. It can generate scrambles, measure time and display the cube's state as a cube net. It can also be used on the Linux console. (A color that cannot be displayed may change to a different color that can be displayed.)


## Usage
### Using uv
#### Linux
If you don't have uv installed, please install it.
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
---
**It must be run as root to detect keyboard events.**
```bash
uv tool install sctt
```
```bash
sudo -E $(which sctt)
```
or
```bash
sudo -E $(which uvx) sctt
```

#### Windows
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

## Screenshots
![sctt_screenshot_7x7x7](https://github.com/user-attachments/assets/4670e5ad-1732-4822-aa96-29d033697825)
![sctt_screenshot_4x4x4_user_input](https://github.com/user-attachments/assets/f53dd3d8-c732-45dd-835b-2f045c3bb6a4)
