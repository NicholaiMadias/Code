#!/usr/bin/env python3
"""Reverse the combined command-line text, matching the other Nexus Toolbox ports."""
import sys

def main() -> None:
    text = " ".join(sys.argv[1:])
    print(text[::-1], end="\n" if text else "")

if __name__ == "__main__":
    main()
