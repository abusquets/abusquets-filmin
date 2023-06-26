from click.testing import CliRunner

from manage import cli_app


runner = CliRunner()


def test_create_admin() -> None:
    result = runner.invoke(cli_app, ['create-admin', 'camila@gmail.com', 'Camila'], input='Berlin123\n')
    assert result.exit_code == 0
    expected = 'Password: Berlin123\nThe User Camila, camila@gmail.com has been created\n'
    assert result.output == expected
