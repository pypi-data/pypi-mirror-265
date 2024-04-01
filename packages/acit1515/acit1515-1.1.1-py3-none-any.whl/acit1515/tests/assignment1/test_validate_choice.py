from colorama import Fore
from acit1515.tests.test import Test

"""
    TODO: concatenate and log error strings?
"""

class Validate_Choice(Test):
    def __init__(self, submission):
        self.name = 'validate_choice()'
        self.submission = submission

    def test1_returns(self):
        returns = True

        try:
            choice = self.submission.validate_choice(1)
        except Exception as e:
            print(e)
            returns = False
        else:
            if choice == None:
                returns = False
        
        if not returns:
            print(Fore.RED + f"FAIL: {self.name} does not return a value (-4 marks)" + Fore.RESET)
            return { 'deduction': 4, 'continue': False }

        return { 'deduction': 0, 'continue': True }
    
    def test2_int(self):
        choice = self.submission.validate_choice(1)
        if not isinstance(choice, int):
            print(Fore.RED + f"FAIL: {self.name} does not return an int (-3 marks)" + Fore.RESET)
            return { 'deduction': 3, 'continue': False } 
        
        return { 'deduction': 0, 'continue': True }
    
    def test3_valid_accepted(self):
        valid_choice = self.submission.validate_choice(1)

        if not valid_choice == 1:
            print(Fore.RED + f"FAIL: {self.name} did not accept a valid choice (-1 mark)" + Fore.RESET)
            return { 'deduction': 1, 'continue': True }
                 
        return { 'deduction': 0, 'continue': True }
    
    def test4_invalid_rejected(self):
        invalid_choice = self.submission.validate_choice(10)

        if not invalid_choice == 0:
            print(Fore.RED + f"FAIL: {self.name} did not reject an invalid choice (-1 mark)" + Fore.RESET)
            return { 'deduction': 1, 'continue': True }
        
        print(Fore.GREEN + f"PASS: {self.name} produced a valid value (4 marks)" + Fore.RESET)
        return { 'deduction': 0, 'continue': True }
    
   