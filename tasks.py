from shutil import copy
import sys

from invoke import task

# define projects directories
app_dir = 'bottleplate'
config_dir = app_dir + '/config'
test_dir = app_dir + '/test'
func_test_dir = test_dir + '/functional'
unit_test_dir = test_dir + '/unit'


@task
def set_settings(ctx, environment='production', nosetests=''):
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
def test_func(ctx, environment='test', nosetests='nosetests'):
    ctx.run(nosetests + ' -w ' + func_test_dir)


@task(set_settings)
def test_unit(ctx, environment='test', nosetests='nosetests'):
    ctx.run(nosetests + ' -w ' + unit_test_dir)


@task(set_settings, test_func, test_unit)
def test(ctx, environment='test', nosetests='nosetests'):
    pass


@task(set_settings)
def setup(ctx):
    src = 'alembic.ini.sample'
    dst = 'alembic.ini'
    print('Copying ' + src + ' to ' + dst)
    copy(src, dst)
    print('Done')


@task
def pep8(ctx):
    # ignore versions folder since migration scripts are auto-generated
    cmd = 'pep8 --exclude=app/db/versions/* run.py tasks.py ' + app_dir
    ctx.run(cmd)


@task
def pyflakes(ctx):
    cmd = 'pyflakes run.py tasks.py ' + app_dir
    ctx.run(cmd)


@task(pep8, pyflakes)
def check(ctx):
    pass


@task
def clean(ctx):
    ctx.run("find . -name '__pycache__' -exec rm -rf {} +")
    ctx.run("find . -name '*.pyc' -exec rm -f {} +")
    ctx.run("find . -name '*.pyo' -exec rm -f {} +")
    ctx.run("find . -name '*~' -exec rm -f {} +")
    ctx.run("find . -name '._*' -exec rm -f {} +")


@task(clean)
def clean_env(ctx):
    ctx.run('rm -r ./env && mkdir env && touch env/.keep')


@task
def rename(ctx, name=None):
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
