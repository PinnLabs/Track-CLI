import typer

from timecli.report import generate_report, show_log
from timecli.tracker import resume_task, start_task, status_task, stop_task

app = typer.Typer()


@app.command()
def start(project: str, tags: list[str] = typer.Option([])):
    """Start a new task"""
    start_task(project, tags)


@app.command()
def stop():
    """Stop the current task (equivalent to a simple stop)"""
    stop_task()


@app.command()
def status():
    """Show the current task status"""
    status_task()


@app.command()
def pause():
    stop_task()


@app.command()
def resume():
    resume_task()


@app.command()
def log():
    show_log()


@app.command()
def report():
    generate_report()


if __name__ == "__main__":
    app()
