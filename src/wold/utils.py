import os.path
import typer

class Utils():

    @staticmethod
    def readall(path):
        try:
            with open(path, 'r') as file:
                content = file.read()
        except Exception as e:
            Utils.log('fatal', f'failed to read file {path}', e)
        return content

    @staticmethod
    def log(level, msg, detail=None):
        typer.echo(typer.style(level, fg=typer.colors.RED) + ': ' + msg)
        if detail:
            typer.echo('\n' + detail)
        if level == 'fatal':
            exit(1)
        