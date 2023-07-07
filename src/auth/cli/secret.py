import secrets

import click


def create_secret() -> None:
    click.echo(secrets.token_urlsafe(32))
