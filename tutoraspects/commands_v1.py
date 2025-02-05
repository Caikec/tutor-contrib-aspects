"""Aspects module for tutor v1 commands"""
from __future__ import annotations

import string

import click


@click.command()
@click.option("-n", "--num_batches", default=100)
@click.option("-s", "--batch_size", default=100)
def load_xapi_test_data(num_batches: int, batch_size: int) -> list[tuple[str, str]]:
    """
    Job that loads bogus test xAPI data to ClickHouse via Ralph.
    """
    return [
        (
            "aspects",
            "echo 'Making demo xapi script executable...' && "
            "chmod +x /app/aspects/scripts/clickhouse-demo-xapi-data.sh && "
            "echo 'Done. Running script...' && "
            f"bash /app/aspects/scripts/clickhouse-demo-xapi-data.sh {num_batches}"
            f" {batch_size} && "
            "echo 'Done!';",
        ),
    ]


# Ex: "tutor local do dbt "
@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "-c",
    "--command",
    default="run",
    type=click.UNPROCESSED,
    help="""The full dbt command to run configured ClickHouse database, wrapped in
         double quotes. The list of commands can be found in the CLI section here:
         https://docs.getdbt.com/reference/dbt-commands
         
         Examples: 
         
         tutor local do dbt -c "test"
         
         tutor local do dbt -c "run -m enrollments_by_day --threads 4"
         """,
)
def dbt(command: string) -> list[tuple[str, str]]:
    """
    Job that proxies dbt commands to a container which runs them against ClickHouse.
    """
    return [
        (
            "aspects",
            "echo 'Making dbt script executable...' && "
            "chmod +x /app/aspects/scripts/dbt.sh && "
            f"echo 'Running dbt {command}' && "
            f"bash /app/aspects/scripts/dbt.sh {command} && "
            "echo 'Done!';",
        ),
    ]


# Ex: "tutor local do alembic "
@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "-c",
    "--command",
    default="run",
    type=click.UNPROCESSED,
    help="""The full alembic command to run configured ClickHouse database, wrapped in
            double quotes. The list of commands can be found in the CLI section here:
            https://alembic.sqlalchemy.org/en/latest/cli.html#command-reference
            Examples:
            
            tutor local do alembic -c "current" # Show current revision
            tutor local do alembic -c "history" # Show revision history
            tutor local do alembic -c "revision --autogenerate -m 'Add new table'" # Create new revision
            tutor local do alembic -c "upgrade head" # Upgrade to latest migrations
            tutor local do alembic -c "downgrade base" # Downgrade to base migration
         """,
)
def alembic(command: string) -> list[tuple[str, str]]:
    """
    Job that proxies alembic commands to a container which runs them against ClickHouse.
    """
    return [
        (
            "aspects",
            "echo 'Making dbt script executable...' && "
            "chmod +x /app/aspects/scripts/dbt.sh && "
            f"bash /app/aspects/scripts/alembic.sh {command} && "
            "echo 'Done!';",
        ),
    ]


COMMANDS = (
    load_xapi_test_data,
    dbt,
    alembic,
)
