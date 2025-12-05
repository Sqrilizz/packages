import subprocess
import json
import argparse
from datetime import datetime

important_groups = {
    "system": [
        "xorg", "x11-xserver-utils", "gnome", "gnome-shell", "gnome-tweaks",
        "kde-plasma-desktop", "kde-standard", "kde-full", "plasma-desktop",
        "xfce4", "xfce4-goodies", "cinnamon", "mate-desktop-environment",
        "lightdm", "gdm3", "sddm", "ly",
        "pipewire", "pipewire-pulse", "wireplumber", "pulseaudio", "alsa-utils",
        "mesa", "mesa-vulkan-drivers", "mesa-utils",
        "vulkan-tools", "vulkan-utils", "vulkan-icd-loader",
        "nvidia-driver", "nvidia-utils", "nvidia-settings",
        "firmware-linux", "firmware-linux-nonfree",
        "linux-headers-generic", "linux-headers", "linux-firmware",
        "bluez", "bluez-utils", "bluetooth",
        "network-manager", "networkmanager", "nm-connection-editor",
        "ufw", "firewalld", "apparmor", "systemd"
    ],

    "development": [
        "python3", "python3-pip", "python3-venv", "python-pipx",
        "build-essential", "base-devel",
        "gcc", "g++", "clang", "llvm", "cmake", "make", "ninja-build", "meson",
        "git", "git-lfs", "curl", "wget", "openssh",
        "nodejs", "npm", "yarn", "pnpm", "bun",
        "openjdk-17-jdk", "openjdk-21-jdk", "jdk-openjdk",
        "cargo", "rustc", "rust", "rustup",
        "go", "golang", "ruby", "php",
        "docker", "docker-compose", "podman",
        "python-is-python3", "gdb", "valgrind", "strace"
    ],

    "gaming": [
        "steam", "steam-native-runtime",
        "heroic-games-launcher", "lutris", "bottles",
        "mangohud", "goverlay", "gamescope", "gamemode", "lib32-gamemode",
        "protontricks", "protonup-qt",
        "wine", "wine64", "wine-staging", "winetricks",
        "dxvk", "vkd3d", "itch",
        "retroarch", "pcsx2", "dolphin-emu", "rpcs3"
    ],

    "utils": [
        "neofetch", "fastfetch", "screenfetch", "btop", "htop", "gtop", "bottom",
        "kitty", "alacritty", "tilix", "terminator", "wezterm",
        "nano", "vim", "neovim", "emacs", "micro", "tmux", "screen",
        "unzip", "zip", "unrar", "rar", "p7zip-full", "p7zip", "tar",
        "gparted", "gnome-disk-utility", "bleachbit", "timeshift",
        "thermald", "lm-sensors", "tlp", "tlp-rdw", "powertop", "auto-cpufreq",
        "ethtool", "ntfs-3g", "exfat-fuse", "exfat-utils", "fuse", "fuse3",
        "rsync", "rclone", "syncthing",
        "ripgrep", "fd-find", "fzf", "ack", "ag",
        "zsh", "fish", "bash-completion", "zsh-autosuggestions", "zsh-syntax-highlighting",
        "bat", "exa", "eza", "lsd", "tree", "duf", "dust", "procs",
        "jq", "yq", "httpie", "ncdu", "ranger", "nnn", "mc"
    ],

    "apps": [
        "discord", "spotify", "spotify-launcher", "obs-studio",
        "firefox", "chromium", "google-chrome-stable", "brave-browser",
        "thunderbird", "evolution", "geary",
        "blender", "gimp", "inkscape", "krita", "darktable", "rawtherapee",
        "kdenlive", "shotcut", "davinci-resolve",
        "vlc", "mpv", "celluloid",
        "qbittorrent", "transmission", "deluge",
        "telegram-desktop", "signal-desktop", "slack", "zoom",
        "code", "vscodium", "codium", "sublime-text", "atom",
        "libreoffice", "onlyoffice-desktopeditors",
        "android-tools-adb", "android-tools-fastboot", "android-file-transfer",
        "flameshot", "spectacle", "gnome-screenshot", "ksnip"
    ],

    "media": [
        "ffmpeg", "imagemagick", "graphicsmagick",
        "audacity", "ardour", "lmms",
        "handbrake", "mkvtoolnix", "mediainfo",
        "youtube-dl", "yt-dlp",
        "calibre", "foliate", "okular", "evince"
    ]
}

package_mappings = {
    "ubuntu": {
        "base-devel": "build-essential",
        "networkmanager": "network-manager",
        "bluez-utils": "bluez",
        "jdk-openjdk": "openjdk-17-jdk",
        "rust": "cargo",
        "golang": "golang-go",
        "eza": "exa",
        "lsd": "lsd",
    },
    "arch": {
        "build-essential": "base-devel",
        "network-manager": "networkmanager",
        "bluez": "bluez-utils",
        "openjdk-17-jdk": "jdk-openjdk",
        "cargo": "rust",
        "golang-go": "go",
        "python3-pip": "python-pip",
        "python3-venv": "python-virtualenv",
    },
    "fedora": {
        "build-essential": "@development-tools",
        "network-manager": "NetworkManager",
        "bluez": "bluez",
        "openjdk-17-jdk": "java-17-openjdk-devel",
        "cargo": "rust cargo",
        "golang-go": "golang",
    }
}

def run(cmd):
    return subprocess.check_output(cmd, shell=True, text=True).strip().split("\n")

def collect_packages():
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

    # Sort all categories
    for category in output:
        output[category] = sorted(output[category])

    return output

def save_json(output):
    with open("installed_packages.json", "w") as f:
        json.dump(output, f, indent=4)
    print("✓ Saved: installed_packages.json")

def save_txt(output):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("installed_packages_list.txt", "w") as f:
        f.write(f"=== Installed Packages Snapshot ===\n")
        f.write(f"Generated: {timestamp}\n\n")
        for category, pkgs in output.items():
            if pkgs:
                f.write(f"[ {category.upper()} ] ({len(pkgs)} packages)\n")
                for p in pkgs:
                    f.write(f" - {p}\n")
                f.write("\n")
    print("✓ Saved: installed_packages_list.txt")

def generate_install_commands(output, distro):
    mapping = package_mappings.get(distro, {})
    
    commands = {
        "ubuntu": "sudo apt install -y",
        "arch": "sudo pacman -S --needed",
        "fedora": "sudo dnf install -y"
    }
    
    base_cmd = commands.get(distro, "sudo apt install -y")
    filename = f"install_{distro}.sh"
    
    with open(filename, "w") as f:
        f.write(f"#!/bin/bash\n")
        f.write(f"# Installation script for {distro.upper()}\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for category, pkgs in output.items():
            if pkgs and category != "other":
                f.write(f"\n# {category.upper()}\n")
                mapped_pkgs = []
                for p in pkgs:
                    mapped_pkgs.append(mapping.get(p, p))
                
                pkg_list = " ".join(mapped_pkgs)
                f.write(f"{base_cmd} {pkg_list}\n")
    
    print(f"✓ Saved: {filename}")

def main():
    parser = argparse.ArgumentParser(description="Export installed packages")
    parser.add_argument("--export-install", choices=["ubuntu", "arch", "fedora", "all"],
                        help="Generate installation script for distro")
    args = parser.parse_args()

    output = collect_packages()
    save_json(output)
    save_txt(output)

    if args.export_install:
        if args.export_install == "all":
            for distro in ["ubuntu", "arch", "fedora"]:
                generate_install_commands(output, distro)
        else:
            generate_install_commands(output, args.export_install)

if __name__ == "__main__":
    main()
