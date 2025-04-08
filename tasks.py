from sys import platform, executable
from invoke import task


PTY_OPTION = platform != "win32"


@task
def start(ctx):
    ctx.run(f"{executable} src/main.py", pty=PTY_OPTION)


@task
def test(ctx):
    ctx.run("pytest src/", pty=PTY_OPTION)


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src/", pty=PTY_OPTION)


@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=PTY_OPTION)


@task
def lint(ctx):
    ctx.run("pylint src/", pty=PTY_OPTION)
