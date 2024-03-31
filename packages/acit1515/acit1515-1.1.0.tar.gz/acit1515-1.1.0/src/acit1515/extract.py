import zipfile
import shutil
import re
import sys
from pathlib import Path
from colorama import Fore

def extract_zip(zip_file, dir):
    temp_dir = dir.joinpath('temp')
    temp_dir.mkdir(exist_ok=True)
    
    with zipfile.ZipFile(dir.joinpath(zip_file.name), 'r') as zip:
        zip.extractall(temp_dir)

    submission = extract_py(temp_dir, True)

    if submission is None:
        motherfucking_subdirectories = list(temp_dir.glob('*/'))
        
        if len(motherfucking_subdirectories) == 1:
            jesus_christ = list(motherfucking_subdirectories[0].glob('*.py'))
        
            if len(jesus_christ) == 1 and jesus_christ[0].suffix == '.py':
                return jesus_christ[0]
            else:
                # THIS IS WHERE I DRAW THE LINE
                return None

    return submission

def extract_py(dir, give_up = False):
    python_files = list(dir.glob('*.py'))
    submission = None

    match len(python_files):
        case 0:
            if not give_up:
                submission = extract_zip(dir)
        case 1:
            if not python_files[0].is_dir():
                submission = python_files[0]
        case _:
            if not python_files[-1].is_dir():
                submission = python_files[-1] 

    return submission

def extract_submissions(target_directory, verbose=False):
    ERROR_STATE = False
    count = 0

    """
        TODO: handle paths with/without windows and unix slashes
    """        

    output_path = Path(f'{"/".join(target_directory.split('\\'))[:-1]}-submissions')
    output_path.mkdir(exist_ok=True)

    pattern = re.compile('A[0-9]{8}_[a-z\\s\\-]+_[a-z]+', re.IGNORECASE) 

    for sub in Path(target_directory).glob('*'):
        if sub.name == 'index.html':
            continue

        result = re.search(pattern, sub.name)

        if result is None:
            print(Fore.RED + f'Filename pattern not matched for {sub}' + Fore.RESET)
            continue

        student = result.group()

        if sub.is_dir():
            submission = extract_py(sub)
        elif sub.suffix == '.py':
            submission = sub 
        elif sub.suffix == '.zip':
            submission = extract_zip(sub, student)

        if submission is None:
            print(Fore.RED + f'ERROR: could not find submission for {student}' + Fore.RESET)
            ERROR_STATE = True

        _from = submission
        _to = f"{output_path.name}/{student.replace(' ', '_')}.py"
        
        try:
            shutil.copy(_from, _to)
        except:
            print(Fore.RED + f'ERROR: could not copy submission for student {student}' + Fore.RESET)
            ERROR_STATE = True
        else:
            count += 1  
    
    if verbose:
        print(Fore.GREEN + f'Output {count} submissions to {output_path}' + Fore.RESET)

    return {
        'e': ERROR_STATE,
        'output_path': output_path
    }