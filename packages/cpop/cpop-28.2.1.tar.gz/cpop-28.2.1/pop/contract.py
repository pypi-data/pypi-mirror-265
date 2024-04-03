"""
Contracts to enforce loader objects
"""
import functools
import inspect
from collections.abc import Iterable
from types import ModuleType
from typing import get_args
from typing import get_origin
from typing import get_type_hints

import pop.exc
import pop.hub
import pop.verify

try:
    # Only do strict type checking in a dev environment
    import pytest  # noqa

    STRICT_TYPE_CHECKING: bool = True
except ImportError:
    STRICT_TYPE_CHECKING: bool = False


class ContractedContext:
    """
    Contracted function calling context
    """

    def __init__(
        self,
        func: functools.partial,
        args: Iterable,
        kwargs: dict,
        signature,
        ref,
        name,
        ret=None,
        cache=None,
    ):  # pylint: disable=too-many-arguments
        if cache is None:
            cache = {}

        self.func = func
        self.args = list(args)
        self.kwargs = kwargs
        self.signature = signature
        self.ref = ref
        self.__name__ = name
        self.ret = ret
        self.cache = cache

    def get_arguments(self):
        """
        Return a dictionary of all arguments that will be passed to the function and their
        values, including default arguments.
        """
        if "__bound_signature__" not in self.cache:
            self.cache["__bound_signature__"] = self.signature.bind(
                *self.args, **self.kwargs
            )
            # Apply any default values from the signature
            self.cache["__bound_signature__"].apply_defaults()
        return self.cache["__bound_signature__"].arguments


def load_contract(
    contracts: "pop.hub.Sub",
    default_contracts: list[str],
    mod: ModuleType,
    name: str,
) -> list["pop.loader.LoadedMod"]:
    """
    return a Contract object loaded up
    Dynamically create the correct Contracted type
    :param contracts: Contracts functions to add to the sub
    :param default_contracts: The contracts that have been marked as defaults
    :param mod: A loader module
    :param name: The name of the module to get from the loader
    """
    raws = []
    loaded_contracts = []
    if hasattr(contracts, name):
        loaded_contracts.append(name)
        raws.append(getattr(contracts, name))
    if hasattr(contracts, "init"):
        if "init" not in loaded_contracts:
            loaded_contracts.append("init")
            raws.append(getattr(contracts, "init"))
    if hasattr(mod, "__contracts__"):
        cnames = getattr(mod, "__contracts__")
        for cname in cnames:
            if cname in contracts:
                loaded_contracts.append(cname)
                raws.append(getattr(contracts, cname))
    return raws


class Contracted:
    """
    This class wraps functions that have a contract associated with them
    and executes the contract routines
    """

    def __init__(
        self,
        hub: "pop.hub.Hub",
        contracts: list["pop.hub.Sub"],
        func: functools.partial,
        ref: str,
        name: str,
        implicit_hub: bool = True,
    ):
        """
        :param hub: The redistributed pop central hub
        :param contracts: Contracts functions to add to the sub
        :param func: The contracted function to call
        :param ref: The reference to the function on the hub
        :param name: An alias for the function
        :param implicit_hub: True if a hub should be implicitly injected into the "call" method
        """
        self.__dict__.update(
            getattr(func, "__dict__", {})
        )  # do this first so we later overwrite any conflicts
        self.func = func
        self.ref = ref
        self.__name__ = name
        self.signature = inspect.signature(self.func)
        self._sig_errors = []
        self.__wrapped__ = func
        self.hub = hub
        self.contracts = contracts or []
        self.implicit_hub = implicit_hub
        self._load_contracts()

    def _get_contracts_by_type(self, contract_type: str = "pre") -> list["Contracted"]:
        """
        :param contract_type: One of "call", "pre", "post", or "sig"
        """
        matches = []
        fn_contract_name = f"{contract_type}_{self.__name__}"
        for contract in self.contracts:
            if hasattr(contract, fn_contract_name):
                matches.append(getattr(contract, fn_contract_name))
            if hasattr(contract, contract_type):
                matches.append(getattr(contract, contract_type))

        if contract_type == "post":
            matches.reverse()

        return matches

    def _load_contracts(self):
        # if Contracted - only allow regular pre/post
        # if ContractedAsync - allow coroutines and functions

        self.contract_functions = {
            "pre": self._get_contracts_by_type("pre"),
            "call": self._get_contracts_by_type("call")[:1],
            "post": self._get_contracts_by_type("post"),
        }
        self._has_contracts = sum(len(l) for l in self.contract_functions.values()) > 0

    async def __call__(self, *args, **kwargs):
        if self.implicit_hub:
            args = (self.hub,) + args

        if STRICT_TYPE_CHECKING:
            assert strict_type_checking(self, *args, **kwargs)

        if not self._has_contracts:
            ret = await self.func(*args, **kwargs)
            if STRICT_TYPE_CHECKING:
                assert strict_return_checking(self, ret)
            return ret
        contract_context = ContractedContext(
            self.func, args, kwargs, self.signature, self.ref, self.__name__
        )

        # Process pre contracts
        for fn in self.contract_functions["pre"]:
            pre_ret = await fn(contract_context)

            await self.hub.pop.contract.process_pre_result(pre_ret, fn, self)

        # Call the one call contract
        if self.contract_functions["call"]:
            ret = await self.contract_functions["call"][0](contract_context)
        else:
            ret = await self.func(*contract_context.args, **contract_context.kwargs)

        # Handle post contracts
        for fn in self.contract_functions["post"]:
            contract_context.ret = ret
            post_ret = await fn(contract_context)
            if post_ret is not None:
                ret = post_ret

        if STRICT_TYPE_CHECKING:
            assert strict_return_checking(self, ret)

        return ret

    def __getstate__(self):
        return dict(
            ref=self.ref,
            name=self.__name__,
            implicit_hub=self.implicit_hub,
            contracts=self.contracts,
        )

    def __setstate__(self, state):
        self.ref = state["ref"]
        self.name = state["name"]
        self.func = self.hub[self.ref][self.name].func
        self.implicit_hub = state["implicit_hub"]
        self.contracts = state["contracts"]


class ContractedAsyncGen(Contracted):
    async def __call__(self, *args, **kwargs):
        if self.implicit_hub:
            args = (self.hub,) + args

        if STRICT_TYPE_CHECKING:
            assert strict_type_checking(self, *args, **kwargs)

        if not self._has_contracts:
            async for chunk in self.func(*args, **kwargs):
                yield chunk
            return
        contract_context = ContractedContext(
            self.func, args, kwargs, self.signature, self.ref, self.__name__
        )

        for fn in self.contract_functions["pre"]:
            pre_ret = await fn(contract_context)

            await self.hub.pop.contract.process_pre_result(pre_ret, fn, self)
        chunk = None
        if self.contract_functions["call"]:
            async for chunk in self.contract_functions["call"][0](contract_context):
                yield chunk
        else:
            async for chunk in self.func(
                *contract_context.args, **contract_context.kwargs
            ):
                yield chunk
        ret = chunk
        for fn in self.contract_functions["post"]:
            contract_context.ret = ret
            post_ret = await fn(contract_context)
            if post_ret is not None:
                ret = post_ret

        if STRICT_TYPE_CHECKING:
            assert strict_return_checking(self, ret)


def create_contracted(
    hub: "pop.hub.Hub",
    contracts: list["pop.loader.LoadedMod"],
    func: functools.partial,
    ref: str,
    name: str,
    implicit_hub: bool = True,
) -> Contracted:
    """
    Dynamically create the correct Contracted type
    :param hub: The redistributed pop central hub
    :param contracts: Contracts functions to add to the sub
    :param func: The contracted function to call
    :param ref: The reference to the function on the hub
    :param name: The name of the module to get from the loader
    :param implicit_hub: True if a hub should be implicitly injected into the "call" method
    """
    if inspect.isasyncgenfunction(func):
        return ContractedAsyncGen(hub, contracts, func, ref, name, implicit_hub)
    else:
        return Contracted(hub, contracts, func, ref, name, implicit_hub)


def strict_type_checking(contract: Contracted, *args, **kwargs) -> bool:
    # Perform type checking based on the signature and type hints
    bound_args = contract.signature.bind(*args, **kwargs)
    type_hints = get_type_hints(contract.func)

    for param_name, value in bound_args.arguments.items():
        expected_type = type_hints.get(param_name)
        if expected_type:
            origin = get_origin(expected_type)
            type_args = get_args(expected_type)

            if origin and not isinstance(value, origin):
                raise TypeError(
                    f"Argument '{param_name}' must be of type {origin.__name__}, got {type(value).__name__}"
                )

            if type_args:
                # Add checks for specific container types if needed
                pass

    return True


def strict_return_checking(contract: Contracted, ret: any) -> bool:
    type_hints = get_type_hints(contract.func)
    expected_return_type = type_hints.get("return")

    if expected_return_type:
        origin = get_origin(expected_return_type)
        type_args = get_args(expected_return_type)

        if origin and not isinstance(ret, origin):
            raise TypeError(
                f"Return value must be of type {origin.__name__}, got {type(ret).__name__}"
            )

        if type_args:
            # Add checks for specific container types if needed
            pass

    return True
