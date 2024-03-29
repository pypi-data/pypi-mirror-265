import os
from colorama import Fore
from acit1515.tests.test import Test
from pathlib import Path

class Is_Valid_Transcript(Test):
    def __init__(self, submission):
        self.name = f'{__class__.__name__.lower()}()'
        self.submission = submission

    def test1_returns(self):
        returns = True

        try:
            updated = self.submission.is_valid_transcript({})
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
        correct = {
            "firstname": "Chris",
            "lastname": "Harris",
            "grades": [
                {"course": "ACIT 1515", "mark": 90},
                {"course": "ACIT 1620", "mark": 100}
            ]
        }
        incorrect = {}
        
        if type(self.submission.is_valid_transcript(correct)) != bool or type(self.submission.is_valid_transcript(incorrect)) != bool:
            print(Fore.RED + f"FAIL: {self.name} does not return a list of Path objects (-3 marks)" + Fore.RESET)
            return { 'deduction': 3, 'continue': False } 
        
        return { 'deduction': 0, 'continue': True }
    
    def test3_hardcoded(self):
        correct = correct = {
            "firstname": "Chris",
            "lastname": "Harris",
            "grades": [
                {"course": "ACIT 1515", "mark": 90},
                {"course": "ACIT 1620", "mark": 100}
            ]
        }
        incorrect1 = {}
        incorrect2 = {
            "firstname": "Jeremy",
            "lastname": "Holman"
        }
        transcripts = [correct, incorrect1, incorrect2]

        if all(self.submission.is_valid_transcript(t) for t in transcripts) or all(not self.submission.is_valid_transcript(t) for t in transcripts):
            print(Fore.RED + f"FAIL: {self.name} appears to be returning a hardcoded value (-2 marks)" + Fore.RESET)
            return { 'deduction': 2, 'continue': False }
    
        return { 'deduction': 0, 'continue': True }
    
    def test4_valid(self):
        correct = correct = {
            "firstname": "Chris",
            "lastname": "Harris",
            "grades": [
                {"course": "ACIT 1515", "mark": 90},
                {"course": "ACIT 1620", "mark": 100}
            ]
        }
        incorrect = {}

        if not self.submission.is_valid_transcript(correct) or self.submission.is_valid_transcript(incorrect):
            print(Fore.RED + f"FAIL: {self.name} does not return a valid list of Path objects (-1 mark)" + Fore.RESET)
            return { 'deduction': 1, 'continue': False }

        print(Fore.GREEN + f"PASS: {self.name} returned a valid list of Path objects (4 marks)" + Fore.RESET)
        return { 'deduction': 0, 'continue': True }