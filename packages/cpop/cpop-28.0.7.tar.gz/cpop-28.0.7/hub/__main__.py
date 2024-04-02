import asyncio
from collections.abc import Callable
from pprint import pprint

import pop.hub


def main():
    # Create the hub, loading all dynes and starting the loop
    hub = pop.hub.Hub(cli="pop_cli")
    finder = hub

    ref = hub.OPT.pop_cli.ref
    parts = ref.split(".")
    for p in parts:
        if not p:
            continue
        finder = getattr(finder, p)

    args = []
    kwargs = {}

    # Override hub.OPT with the the new cli
    cli = hub.OPT.pop_cli.cli
    if cli:
        # Pass all remaining args onto the new parser
        hub.OPT = hub._sync.pop.config.load(cli=cli, parser_args=hub.OPT.pop_cli.args)
    else:
        # We are using the pop cli, treat all the extra args as parameters for the called function
        PLACEHOLDER = object()
        hold = PLACEHOLDER
        for arg in hub.OPT.pop_cli.args:
            if hold is not PLACEHOLDER:
                key = hold.replace("-", "_").lstrip("_")
                if "," in arg:
                    arg = arg.split(",")
                kwargs[key] = arg
                hold = PLACEHOLDER
            elif "=" in arg:
                key, value = arg.split("=", maxsplit=1)
                key = key.replace("-", "_").lstrip("_")
                if "," in value:
                    value = value.split(",")
                kwargs[key] = value
            elif arg.startswith("--"):
                hold = arg
            else:
                args.append(arg)

    # Call the named reference on the hub
    # This allows you to do
    # $ pop idem.init.cli
    # This way you can have multiple entrypoints, or even alias the above command to "idem"
    if asyncio.iscoroutinefunction(finder):
        pprint(hub._synchronize(finder))
    elif isinstance(finder, Callable):
        ret = finder(*args, **kwargs)
        while asyncio.iscoroutine(ret):
            ret = hub._synchronize(ret)

        pprint(ret)
    else:
        pprint(finder)


if __name__ == "__main__":
    main()
