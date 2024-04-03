import asyncio
import pathlib
from collections.abc import Callable
from pprint import pprint

import msgpack

import pop.hub


def save_hub_state(hub, state_file: pathlib.Path):
    # Manually retrieve the state using __getstate__
    state = hub.__getstate__()
    state_file.parent.mkdir(parents=True, exist_ok=True)
    with state_file.open("wb") as f:
        msgpack.dump(state, f)


def load_hub_state(hub, state_file: pathlib.Path):
    if state_file.exists():
        try:
            with state_file.open("rb") as f:
                state = msgpack.load(f)
        except:
            return
        if hub._init_kwargs != state["init_kwargs"]:
            hub.__init__(**state["init_kwargs"])
        hub.__setstate__(state)
        return hub


def main():
    # Create the hub, loading all dynes and starting the loop
    hub = pop.hub.Hub(cli="pop_cli")

    args = []
    kwargs = {}

    original_opt = hub.OPT
    ref = original_opt.pop_cli.ref or "."

    # Try to get a saved hub
    if original_opt.pop_cli.hub_state:
        hub_state_file = pathlib.Path(original_opt.pop_cli.hub_state).expanduser()
        new_hub = load_hub_state(hub, hub_state_file)
    else:
        hub_state_file = None
        new_hub = None

    # Successfully loaded a hub from a file
    if new_hub is not None:
        hub = new_hub

    # Override hub.OPT with the the new cli
    cli = original_opt.pop_cli.cli
    if cli:
        # Pass all remaining args onto the new parser
        hub._opt = hub._sync.pop.config.load(
            cli=cli, parser_args=original_opt.pop_cli.args
        )
    else:
        # We are using the pop cli, treat all the extra args as parameters for the called function
        PLACEHOLDER = object()
        hold = PLACEHOLDER
        for arg in original_opt.pop_cli.args:
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

    # Get the named reference from the hub
    finder = hub
    parts = ref.split(".")
    for p in parts:
        if not p:
            continue
        finder = getattr(finder, p)

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

    if hub_state_file:
        save_hub_state(hub, hub_state_file)


if __name__ == "__main__":
    main()
