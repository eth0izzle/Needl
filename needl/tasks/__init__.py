import glob
import imp
import os
import needl
import needl.schedule as schedule


def _discover_tasks():
    mydir = os.path.dirname(os.path.realpath(__file__))
    tasks = list(filter(lambda p: not os.path.basename(p).startswith('_'), glob.glob(os.path.join(mydir, '*.py'))))
    tasks = [(os.path.basename(os.path.splitext(task)[0]), task) for task in tasks]
    task_modules = [imp.load_source(task_name, task_path) for task_name, task_path in tasks]
    return task_modules


def register_tasks():
    for task in _discover_tasks():
        needl.log.debug('Loading task module {0}'.format(task.__name__))
        task.register()


def start():
    schedule.run_pending()


def stop():
    schedule.clear()
