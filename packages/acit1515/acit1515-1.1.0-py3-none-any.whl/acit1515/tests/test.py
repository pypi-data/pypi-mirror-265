class Test():
    """
    MANIFESTO

    Assignments must consist of:
        - Simple functions with no side effects, no sys.exit()
        - Input and output confined to __main__ 

    Test functions must be organized in order of blocking requirements, where x is the maximum number of marks for the question, e.g.:
        First function tests if value is returned (x marks deducted)
        Second function tests if returned value is correct type (x - 1 marks deducted)
        Third function tests if returned value is valid (x - 2 marks deducted)
    """
    def run_tests(self):
        tests = [attr for attr in dir(self) if attr.startswith("test")]
        total_marks = len(tests)

        for test in tests:
            result = getattr(self, test)()
            total_marks -= result['deduction']
            if not result['continue']:
                break
        
        return (len(tests), len(tests) - total_marks)