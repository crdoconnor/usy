from hitchstory import StoryCollection, StorySchema, BaseEngine, validate, exceptions
from hitchrun import Path, hitch_maintenance, expected
from commandlib import Command
from pathquery import pathq
from strictyaml import MapPattern, Str
from commandlib import python
import hitchpython
import hitchserve
import strictyaml
import hitchtest


KEYPATH = Path(__file__).abspath().dirname()
git = Command("git").in_dir(KEYPATH.parent)


class Paths(object):
    def __init__(self, keypath):
        self.keypath = keypath
        self.project = keypath.parent
        self.state = keypath.parent.joinpath("state")


class Engine(BaseEngine):
    schema = StorySchema(
        preconditions={"files": MapPattern(Str(), Str())},
    )

    def __init__(self, keypath):
        self.path = Paths(keypath)

    def set_up(self):
        if self.path.state.exists():
            self.path.state.rmtree(ignore_errors=True)
        self.path.state.mkdir()

        for filename, text in self.preconditions.get("files", {}).items():
            filepath = self.path.state.joinpath(filename)
            if not filepath.dirname().exists():
                filepath.dirname().mkdir()
            filepath.write_text(str(text))

        self.path.project.joinpath("usy.py").copy(self.path.state)

        self.python_package = hitchpython.PythonPackage(
            self.preconditions.get('python_version', '3.5.0')
        )
        self.python_package.build()

        self.pip = self.python_package.cmd.pip
        self.python = self.python_package.cmd.python

        with hitchtest.monitor([self.path.keypath.joinpath("debugrequirements.txt")]) as changed:
            if changed:
                self.pip("install", "-r", "debugrequirements.txt").in_dir(self.path.keypath).run()

        self.services = hitchserve.ServiceBundle(
            str(self.path.project),
            startup_timeout=8.0,
            shutdown_timeout=1.0
        )


        self.services['IPython'] = hitchpython.IPythonKernelService(self.python_package)

        self.services.startup(interactive=False)
        self.ipython_kernel_filename = self.services['IPython'].wait_and_get_ipykernel_filename()
        self.ipython_step_library = hitchpython.IPythonStepLibrary()
        self.ipython_step_library.startup_connection(self.ipython_kernel_filename)

        self.run("import os")
        self.run("os.chdir('{}')".format(self.path.state))

    def run(self, command):
        self.ipython_step_library.run(command)

    def assert_true(self, command):
        self.ipython_step_library.assert_true(command)

    def assert_exception(self, command, exception):
        self.ipython_step_library.assert_exception(command, exception)


    def tear_down(self):
        """Clean out the state directory."""
        try:
            self.shutdown_connection()
        except:
            pass
        if hasattr(self, 'services'):
            self.services.shutdown()


@expected(strictyaml.exceptions.YAMLValidationError)
@expected(exceptions.HitchStoryException)
def test(*words):
    """
    Run test with words.
    """
    STORY_COLLECTION = StoryCollection(pathq(KEYPATH).ext("story"), Engine(KEYPATH))
    print(STORY_COLLECTION.shortcut(*words).play().report())


def ci():
    """
    Run all stories.
    """
    lint()
    print(STORY_COLLECTION.ordered_by_name().play().report())


def hitch(*args):
    """
    Use 'h hitch --help' to get help on these commands.
    """
    hitch_maintenance(*args)


def lint():
    """
    Lint all code.
    """
    python("-m", "flake8")(
        KEYPATH.parent.joinpath("usy.py"),
        "--max-line-length=100",
        "--exclude=__init__.py",
    ).run()
    python("-m", "flake8")(
        KEYPATH.joinpath("key.py"),
        "--max-line-length=100",
        "--exclude=__init__.py",
    ).run()
    print("Lint success!")
