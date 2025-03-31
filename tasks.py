from invoke import task
from sys import platform, executable

pty_option = False if platform == "win32" else True

@task
def start(ctx):
    ctx.run(f"{executable} src/main.py", pty=pty_option)

@task
def test(ctx):
    ctx.run("pytest src/", pty=pty_option)

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src/", pty=pty_option)

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=pty_option)