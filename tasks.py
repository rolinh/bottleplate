from shutil import copy
import sys

from invoke import task, call

# define projects directories
app_dir = 'bottleplate'
config_dir = app_dir + '/config'
test_dir = app_dir + '/test'
func_test_dir = test_dir + '/functional'
unit_test_dir = test_dir + '/unit'


@task
def dev(ctx):
    """Run the application (use when developing)."""
    ctx.run("python run.py")


@task(help={'environment': "One of 'production', 'development' or 'test'."})
def set_settings(ctx, environment='production'):
    """Copy the default configuration file from the template."""
    if environment not in ['production', 'development', 'test']:
        print('Error: ' + environment + ' is not a valid parameter',
              file=sys.stderr)
        exit(1)

    src = config_dir + '/settings-' + environment + '.py.sample'
    dst = config_dir + '/settings.py'
    print('Copying ' + src + ' to ' + dst)
    copy(src, dst)
    print('Done')


@task(set_settings)
def setup(ctx):
    """Copy the configuration and alembic sample files from their template."""
    src = 'alembic.ini.sample'
    dst = 'alembic.ini'
    print('Copying ' + src + ' to ' + dst)
    copy(src, dst)
    print('Done')


@task(pre=[call(set_settings, environment='test')])
def test_func(ctx):
    """Run the functional tests."""
    ctx.run('nosetests -w ' + func_test_dir)


@task(pre=[call(set_settings, environment='test')])
def test_unit(ctx):
    """Run the unit tests."""
    ctx.run('nosetests -w ' + unit_test_dir)


@task(test_func, test_unit)
def test(ctx):
    """Run the tests (functional and unit)."""
    pass


@task
def pep8(ctx):
    """Check source code compliance to PEP8."""
    # ignore versions folder since migration scripts are auto-generated
    ctx.run('pep8 --exclude=app/db/versions/* run.py tasks.py ' + app_dir)


@task
def flake8(ctx):
    """Check source code for errors."""
    ctx.run('flake8 run.py tasks.py ' + app_dir)


@task(pep8, flake8)
def check(ctx):
    """Run the pep8 and flake8 tasks."""
    pass


@task
def clean(ctx):
    """Clean any python generated files and folders."""
    ctx.run("find . -name '__pycache__' -exec rm -rf {} +")
    ctx.run("find . -name '*.pyc' -exec rm -f {} +")
    ctx.run("find . -name '*.pyo' -exec rm -f {} +")
    ctx.run("find . -name '*~' -exec rm -f {} +")
    ctx.run("find . -name '._*' -exec rm -f {} +")


@task(clean)
def clean_env(ctx):
    """Run the clean task and clean the python virtual environmnent."""
    ctx.run('rm -r ./env && mkdir env && touch env/.keep')


@task(help={'name': "A new name for your awesome app."})
def rename(ctx, name=None):
    """
    Rename the 'bottleplate' application to whichever name of your
    choosing.
    """
    if name is None:
        print('Please, provide a name for your application. '
              'Example: invoke rename --name=\'my awesome app\'')
    else:
        app_name = name.lower().replace(' ', '')
        class_name = name.title().replace(' ', '')

        rename_app_name = "sed -i 's/bottleplate/" + app_name + "/g'"
        rename_class_name = "sed -i 's/Bottleplate/" + class_name + "/g'"

        pyfiles = "find bottleplate -type f -name '*.py' | xargs "
        ctx.run(pyfiles + rename_app_name)
        ctx.run(pyfiles + rename_class_name)

        ctx.run(rename_app_name + " run.py tasks.py alembic.ini.sample")
        ctx.run(rename_class_name + " run.py tasks.py")

        ctx.run('mv -v bottleplate ' + app_name)
