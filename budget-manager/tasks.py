from invoke import task


# käynnistä sovellus
@task
def start(ctx):
    ctx.run("python3 src/index.py", pty=True)


# käynnistä sovellus kehitysympäristössä
# (kirjaa automaattisesti testikäyttäjän sisään)
@task
def start_dev(ctx):
    ctx.run("python3 src/index.py --autologin", pty=True)


# alusta tietokanta
@task
def init_db(ctx):
    ctx.run("python3 src/utils/initialize_database.py", pty=True)


# suorita testit src/tests kansiosta
@task
def test(ctx):
    ctx.run("pytest src", pty=True)


# koodin staattinen analysointi
@task
def lint(ctx):
    ctx.run("pylint src", pty=True)


# luo testien kattavuustulokset
@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)


# generoi testien haraumakattavuustulokset html-tiedostoon
@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=True)
