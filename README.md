# BOTTLEPLATE

**bottleplate** is a [bottle](http://bottlepy.org/docs/stable/) template for
`python` 3.3+ web applications or API servers. The files structure is very
similar to that of a [Ruby on Rails](http://rubyonrails.org/) application and
thus follows a model-view-controller (MVC) pattern.  It provides a simple way to
have development, test and production environments.  The structure for
functional and unit testing is also already in place.  It is very common for
`bottle` applications to define routes using the `bottle` route decorator.
However, I find it more convenient to have all routes defined in a file. This
template uses `bottleplate/config/routes.py` for that.  `SQLAlchemy` is used as
the object relational mapping (ORM) tool. It supports a broad range of database
backends (MySQL, PostgreSQL, SQLite, ...) and is usually the ORM of choice when
it comes to `python`. `alembic` is used to handle database migrations so it
takes care of the changes regarding the database schemas.

Sounds interesting? If you still have questions after having read this readme
file, feel free to contact me (either by email or IRC at #gwcomputingnet on
Freenode).

Need to have a look at a concrete examples? Have a look at
[pydeo](https://github.com/Rolinh/pydeo) to see a usage of this template for a
web application and [devmine-core](https://github.com/DevMine/devmine-core) to
see an example usage of this template for an API server.

## WHAT IS INCLUDED ?

Not much actually since this is not a framework but just a template. However, it
assumes some choices such as:

* [bottle](http://bottlepy.org/docs/stable/), the minimalist `python` web
  framework
* [SQLAlchemy](http://www.sqlalchemy.org/) as the ORM of choice
* [alembic](https://bitbucket.org/zzzeek/alembic) for handling database
  migrations
* [invoke](http://invoke.readthedocs.org/) as the task execution tool
* [nose](https://nose.readthedocs.org) for unit testing
* [WebTest](http://webtest.readthedocs.org/) for functional testing
* [pep8](http://pep8.readthedocs.org/) to check source code conformance to pep8
  style conventions
* [pyflakes](https://launchpad.net/pyflakes) to scan python source code for
  errors

Of course, nothing is written into stone and you can adapt the template to your
needs.

## FILES STRUCTURE AND ORGANIZATION

### ROOT DIRECTORY

The root directory contains two folders and some files:

* `alembic.ini.sample`: this is a template file for `alembic.ini`. It is copied
  to `alembic.ini` when `invoke setup` is run.
* `bottleplate`: this is where lays your bottle application.
* `env`: this folder is used for the python virtual environment.
* `requirements.txt`: this file defines the prerequisite packages to run the
  application.
* `requirements_dev.txt`: this file defines the prerequisite packages needed to
  develop the application or contribute to the project.
* `run.py`: this script is used to run the application.
* `tasks.py`: this is where you can define tasks. In some ways, this is similar
  to UNIX Makefiles. 

### THE APPLICATION DIRECTORY

* `app`: is used to organize your application contents such as controllers,
  static assets, models and views.
* `app/controllers`: this is where lay the application controllers.
* `app/helpers`: this is where helper classes are defined.
* `app/models`: this is where the application models are defined, using
  SQLAlchemy.
* `app/views`: this is where the HTML template files are. The basic
  `bottleplate` uses the `SimpleTemplate`, which is a very simple template
  engine shipped with `bottle` but of course, other template engines such as
  [Mako](http://www.makotemplates.org/) may be used instead.
* `app/views/layouts`: this is where you define the base layout templates to be
  used with views.
* `config`: the configuration files lay there.
* `config/environments`: this is where you define the specific environment
  settings for development, test or production.
* `config/routes.py`: this is where you define your routes and associate them to
  the appropriate controllers.
* `db`: if you use a SQLite database, you will find the database file here. 
  This folder is also used by `alembic` to store the database migration
  scripts.
* `lib`: if you need to write libraries, you would place them here.
* `log`: this is where the log files should go.
* `test`: this folder is meant to hold the test files.
* `test/functional`: this is where you write functional tests.
* `test/unit`: this is where you write unit tests.

## PREDEFINED TASKS

Some tasks are already defined in the `tasks.py` file.

* `set_settings`: this task is used to copy the default configuration file from
  from the templates. Basically, it copies the `settings-{environment}.py` file
  to `settings.py` where `{environment}` is one of `development | production |
  test`.
  Example:
  `invoke set_settings --environment=production`
* `test_func`: run the functional tests.
* `test_unit`: run the unit tests.
* `test`: run both the functional and unit tests.
* `setup`: copy the setting files and alembic sample files from their
  templates.
* `pep8`: check source code compliance to PEP8.
* `pyflakes`: check source code for errors.
* `check` run both the `pep8` and `pyflakes` tasks.
* `clean`: clean any python generated files and folders.
* `clean_env`: run the `clean` tasks and reinitializes the python environment.
* `rename`: this is supposed to be used only once. It rename the `bottleplate`
  directory and replaces `bottleplate` and `Bottleplate` names in python sources
  where appropriate. If you provide a name like this one: `my awesome app`,
  occurences of `bottleplate` will be replaced by `myawesomeapp` and occurences
  of `Bottleplate` by `MyAwesomeApp`.

## SETTING THE WHOLE THING

Make sure you have `python` 3.3 or above and `virtualenv`. Follow these steps:

* create the virtual environment: `virtualenv -p python3 env`
* activate the environment: `source env/bin/activate`
* install the required packages through `pip`:
  `pip install -r requirements.txt -r requirements_dev.txt`

From now on, you also need to choose which web server backend you are willing to
use with bottle. Have a look
[here](http://bottlepy.org/docs/stable/deployment.html#switching-the-server-backend)
for the full list of servers supported by `bottle` but keep in mind that not all
of them are compatible with `python3`.  Let's assume that your choice is
`cherrypy` (which is the server set by default in this template but you can
easily change that). Then, what you would do is make sure that in
`bottleplate/config/environments/(development|production|test).py`, `server` is
set to `cherrypy`: `server = 'cherrypy'`. Maybe, it is OK to keep the simple
`wsgiref` server for testing so you would simple set it to this `wsgiref` for
the test environment.
Of course, you then need to install the server backend: `pip install cherrypy`.

Now that you have a web server backend, you also need to choose a database
backend. Let's assume that you choose to use `sqlite` as test and
development databases and `postgresql` for production. The you need to change
`db_url` in the respective files like, for instance:

* `development.py`: `db_url = 'sqlite:///bottleplate/db/dev.db'`
* `production.py`: `db_url = 'postgresql://user:pass@localhost/dbname'`
* `test.py`: `db_url = 'sqlite:///:memory:'`

Of course, you might need additional packages to support the database backend.
For instance, if you use `postgresql`, you need `psycopg2`.

To use the migration, you also need to provide the appropriate database URL in
the `alembic.ini` file. Have a look at
[alembic documentation](http://alembic.readthedocs.org/) for more information.

Once all of this is setup, you can rename the template using this command:
`invoke rename --name='my awesome app name'`.
Of course, replace the name by the appropriate one. You may want to remove the
template under views if you are creating an API server.

## RUN IT

Considering all has been setup, you can run your application using this command:

    python run.py

You can now navigate to `http://localhost:8080` (considering you haven't changed
the default port) and see a sample home page.
