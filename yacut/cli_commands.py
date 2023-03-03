import click

from . import app, db


@app.cli.command('create_db')
def load_opinions_command():
    """Функция создания пустой БД (если она отсутствует)."""
    db.create_all()
    click.echo("Создана БД")


@app.cli.command('flush_db')
def load_opinions_command():
    """Очистка всех записей ДБ."""
    db.drop_all()
    db.create_all()
    click.echo("БД очищена")
