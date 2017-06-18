import needl.schedule as schedule
import functools
import needl


# todo: this is ugly, we need to automate finding and registering tasks.. imp?
def register_tasks():
    import needl.tasks.alexa as alexa
    alexa.register()

    import needl.tasks.google as google
    google.register()

    import needl.tasks.dns as dns
    dns.register()

    import needl.tasks.twitter as twitter
    twitter.register()

    import needl.tasks.spotify as spotify
    spotify.register()


def start():
    schedule.run_pending()


def stop():
    schedule.clear()