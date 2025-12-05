### Installed Packages Export

Python script that exports all installed packages from your system and generates installation scripts for different distros.

### Features

- Export installed packages to JSON and TXT
- Categorized package lists (system, development, gaming, utils, apps, media)
- Alphabetically sorted output
- Generate installation scripts for Ubuntu, Arch, Fedora
- Package name mapping between distros

### Usage

**Basic export:**
```bash
python3 packages.py
```

**Generate installation script:**
```bash
# For specific distro
python3 packages.py --export-install ubuntu
python3 packages.py --export-install arch
python3 packages.py --export-install fedora

# For all distros at once
python3 packages.py --export-install all
```

### Output Files

- `installed_packages.json` — structured JSON with categories
- `installed_packages_list.txt` — human-readable list with timestamps
- `install_ubuntu.sh` — installation script for Ubuntu/Debian
- `install_arch.sh` — installation script for Arch Linux
- `install_fedora.sh` — installation script for Fedora/RHEL

### Example Output

```
=== Installed Packages Snapshot ===
Generated: 2025-12-05 14:30:00

[ SYSTEM ] (15 packages)
 - bluez
 - gdm3
 - mesa
 - vulkan-tools
 - xorg

[ DEVELOPMENT ] (12 packages)
 - build-essential
 - git
 - nodejs
 - python3
 - rust

[ GAMING ] (8 packages)
 - lutris
 - mangohud
 - steam
 - wine
...
```
