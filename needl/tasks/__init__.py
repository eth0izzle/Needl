import schedule
import functools
import needl


# todo: this is ugly, we need to automate finding and registering tasks
def register_tasks():
    import needl.tasks.alexa as alexa
    alexa.register()

    import needl.tasks.google as google
    google.register()

    import needl.tasks.dns as dns
    dns.register()


def start():
    schedule.run_pending()


def stop():
    schedule.clear()


# todo: maybe we can just wrap up the schedule class to include catching exceptions? then we don't need to decorate every task with this!
def catch_exceptions(job_func, cancel_on_failure=False):
    @functools.wraps(job_func)
    def wrapper(*args, **kwargs):
        try:
            return job_func(*args, **kwargs)
        except:
            import traceback
            needl.log.error('Task failed: %s', traceback.format_exc())

            if cancel_on_failure:
                return schedule.CancelJob

    return wrapper