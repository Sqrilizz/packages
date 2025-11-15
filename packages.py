import subprocess
import json

important_groups = {
    "system": [
        "xorg", "x11", "gnome", "kde-plasma-desktop", "kde-standard", "kde-full",
        "xfce4", "cinnamon", "lightdm", "gdm3", "sddm",
        "pipewire", "wireplumber", "pulseaudio", "alsa-utils",
        "mesa", "mesa-vulkan-drivers",
        "vulkan-tools", "vulkan-utils",
        "nvidia-driver", "firmware-linux",
        "linux-headers-generic", "bluez",
        "network-manager", "ufw", "apparmor"
    ],

    "development": [
        "python3", "python3-pip", "python3-venv", "build-essential",
        "gcc", "g++", "clang", "cmake", "make", "ninja-build",
        "git", "curl", "wget",
        "nodejs", "npm", "yarn", "pnpm",
        "openjdk-17-jdk", "openjdk-21-jdk",
        "cargo", "rustc", "python-is-python3"
    ],

    "gaming": [
        "steam", "heroic-games-launcher", "lutris",
        "mangohud", "gamescope", "goverlay",
        "protontricks", "gamemode",
        "wine", "wine64", "winetricks",
        "dxvk", "bottles", "itch"
    ],

    "utils": [
        "neofetch", "fastfetch", "btop", "htop",
        "kitty", "alacritty", "tilix",
        "nano", "vim", "neovim", "tmux",
        "unzip", "unrar", "p7zip-full",
        "gparted", "bleachbit", "timeshift",
        "thermald", "lm-sensors", "tlp", "powertop",
        "ethtool", "ntfs-3g", "fuse", "fuse3",
        "rsync", "ripgrep", "fd-find", "fzf",
        "zsh", "bat", "exa", "tree"
    ],

    "apps": [
        "discord", "spotify", "obs-studio",
        "blender", "gimp", "inkscape", "krita",
        "vlc", "qbittorrent", "telegram-desktop",
        "code", "codium",
        "android-tools-adb", "android-tools-fastboot"
    ]
}

def run(cmd):
    return subprocess.check_output(cmd, shell=True, text=True).strip().split("\n")

print("Collecting installed packages...")
installed = run("dpkg --get-selections | awk '{print $1}'")
installed_set = set(installed)

output = {cat: [] for cat in important_groups}
output["other"] = []

for category, pkgs in important_groups.items():
    for p in pkgs:
        if p in installed_set:
            output[category].append(p)

all_important = {p for group in important_groups.values() for p in group}

for p in installed_set:
    if p not in all_important:
        output["other"].append(p)

with open("installed_packages.json", "w") as f:
    json.dump(output, f, indent=4)

with open("installed_packages_list.txt", "w") as f:
    f.write("=== Installed Packages Snapshot ===\n\n")
    for category, pkgs in output.items():
        f.write(f"[ {category.upper()} ]\n")
        for p in sorted(pkgs):
            f.write(f" - {p}\n")
        f.write("\n")

print("Saved: installed_packages.json + installed_packages_list.txt")
