# Needl

**Take back your privacy. Lose yourself in the haystack.**

Your ISP is most likely tracking your browsing habits and selling them to marketing agencies (albeit anonymised). Or worse, making your browsing history available to law enforcement at the hint of a Subpoena. **Needl** will generate random Internet traffic in an attempt to conceal your legitimate traffic, essentially making your data the **Needl**e in the haystack and thus harder to find. The goal is to make it harder for your ISP, government, etc to track your browsing history and habits.

It's not perfect. But it's a start. Have an idea? [Get involved](CONTRIBUTING.md)!

![Demo](https://pbs.twimg.com/media/CxeQsH5XAAAp_vN.jpg:large)

Implemented modules:

- **Google**: generates a random search string, searches Google and clicks on a random result.
- **Alexa**: visits a website from the Alexa Top 1 Million list. (**warning**: contains a lot of porn websites)
- **Twitter**: generates a popular English name and visits their profile; performs random keyword searches
- **DNS**: produces random DNS queries from the Alexa Top 1 Million list.

Module ideas:

- **WhatsApp**
- **Spotify**
- **Facebook Messenger**

## Installation

Needl will work on pretty much any Linux system with Python 3.0+. A simple `sudo apt-get install python3 python3-pip` (replace `apt-get` with your OS' package manager) will take all of your troubles away.

You can then install Needl in 4 simple steps:

1. `cd /opt`
2. `git clone https://github.com/eth0izzle/needl.git`
3. `sudo make install` or `sudo pip3 install -r requirements.txt`
4. `python3 needl.py --daemon` _(todo: [write service scripts](https://github.com/eth0izzle/needl/issues/1))_

## Usage

Needl runs as a daemon and will happily sit in the background chomping away 24/7, 365. Each module (task) has scheduled actions, for example random DNS queries will happen every 1 to 3 minutes. You can configure the intervals within `./data/settings.yaml`.

    usage: needl.py [-h] [--datadir DATADIR] [-d] [-v] [--logfile LOGFILE]
                    [--pidfile PIDFILE]
    
    Take back your privacy. Lose yourself in the haystack.
    
    optional arguments:
      -h, --help         show this help message and exit
      --datadir DATADIR  Data directory
      -d, --daemon       Run as a deamon
      -v, --verbose      Increase logging
      --logfile LOGFILE  Log to this file. Default is stdout.
      --pidfile PIDFILE  Save process PID to this file. Default is /tmp/needl.pid.
                         Only valid when running as a daemon.

## F.A.Qs

1. **Why not just use a VPN/Tor?**
And you should! Needl does not protect your legitimate traffic in any way. It simply generates more.

2. **By using Needl will my legitimate traffic be hidden/protected/safe?**
No. This isn't the goal of Needl. It's purpose is to generate more traffic to make it *harder* to identify your legitimate traffic. There's no evidence to suggest this actually works - it's a proof of concept.

3. **Can [insert service here] differentiate between Needl and my legitimate requests?**
In theory, yes. [insert service here] can track you with Cookies, Session data or *algorithms*. Needl will tackle this in the future.

4. **Where are your tests?!?**
Submit a pull request. _Please_.

## Contributing

Check out the [issue tracker](https://github.com/eth0izzle/needl/issues) and see what tickles your fancy.

1. Fork it, baby!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

## History

**v0.1**
First release

## License

MIT. See LICENSE
