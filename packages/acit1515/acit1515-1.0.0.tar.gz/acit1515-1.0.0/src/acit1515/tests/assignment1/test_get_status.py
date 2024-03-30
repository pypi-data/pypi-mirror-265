from colorama import Fore
from acit1515.tests.test import Test

class Get_Status(Test):
    def __init__(self, submission):
        self.name = 'get_status()'
        self.submission = submission

    def test1_returns(self):
        returns = True

        try:
            status = self.submission.get_status([7, 7, 7, 7, 7, 7, 7])
        except:
            returns = False
        else:
            if status == None:
                returns = False
        
        if not returns:
            print(Fore.RED + f"FAIL: {self.name} does not return a value (-3 marks)" + Fore.RESET)
            return { 'deduction': 3, 'continue': False }

        return { 'deduction': 0, 'continue': True }
    
    def test2_bool(self):
        status = self.submission.get_status([7, 7, 7, 7, 7, 7, 7])
        if not isinstance(status, bool):
            print(Fore.RED + f"FAIL: {self.name} does not return a boolean value (-2 marks)" + Fore.RESET)
            return { 'deduction': 2, 'continue': False } 
        
        return { 'deduction': 0, 'continue': True }
    
    def test3_valid(self):
        status1 = self.submission.get_status([7, 7, 7, 7, 7, 7, 7])
        status2 = self.submission.get_status([90, 90, 90, 90, 90, 90, 90])
        
        if status1 and not status2:
            print(Fore.RED + f"FAIL: {self.name} does not correctly return the status (-1 marks)" + Fore.RESET)
            return { 'deduction': 1, 'continue': False }

        print(Fore.GREEN + f"PASS: {self.name} produced a valid value (3 marks)" + Fore.RESET)
        return { 'deduction': 0, 'continue': True }