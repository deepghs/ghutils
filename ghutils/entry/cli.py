from .dispatch import ghutilcli

_DECORATORS = [
]

cli = ghutilcli
for deco in _DECORATORS:
    cli = deco(cli)
