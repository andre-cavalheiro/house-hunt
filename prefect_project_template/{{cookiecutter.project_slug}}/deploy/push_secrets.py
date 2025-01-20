from secrets_manager import execute_all_modules, search_modules, execute_function
import sys


if __name__ == "__main__":
    secret = sys.argv[1] if len(sys.argv) > 1 else None
    if secret:
        modules = search_modules(secret)
        if not modules:
            print("No modules found for function %s" % secret)
            sys.exit()
        for module in modules:
            execute_function(module, secret)
    else:
        execute_all_modules()
