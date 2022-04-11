# copyright: (c) 2020 by Jesse Johnson.
# license: LGPL-3.0, see LICENSE.md for more details.
"""Simple package manager for GitHub releases."""

from argufy import Parser, __version__

from . import cli


def main() -> None:
    """Proide main function for CLI."""
    parser = Parser(
        version=__version__,
        # use_module_args=True,
        main_args_builder={
            'module': 'proman_github',
            'function': 'get_package_manager',
            'instance': 'package_manager',
            'variables': {'token': None},
        },
    )
    parser.add_commands(cli)
    parser.dispatch()


if __name__ == '__main__':
    main()
