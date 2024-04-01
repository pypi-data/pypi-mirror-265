from colorama import Fore
from acit1515.tests.test import Test

class Generate_Grade(Test):
    def __init__(self, submission):
        self.name = 'generate_grade()'
        self.submission = submission

    def test1_returns(self):
        is_none = self.submission.generate_grade()
        if is_none == None:
            print(Fore.RED + f"FAIL: {self.name} does not return a value (-3 marks)" + Fore.RESET)
            return { 'deduction': 3, 'continue': False }

        return { 'deduction': 0, 'continue': True }
    
    def test2_hardcoded(self):
        grade_set = { self.submission.generate_grade(), self.submission.generate_grade(), self.submission.generate_grade(), self.submission.generate_grade() }
        if len(grade_set) == 1:
            print(Fore.RED + f"FAIL: {self.name} is returning a hard-coded value (-2 marks)" + Fore.RESET)
            return { 'deduction': 2, 'continue': False }
        
        return { 'deduction': 0, 'continue': True }
        
    def test3_valid(self):
        for i in range(10000):
            test_grade = self.submission.generate_grade()

            if not isinstance(test_grade, int) or test_grade < 0 or test_grade > 100:
                print(Fore.RED + f"FAIL: {self.name} produced an invalid value (-1 mark)" + Fore.RESET)
                return { 'deduction': 1, 'continue': False }
        
        print(Fore.GREEN + f"PASS: {self.name} produced a valid value (3 marks)" + Fore.RESET)
        return { 'deduction': 0, 'continue': True }