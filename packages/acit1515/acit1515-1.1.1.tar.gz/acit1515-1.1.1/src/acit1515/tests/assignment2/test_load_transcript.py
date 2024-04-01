import platform
import json
from colorama import Fore
from acit1515.tests.test import Test
from acit1515.helpers import Transcript
from pathlib import Path

sep = '\\' if platform.system() == 'Windows' else '/'

class Load_Transcript(Test):
    def __init__(self, submission):
        self.name = f'{__class__.__name__.lower()}()'
        self.submission = submission

    def test0_handles_invalid_json(self):
        handles = True
        dir = Path("/".join(__file__.split(sep)[:-1]))
        
        try:
            empty_path = dir.joinpath('transcripts/Blank-User.json')
            empty = self.submission.load_transcript(empty_path)
        except:
            handles = False 
        else:
            if empty != False:
                handles = False
        
        if not handles:
            print(Fore.RED + f"FAIL: {self.name} does not handle empty/invalid JSON files (-5 marks)" + Fore.RESET)
            return { 'deduction': 5, 'continue': False } 
        
        return { 'deduction': 0, 'continue': True }

    def test1_returns(self):
        returns = True
        dir = Path("/".join(__file__.split(sep)[:-1]))
        p = dir.joinpath('transcripts/Test-User.json')

        try:
            updated = self.submission.load_transcript(p)
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
        dir = Path("/".join(__file__.split(sep)[:-1]))
        
        valid_path = dir.joinpath('transcripts/Test-User.json')
        invalid_path = dir.joinpath('transcripts/User-Test.json')

        valid = self.submission.load_transcript(valid_path)
        invalid = self.submission.load_transcript(invalid_path)
        
        if not isinstance(valid, Transcript) or invalid != False:
            print(Fore.RED + f"FAIL: {self.name} does not return the correct data type for valid/invalid path (-3 marks)" + Fore.RESET)
            return { 'deduction': 3, 'continue': False } 
        
        return { 'deduction': 0, 'continue': True }
    
    def test3_hardcoded(self):
        dir = Path("/".join(__file__.split(sep)[:-1]))
        
        valid_path = dir.joinpath('transcripts/Test-User.json')
        another_valid_path = dir.joinpath('transcripts/Test-User2.json')
        
        invalid_path = dir.joinpath('transcripts/User-Test.json')

        valid = self.submission.load_transcript(valid_path)
        another_valid = self.submission.load_transcript(another_valid_path)
        invalid = self.submission.load_transcript(invalid_path)

        if (
            isinstance(valid, Transcript) 
            and isinstance(another_valid, Transcript) 
            and valid == invalid
        ) or (
            valid == False 
            and another_valid == False 
            and invalid == False
        ):
            print(Fore.RED + f"FAIL: {self.name} appears to be returning a hardcoded value (-2 marks)" + Fore.RESET)
            return { 'deduction': 2, 'continue': False }
    
        return { 'deduction': 0, 'continue': True }
    
    def test4_valid(self):
        returns = True

        dir = Path("/".join(__file__.split(sep)[:-1]))
        valid_path = dir.joinpath('transcripts/Test-User.json')
        
        try:
            with valid_path.open() as file:
                valid_user = json.load(file)
                valid_user = Transcript(
                    valid_user["firstname"], 
                    valid_user["lastname"], 
                    valid_user["grades"]
                )
        except:
            returns = False
        else:
            valid_result = self.submission.load_transcript(valid_path)
            if valid_result != valid_user:
                returns = False
        
        if not returns:
            print(Fore.RED + f"FAIL: {self.name} does not return a valid Transcript object (-1 mark)" + Fore.RESET)
            return { 'deduction': 1, 'continue': False }

        print(Fore.GREEN + f"PASS: {self.name} returned a valid Transcript object (5 marks)" + Fore.RESET)
        return { 'deduction': 0, 'continue': True }