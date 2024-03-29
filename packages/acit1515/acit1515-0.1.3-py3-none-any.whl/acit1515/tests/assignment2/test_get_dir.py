import os
from colorama import Fore
from acit1515.tests.test import Test
from pathlib import Path

class Get_Dir(Test):
    def __init__(self, submission):
        self.name = f'{__class__.__name__.lower()}()'
        self.submission = submission

    def test1_returns(self):
        returns = True

        try:
            updated = self.submission.get_dir('./transcripts')
        except Exception as e:
            returns = False
        else:
            if updated == None:
               returns = False 
        
        if not returns:
            print(Fore.RED + f"FAIL: {self.name} does not return a value (-4 marks)" + Fore.RESET)
            return { 'deduction': 4, 'continue': False }

        return { 'deduction': 0, 'continue': True }
    
    def test2_type(self):
        correct = self.submission.get_dir('./transcripts')
        incorrect = self.submission.get_dir('./someotherdirectory')
        
        if not isinstance(correct, Path):
            print(Fore.RED + f"FAIL: {self.name} does not return a Path object for valid directory (-3 marks)" + Fore.RESET)
            return { 'deduction': 3, 'continue': False } 
        if incorrect != False:
            print(Fore.RED + f"FAIL: {self.name} does not return False for an invalid directory (-3 marks)" + Fore.RESET)
            return { 'deduction': 3, 'continue': False } 
        
        return { 'deduction': 0, 'continue': True }
    
    def test3_hardcoded(self):
        current_dir = "/".join(os.path.realpath(__file__).split('\\')[:-1])
        transcripts_path = Path(current_dir + "/transcripts")
        mock_path = Path(current_dir + '/mock')
        dir1 = self.submission.get_dir(transcripts_path)
        dir2 = self.submission.get_dir(mock_path)

        dir1_files = dir1.glob('**/*')
        dir2_files = dir2.glob('**/*')

        if dir1_files == dir2_files:
            print(Fore.RED + f"FAIL: {self.name} appears to be returning a hardcoded value (-2 marks)" + Fore.RESET)
            return { 'deduction': 2, 'continue': False }
    
        return { 'deduction': 0, 'continue': True }
    
    def test4_valid(self):
        valid = True

        current_dir = "/".join(os.path.realpath(__file__).split('\\')[:-1])
        transcripts_path = Path(current_dir + "/transcripts")
        mock_path = Path(current_dir + '/mock')
        dir1 = self.submission.get_dir(transcripts_path)
        dir2 = self.submission.get_dir(mock_path)

        if not dir1.joinpath('Test-User.json').is_file() and not dir2.joinpath('mock.txt').is_file():
            print(Fore.RED + f"FAIL: {self.name} does not return the correct directory (-1 mark)" + Fore.RESET)
            return { 'deduction': 1, 'continue': False }

        print(Fore.GREEN + f"PASS: {self.name} returned a valid value (4 marks)" + Fore.RESET)
        return { 'deduction': 0, 'continue': True }