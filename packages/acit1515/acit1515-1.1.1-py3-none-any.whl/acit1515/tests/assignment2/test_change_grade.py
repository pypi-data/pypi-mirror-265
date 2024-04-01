import random
import json
import platform
from colorama import Fore
from acit1515.tests.test import Test
from acit1515.helpers import Transcript
from pathlib import Path

sep = '\\' if platform.system() == 'Windows' else '/'

class Change_Grade(Test):
    def __init__(self, submission):
        self.name = f'{__class__.__name__.lower()}()'
        self.submission = submission

    def test1_returns(self):
        returns = True
        
        valid_dir_string = "/".join(__file__.split(sep)[:-1]) + '/transcripts'
        valid_user = Transcript(
            "Test", 
            "User", 
            [
                {"course": "ACIT 1630", "mark": 74}, 
                {"course": "ACIT 1515", "mark": 65}, 
                {"course": "MATH 1310", "mark": 90}
            ]
        )
        valid_course = 0
        valid_mark = 99

        try:
            updated = self.submission.change_grade(valid_dir_string, valid_user, valid_course, valid_mark)
        except Exception as e:
            returns = False
        else:
            if updated != None:
                returns = False
        
        if not returns:
            print(Fore.RED + f"FAIL: {self.name} failed or incorrectly returned a value (-3 marks)" + Fore.RESET)
            return { 'deduction': 3, 'continue': False }

        return { 'deduction': 0, 'continue': True }
    
    def test2_hardcoded(self):
        returns = True
        
        valid_dir_string = "/".join(__file__.split(sep)[:-1]) + '/transcripts'
        valid_user = Transcript(
            "Test", 
            "User", 
            [
                {"course": "ACIT 1630", "mark": 74}, 
                {"course": "ACIT 1515", "mark": 65}, 
                {"course": "MATH 1310", "mark": 90}
            ]
        )
        another_valid_user = Transcript(
            "Test", 
            "User2", 
            [
                {"course": "ACIT 1630", "mark": 74}, 
                {"course": "ACIT 1515", "mark": 65}, 
                {"course": "MATH 1310", "mark": 90}
            ]
        )
        random_course = random.randint(0,2)
        random_mark = random.randint(0,100)
        another_random_course = random.randint(0,2)
        another_random_mark = random.randint(0,100)

        self.submission.change_grade(valid_dir_string, valid_user, random_course, random_mark)
        self.submission.change_grade(valid_dir_string, another_valid_user, another_random_course, another_random_mark)

        dir = Path("/".join(__file__.split(sep)[:-1]))
        valid_path = dir.joinpath('transcripts/Test-User.json')
        another_valid_path = dir.joinpath('transcripts/Test-User2.json')

        try:
            with valid_path.open() as file:
                data = json.load(file)

            with another_valid_path.open() as file:
                more_data = json.load(file)
        except:
            returns = False
        else:
            if data == more_data:
                returns = False

        if not returns:
            print(Fore.RED + f"FAIL: {self.name} appears to be returning a hardcoded value (-2 marks)" + Fore.RESET)
            return { 'deduction': 2, 'continue': False }
    
        return { 'deduction': 0, 'continue': True }
    
    def test3_valid(self):
        returns = True

        valid_dir_string = "/".join(__file__.split(sep)[:-1]) + '/transcripts'
        valid_user = Transcript(
            "Test", 
            "User", 
            [
                {"course": "ACIT 1630", "mark": 74}, 
                {"course": "ACIT 1515", "mark": 65}, 
                {"course": "MATH 1310", "mark": 90}
            ]
        )
        random_course = random.randint(0,2)
        random_mark = random.randint(0,100)

        self.submission.change_grade(valid_dir_string, valid_user, random_course, random_mark)

        dir = Path("/".join(__file__.split(sep)[:-1]))
        valid_path = dir.joinpath('transcripts/Test-User.json')

        try:
            with valid_path.open() as file:
                data = json.load(file)
        except:
            returns = False
        else:
            if not (
                valid_user.firstname == data["firstname"]
                and valid_user.lastname == data["lastname"]
                and valid_user.grades == data["grades"]
            ):
                returns = False
                
        if not returns:
            print(Fore.RED + f"FAIL: {self.name} does not successfully update a transcript file (-3 marks)" + Fore.RESET)
            return { 'deduction': 3, 'continue': False }

        print(Fore.GREEN + f"PASS: {self.name} returned a valid Transcript object (3 marks)" + Fore.RESET)
        return { 'deduction': 0, 'continue': True }