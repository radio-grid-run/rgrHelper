import click
from click.testing import CliRunner
from rgr_helper import cli


class TestCommandsHelps:

    def test_rgrHelper_help(self):

        runner = CliRunner()
        result = runner.invoke(cli, ' --help')
        assert result.exit_code == 0
        assert "--help         Show this message and exit." in result.output

    def test_testw3w_help(self):

        runner = CliRunner()
        result = runner.invoke(cli, 'testw3w --help')
        assert result.exit_code == 0
        assert "Sending a API call to w3w to check" in result.output

    def test_rgrHelper_testaera(self):

        runner = CliRunner()
        result = runner.invoke(cli, 'testarea')
        assert result.exit_code == 0
        assert "253239.42144594956" in result.output