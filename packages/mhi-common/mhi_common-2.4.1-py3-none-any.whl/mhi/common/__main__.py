"""
Common Library Version Report Application
"""

from . import version_msg


def main():
    """
    CLI main function - report package version
    """

    print(version_msg())


if __name__ == '__main__':
    main()
