# Needl

**Take back your privacy. Lose yourself in the haystack.**

Needl will generate legitimate random Internet traffic in order to conceal your "real" traffic. The goal is to make it harder for your ISP, government, etc to track your browsing habits.

Currently supported modules:

- **Google**: generates random search strings, searches Google and clicks on a random result.
- **Alexa**: visits a website from the Alexa Top 1 Million list.
- **DNS**: produces random DNS queries.

## Installation

1. `cd /opt`
2. `git clone https://github.com/eth0izzle/needl.git`
3. `make install` or `pip install -r requirements.txt`
4. `python needl.py &` _(todo: write init scripts)_

## Usage

Needl runs as a daemon and will happily sit in the background chomping away 24/7, 365. Each module (task) has scheduled actions, for example random DNS queries will happen every 60 seconds. You can configure the intervals within `data/settings.yaml`.

**If your ISP has data caps it's recommended to increase the default intervals within `data/settings.yaml`**

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History

**v0.1**
First release

## License

MIT. See LICENSE