from invoke import task


# käynnistä sovellus
@task
def start(ctx):
    ctx.run("python3 src/index.py", pty=True)


# suorita testit src/tests kansiosta
@task
def test(ctx):
    ctx.run("pytest src", pty=True)


# generoi testien haraumakattavuustulokset html-tiedostoon
@task
def coverage_report(ctx):
    ctx.run("coverage html", pty=True)
