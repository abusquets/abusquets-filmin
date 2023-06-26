from click.testing import CliRunner

from manage import cli_app


def test_main() -> None:
    runner = CliRunner()
    result = runner.invoke(cli_app, ['test'])
    assert 'Manage is working fine' in result.stdout
