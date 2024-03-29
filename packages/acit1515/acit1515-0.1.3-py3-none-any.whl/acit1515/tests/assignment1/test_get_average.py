import random
from colorama import Fore
from statistics import mean
from acit1515.tests.test import Test

class Get_Average(Test):
    def __init__(self, submission):
        self.name = 'get_average()'
        self.submission = submission

    def test1_returns(self):
        average = self.submission.get_average([7, 7, 7, 7, 7, 7, 7])
        if average == None:
            print(Fore.RED + f"FAIL: {self.name} does not return a value (-4 marks)" + Fore.RESET)
            return { 'deduction': 4, 'continue': False }

        return { 'deduction': 0, 'continue': True }
    
    def test2_number(self):
        average = self.submission.get_average([7, 7, 7, 7, 7, 7, 7])
        if not (isinstance(average, int) or isinstance(average, float)):
            print(Fore.RED + f"FAIL: {self.name} does not return an int/float (-3 marks)" + Fore.RESET)
            return { 'deduction': 3, 'continue': False } 
        
        return { 'deduction': 0, 'continue': True }
    
    def test3_hardcoded(self):
        average1 = self.submission.get_average([7, 7, 7, 7, 7, 7, 7])  
        average2 = self.submission.get_average([8, 8, 8, 8, 8, 8, 8])  
        average3 = self.submission.get_average([9, 9, 9, 9, 9, 9, 9])

        if average1 == average2 and average1 == average3:
                print(Fore.RED + f"FAIL: {self.name} appears to be returning hard coded values (-2 marks)" + Fore.RESET)
                return { 'deduction': 2, 'continue': False }

        return { 'deduction': 0, 'continue': True }
    
    def test4_valid(self):
        test_grades = random.sample(range(101), 7)
        average = self.submission.get_average(test_grades)
        if round(average, 2) != round(mean(test_grades), 2):
            print(Fore.RED + f"FAIL: {self.name} does not correctly return the average of a list (-1 marks)" + Fore.RESET)
            return { 'deduction': 1, 'continue': False }

        print(Fore.GREEN + f"PASS: {self.name} produced a valid value (4 marks)" + Fore.RESET)
        return { 'deduction': 0, 'continue': True }