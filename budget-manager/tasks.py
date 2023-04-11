from invoke import task


# käynnistä sovellus
@task
def start(ctx):
    ctx.run("python3 src/index.py", pty=True)


# suorita testit src/tests kansiosta
@task
def test(ctx):
    ctx.run("pytest src", pty=True)


# luo testien kattavuustulokset
@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest", pty=True)


# generoi testien haraumakattavuustulokset html-tiedostoon
@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=True)
