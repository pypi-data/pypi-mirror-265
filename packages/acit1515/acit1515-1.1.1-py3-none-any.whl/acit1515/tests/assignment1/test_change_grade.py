from colorama import Fore
from acit1515.tests.test import Test

"""

    TODO: concatenate and log error strings?

"""

class Change_Grade(Test):
    def __init__(self, submission):
        self.name = 'change_grade()'
        self.submission = submission

    def test1_returns(self):
        returns = True

        try:
            updated = self.submission.change_grade([50, 50, 50, 50, 50, 50, 50], 1, 75)
        except Exception as e:
            returns = False
        else:
            if updated == None:
               returns = False 
            
        if not returns:
            print(Fore.RED + f"FAIL: {self.name} does not return a value (-6 marks)" + Fore.RESET)
            return { 'deduction': 6, 'continue': False }

        return { 'deduction': 0, 'continue': True }
    
    def test2_list(self):
        updated = self.submission.change_grade([50, 50, 50, 50, 50, 50, 50], 1, 75)
        if not isinstance(updated, list):
            print(Fore.RED + f"FAIL: {self.name} does not return a list (-5 marks)" + Fore.RESET)
            return { 'deduction': 5, 'continue': False } 
        
        return { 'deduction': 0, 'continue': True }
    
    def test3_length(self):
        updated = self.submission.change_grade([50, 50, 50, 50, 50, 50, 50], 1, 75)
        if len(updated) != 7:
            print(Fore.RED + f"FAIL: {self.name} does not return a list of length 7 (-4 marks)" + Fore.RESET)
            return { 'deduction': 4, 'continue': False } 
        
        return { 'deduction': 0, 'continue': True }
    
    def test4_hardcoded(self):
        updated1 = self.submission.change_grade([50, 50, 50, 50, 50, 50, 50], 1, 75)
        updated2 = self.submission.change_grade([40, 50, 50, 50, 50, 50, 50], 1, 90)
        updated3 = self.submission.change_grade([30, 50, 50, 50, 50, 50, 50], 1, 45)
        
        if updated1[0] == updated2[0] and updated1[0] == updated3[0]:
            print(Fore.RED + f"FAIL: {self.name} appears to be returning hard-coded values (-3 marks)" + Fore.RESET)
            return { 'deduction': 3, 'continue': False }

        return { 'deduction': 0, 'continue': True }
    
    def test5_changed(self):
        """
        
            TODO: update instructions to ensure students are allowing the correct offset,
                i.e. a user running the program chooses '2' to change the second grade
                    which should update the list at position 1
        
        """
        try:
           updated = self.submission.change_grade([50, 0, 50, 50, 50, 50, 50], 7, 99) 
        except:
            print(Fore.RED + f"FAIL: {self.name} allows out of bounds list index (-2 marks)" + Fore.RESET)
            return { 'deduction': 2, 'continue': False } 
        
        updated = self.submission.change_grade([50, 0, 50, 50, 50, 50, 50], 2, 99)
        
        if updated[1] != 99:
            print(Fore.RED + f"FAIL: {self.name} does not correctly change grade (-2 marks)" + Fore.RESET)
            return { 'deduction': 2, 'continue': False } 
        
        return { 'deduction': 0, 'continue': True }
    
    def test6_valid(self):
        updated1 = self.submission.change_grade([50, 50, 50, 50, 50, 50, 50], 1, 101)
        updated2 = self.submission.change_grade([50, 50, 50, 50, 50, 50, 50], 1, -1)

        if updated1 == None or updated2 == None:
            print(Fore.RED + f"FAIL: {self.name} does not return a value for invalid data (-1 marks)" + Fore.RESET)
            return { 'deduction': 1, 'continue': False }

        if updated1[0] != 50 and updated2[0] != 50:
            print(Fore.RED + f"FAIL: {self.name} does not correctly ignore invalid grades (-1 marks)" + Fore.RESET)
            return { 'deduction': 1, 'continue': False }

        print(Fore.GREEN + f"PASS: {self.name} produced a valid list (5 marks)" + Fore.RESET)
        return { 'deduction': 0, 'continue': True }