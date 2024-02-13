#!/usr/bin/env python3
"""
Just a nice looking banner for cheap_pie
"""
# this file is part of cheap_pie, a python tool for chip validation
# author: Marco Merlin
# email: marcomerli@gmail.com


def cp_banner():
    """
    Just a nice looking banner for cheap_pie
    """
    logo = (
        "        _..._                                                                     ",
        "    .-'_..._''.                                                                   ",
        "  .' .'      '.\  .              __.....__               _________   _...._       ",  # pylint: disable=W1401
        " / .'           .'|          .-''         '.             \        |.'      '-.    ",  # pylint: disable=W1401
        ". '            <  |         /     .-''`'-.  `.            \        .'```'.    '.  ",  # pylint: disable=W1401
        "| |             | |        /     /________\   \    __      \      |       \     \ ",  # pylint: disable=W1401
        "| |             | | .'''-. |                  | .:--.'.     |     |        |    | ",
        ". '             | |/.'''. \|    .-------------'/ |   \ |    |      \      /    .  ",  # pylint: disable=W1401
        " \ '.          .|  /    | | \    '-.____...---.`` __ | |    |     |\`'-.-'   .'   ",  # pylint: disable=W1401
        "  '. `._____.-'/| |     | |  `.             .'  .'.''| |    |     | '-....-'`     ",
        "    `-.______ / | |     | |    `''-...... -'   / /   | |_  .'     '.              ",
        "             `  | '.    | '.                   \ \._,\ '/'-----------'            ",  # pylint: disable=W1401
        "                '---'   '---'                   `--'  ``                          ",
        "                            ___                                                   ",
        "                         .'/   \                                                  ",  # pylint: disable=W1401
        "_________   _...._      / /     \      __.....__                                  ",  # pylint: disable=W1401
        "\        |.'      '-.   | |     |  .-''         '.                                ",  # pylint: disable=W1401
        " \        .'```'.    '. | |     | /     .-''`'-.  `.                              ",  # pylint: disable=W1401
        "  \      |       \     \|/`.   .'/     /________\   \                             ",  # pylint: disable=W1401
        "   |     |        |    | `.|   | |                  |                             ",
        "   |      \      /    .   ||___| \    .-------------'                             ",  # pylint: disable=W1401
        "   |     |\`'-.-'   .'    |/___/  \    '-.____...---.                             ",  # pylint: disable=W1401
        "   |     | '-....-'`      .'.--.   `.             .'                              ",
        "  .'     '.              | |    |    `''-...... -'                                ",
        "'-----------'            \_\    /                                                 ",  # pylint: disable=W1401
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
