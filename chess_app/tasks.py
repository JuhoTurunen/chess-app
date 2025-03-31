from invoke import task
from sys import platform

pty_option = False if platform == "win32" else True

@task
def start(ctx):
    ctx.run("python src/main.py", pty=pty_option)

@task
def test(ctx):
    ctx.run("pytest", pty=pty_option)

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest", pty=pty_option)

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=pty_option)