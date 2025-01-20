import importlib
import os

from typing import List


def execute_all_modules() -> None:
    """
    Execute all functions in all modules in the folder.
    """
    print("Executing all functions in all modules...")
    m = list_modules()
    for module in m:
        execute_all_functions_in_module(module)


def list_modules() -> List[str]:
    """
    List all Python modules in the folder, excluding __init__.py.
    """
    return [
        module[:-3]
        for module in os.listdir(os.path.dirname(__file__))
        if module.endswith(".py") and module not in {"__init__.py"}
    ]


def execute_all_functions_in_module(module_name: str) -> None:
    """
    Execute all non-private functions in a specific module.
    :param module_name: The name of the module.
    """
    functions = list_functions_in_module(module_name)
    if not functions:
        print("No public functions found in %s.py." % module_name)
        return

    print("Executing all public functions in %s.py..." % module_name)
    for function in functions:
        execute_function(module_name, function)


def list_functions_in_module(module_name: str) -> List[str]:
    """
    List all functions in a given module, excluding private functions (those starting with '_').
    :param module_name: The name of the module to retrieve functions from.
    :return: A list of function names in the module.
    """
    try:
        module = importlib.import_module("secrets_manager." + module_name)
        return [
            func
            for func in dir(module)
            if callable(getattr(module, func)) and func.startswith("upsert")
        ]
    except ModuleNotFoundError:
        print("Error: module '%s.py' not found." % module_name)
        return []


def execute_function(module_name: str, function_name: str) -> None:
    """
    Execute a specific function from a specific module.
    :param module_name: The name of the module.
    :param function_name: The name of the function to execute.
    """
    try:
        module = importlib.import_module("secrets_manager." + module_name)
        if hasattr(module, function_name):
            print("Executing %s from %s.py..." % (function_name, module_name))
            getattr(module, function_name)()
        else:
            print(
                "Error: Function '%s' not found in %s.py."
                % (function_name, module_name)
            )
    except ModuleNotFoundError:
        print("Failed to import module '%s.py'." % module_name)


def search_modules(function_name: str) -> str:
    modules_with_target = []

    modules = list_modules()
    for module in modules:
        functions = list_functions_in_module(module)
        if function_name in functions:
            modules_with_target.append(module)
    return modules_with_target
