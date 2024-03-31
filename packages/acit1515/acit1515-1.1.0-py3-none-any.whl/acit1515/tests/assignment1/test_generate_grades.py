from colorama import Fore
from acit1515.tests.test import Test

class Generate_Grades(Test):
    def __init__(self, submission):
        self.name = 'generate_grades()'
        self.submission = submission

    def test1_returns(self):
        test_grades = self.submission.generate_grades()
        if test_grades == None:
            print(Fore.RED + f"FAIL: {self.name} does not return a value (-5 marks)" + Fore.RESET)
            return { 'deduction': 5, 'continue': False } 
        
        return { 'deduction': 0, 'continue': True }

    def test2_list(self):
        test_grades = self.submission.generate_grades()
        if not isinstance(test_grades, list):
            print(Fore.RED + f"FAIL: {self.name} does not return a list (-4 marks)" + Fore.RESET)
            return { 'deduction': 4, 'continue': False } 
        
        return { 'deduction': 0, 'continue': True }
        
    def test3_length(self):
        test_grades = self.submission.generate_grades()
        if len(test_grades) != 7:
            print(Fore.RED + f"FAIL: {self.name} did not produce a list of length 7 (-3 marks)" + Fore.RESET)
            return { 'deduction': 3, 'continue': False } 

        return { 'deduction': 0, 'continue': True }
    
    def test4_hardcoded(self):
        test_grades = [self.submission.generate_grades(), self.submission.generate_grades(), self.submission.generate_grades()]  

        test_grades_set = set(self.submission.generate_grades())
        
        if (test_grades[0] == test_grades[1] and test_grades[0] == test_grades[2]) or len(test_grades_set) == 1:
            print(Fore.RED + f"FAIL: {self.name} appears to be returning hard coded values (-2 marks)" + Fore.RESET)
            return { 'deduction': 2, 'continue': False }

        return { 'deduction': 0, 'continue': True }
    
    def test5_valid(self):
        test_grades = self.submission.generate_grades()

        for v in test_grades:
            if v < 0 or v > 100:
                print(Fore.RED + f"FAIL: {self.name} returned invalid values (-1 marks)" + Fore.RESET)
                return { 'deduction': 1, 'continue': False }

        print(Fore.GREEN + f"PASS: {self.name} produced a valid list (5 marks)" + Fore.RESET)
        return { 'deduction': 0, 'continue': True }