from colorama import Fore
from acit1515.tests.test import Test

class Get_Menu(Test):
    def __init__(self, submission):
        self.name = 'get_menu()'
        self.submission = submission

    def test1_returns(self):
        is_none = self.submission.get_menu()
        if is_none == None:
            print(Fore.RED + f"FAIL: {self.name} does not return a value (-5 marks)" + Fore.RESET)
            return { 'deduction': 5, 'continue': False }

        return { 'deduction': 0, 'continue': True }
    
    def test2_list(self):
        test_menu = self.submission.get_menu()
        if not isinstance(test_menu, list):
            print(Fore.RED + f"FAIL: {self.name} does not return a list (-4 marks)" + Fore.RESET)
            return { 'deduction': 4, 'continue': False } 
        
        return { 'deduction': 0, 'continue': True }
    
    def test3_length(self):
        test_menu = self.submission.get_menu()
        if len(test_menu) != 5:
            print(Fore.RED + f"FAIL: {self.name} did not produce a list of length 5 (-3 marks)" + Fore.RESET)
            return { 'deduction': 3, 'continue': False } 

        return { 'deduction': 0, 'continue': True }
    
    def test4_tuples(self):
        test_menu = self.submission.get_menu()
        for value in test_menu:
            if not isinstance(value, tuple):
                print(Fore.RED + f"FAIL: {self.name} does not return a list of tuples (-2 marks)" + Fore.RESET)
                return { 'deduction': 2, 'continue': False } 
        
        return { 'deduction': 0, 'continue': True }
    
    def test5_enumerated(self):
        test_menu = self.submission.get_menu()
        for i in range(len(test_menu)):
            if not isinstance(test_menu[i][0], int) and test_menu[i][0] == i + 1:
                print(Fore.RED + f"FAIL: {self.name} does not return a correctly enumerated list (-1 mark)" + Fore.RESET)
                return { 'deduction': 1, 'continue': False } 
        
        print(Fore.GREEN + f"PASS: {self.name} produced a valid list (5 marks)" + Fore.RESET)
        return { 'deduction': 0, 'continue': True }