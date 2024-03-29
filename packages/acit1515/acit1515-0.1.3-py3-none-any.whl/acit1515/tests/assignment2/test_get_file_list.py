import os
from colorama import Fore
from acit1515.tests.test import Test
from pathlib import Path

class Get_File_List(Test):
    def __init__(self, submission):
        self.name = f'{__class__.__name__.lower()}()'
        self.submission = submission

    def test1_returns(self):
        returns = True

        try:
            updated = self.submission.get_file_list('./transcripts')
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
        correct = self.submission.get_file_list('./transcripts')
        incorrect = self.submission.get_file_list('./someotherdirectory')
        
        if type(correct) != list or (type(correct) == list and not all(isinstance(p, Path) for p in correct)):
            print(Fore.RED + f"FAIL: {self.name} does not return a list of Path objects (-3 marks)" + Fore.RESET)
            return { 'deduction': 3, 'continue': False } 

        if incorrect != False:
            print(Fore.RED + f"FAIL: {self.name} does not return False for an invalid directory (-3 marks)" + Fore.RESET)
            return { 'deduction': 3, 'continue': False } 
        
        return { 'deduction': 0, 'continue': True }
    
    def test3_hardcoded(self):
        current_dir = "/".join(os.path.realpath(__file__).split('\\')[:-1])
        transcripts_path = Path(current_dir + "/transcripts")
        mock_path = Path(current_dir + '/mock')
        files1 = self.submission.get_file_list(transcripts_path.resolve())
        files2 = self.submission.get_file_list(mock_path.resolve())

        if files1 == files2:
            print(Fore.RED + f"FAIL: {self.name} appears to be returning a hardcoded value (-2 marks)" + Fore.RESET)
            return { 'deduction': 2, 'continue': False }
    
        return { 'deduction': 0, 'continue': True }
    
    def test4_valid(self):
        valid = True

        current_dir = "/".join(os.path.realpath(__file__).split('\\')[:-1])
        transcripts_path = Path(current_dir + "/transcripts")
        mock_path = Path(current_dir + '/mock')
        
        files1 = [p.name for p in self.submission.get_file_list(transcripts_path)]
        files2 = [p.name for p in self.submission.get_file_list(mock_path)]

        if (
            "Test-User.json" not in files1 or
            "User-Test.json" not in files1
        ) or (
            "mock.txt" not in files2
        ):
            print(Fore.RED + f"FAIL: {self.name} does not return a valid list of Path objects (-1 mark)" + Fore.RESET)
            return { 'deduction': 1, 'continue': False }

        print(Fore.GREEN + f"PASS: {self.name} returned a valid list of Path objects (4 marks)" + Fore.RESET)
        return { 'deduction': 0, 'continue': True }