#!/usr/bin/env python3
import argparse

from alembic import command
from config import alembic_cfg


def upgrade() -> None:
    command.upgrade(alembic_cfg, 'head')


def downgrade() -> None:
    command.downgrade(alembic_cfg, '-1')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=[
            "upgrade",
            "downgrade",
        ],
    )

    args = parser.parse_args()

    if args.command == "upgrade":
        upgrade()
    elif args.command == "downgrade":
        downgrade()


if __name__ == "__main__":
    main()
