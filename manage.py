import csv
import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import blueprint

from app.src import create_app, db
from app.src.users.models import User
from app.src.states.models import State
from app.src.states.preloader import preload_data

app = create_app(os.getenv("APP_ENV", "dev"))
app.register_blueprint(blueprint)
app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command("db", MigrateCommand)


@manager.command
def load_initial_data():
    "Load initial data into database."
    with open("states.csv", "r") as states_file:
        preload_data(csv.reader(states_file))


@manager.command
def run():
    app.run(host="0.0.0.0")


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover("app/tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    manager.run()
