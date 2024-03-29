import importlib
import importlib.util
import os
import sys
from colorama import Fore
from . import extract

def run_test(test, input_file):
    try:
        """
        
        TODO: ensure path construction works on all operating systems and for all variants
        
        """
        path_parts = input_file.split('\\')
        mod = path_parts[-1]
        pkg = "/".join(path_parts[:-1])
        
        spec = importlib.util.spec_from_file_location(f"{pkg}.{mod}", input_file)
        submission = importlib.util.module_from_spec(spec)
        sys.modules[f"{pkg}.{mod}"] = submission
        spec.loader.exec_module(submission)
    except Exception as e:
        print(Fore.RED + f'FAIL: script could not be run' + Fore.RESET)
        print(e)
        print(f'Final mark: 0')
        sys.exit()
    else:
        results = []
        directory = "/".join(os.path.realpath(__file__).split('\\')[:-1])

        for filename in os.listdir(os.path.join(directory, f'tests/{test}')):
            if filename.startswith('test_'):
                module_name = f'acit1515.tests.{test}.{filename[:-3]}'
                module = importlib.import_module(module_name)
                class_name = filename[5:-3].title()
                results.append(getattr(module, class_name)(submission).run_tests())

        total_marks = sum([total for total, _ in results])
        deductions = sum([deduction for _, deduction in results])

        print(f'Final mark: {total_marks - deductions}/{total_marks}')

def run_tests(test_suite, target_directory):
    res = extract.extract_submissions(target_directory)

    if not res['ERROR_STATE']:
        for submission in res['output_path'].glob('*.py'):
            print(Fore.CYAN + f'\nRUNNING TESTS FOR .\\{submission}' + Fore.RESET)
            try:
                run_test(test_suite, f'.\\{submission}')
                print()
            except Exception as e:
                print(Fore.YELLOW + f'CAUGHT ERROR: {e}' + Fore.RESET)
            finally:
                print('----------------------------------------')
