from json import loads

config = loads(open("config.json", "r").read())

is_allowed = lambda url : url.startswith("https://docs.github.com/en")
is_skipped = lambda url : False