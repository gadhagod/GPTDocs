from json import loads

config = loads(open("config.json", "r").read())

is_allowed = lambda url : url.startswith("https://docs.github.com/en") and not url.startswith("https://docs.github.com/enterprise")