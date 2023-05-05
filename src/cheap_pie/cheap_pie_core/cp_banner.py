#!/usr/bin/python3
"""
Just a nice looking banner for cheap_pie
"""
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

def cp_banner():
    """
    Just a nice looking banner for cheap_pie
    """
    logo = (
    "        _..._                                                                     ",
    "    .-'_..._''.                                                                   ",
    "  .' .'      '.\  .              __.....__               _________   _...._       ",
    " / .'           .'|          .-''         '.             \        |.'      '-.    ",
    ". '            <  |         /     .-''`'-.  `.            \        .'```'.    '.  ",
    "| |             | |        /     /________\   \    __      \      |       \     \ ",
    "| |             | | .'''-. |                  | .:--.'.     |     |        |    | ",
    ". '             | |/.'''. \|    .-------------'/ |   \ |    |      \      /    .  ",
    " \ '.          .|  /    | | \    '-.____...---.`` __ | |    |     |\`'-.-'   .'   ",
    "  '. `._____.-'/| |     | |  `.             .'  .'.''| |    |     | '-....-'`     ",
    "    `-.______ / | |     | |    `''-...... -'   / /   | |_  .'     '.              ",
    "             `  | '.    | '.                   \ \._,\ '/'-----------'            ",
    "                '---'   '---'                   `--'  ``                          ",
    "                            ___                                                   ",
    "                         .'/   \                                                  ",
    "_________   _...._      / /     \      __.....__                                  ",
    "\        |.'      '-.   | |     |  .-''         '.                                ",
    " \        .'```'.    '. | |     | /     .-''`'-.  `.                              ",
    "  \      |       \     \|/`.   .'/     /________\   \                             ",
    "   |     |        |    | `.|   | |                  |                             ",
    "   |      \      /    .   ||___| \    .-------------'                             ",
    "   |     |\`'-.-'   .'    |/___/  \    '-.____...---.                             ",
    "   |     | '-....-'`      .'.--.   `.             .'                              ",
    "  .'     '.              | |    |    `''-...... -'                                ",
    "'-----------'            \_\    /                                                 ", 
    "                          `''--'                                                  ",
    "A python tool for chip validation by Marco Merlin\n"
    )
    for line in logo:
        print(line)

def test_banner():
    """
    Test function for cheap_pie banner
    """
    return cp_banner()

if __name__ == '__main__':
    cp_banner()
