"""A python source module to hold custom error classes for emld.py

Raises:
    ForceProblem: _description_
    VerboseProblem: _description_
    FutureDateProblem: _description_
"""
import sys

class bcolors:
    '''
    # Colors used in `Emld` console messages

    ### Examples
    ```
    # Example 1 (AssertionError)
    assert filepath != "", bcolors.FAIL + "`filepath` cannot be blank" + bcolors.ENDC

    # Example 2 (print statement)
    print(f'{bcolors.OKGREEN} Emld instance created! {bcolors.ENDC}')

    # Example 3 (multi-line f-string)
    self.msg = bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE + 'Process execution failed.' + bcolors.ENDC \
            + bcolors.FAIL + '`date_string` entered: ' + bcolors.WARNING + f'{self.problem_val}' \
            + bcolors.FAIL + 'Parameter ' \
            + bcolors.OKBLUE + '`date_string` ' \
            + bcolors.FAIL + 'cannot be in the future.' + bcolors.ENDC
    ```
    '''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class MissingNodeException(Exception):
    '''
    # Sub-class of `Error` that handles Missing nodes

    ### `Error`; parent-class
        - `FutureDateProblem` inherits `ValueError` from `Error` and is used to supply custom error handling for future date exceptions
    
    ### Examples
    ```
    import datetime
    # define a function that checks for future dates
    def myfunc(mydate):
        # `mydate` is a date string
        try:
            mydate = datetime.date.fromisoformat(mydate)
            if mydate > datetime.date.today():
                raise FutureDateProblem
        except FutureDateProblem:
            myerror = FutureDateProblem()
            myerror.print_problem()
    # call function and supply a future date as an argument
    myfunc(mydate='5199-01-01')
    ```
    '''

    def __init__(self, problem_val:str):
        '''
        # Instantiate `MissingNodeException`

        Produces `self.msg` which is a str that is printed to console via `print_problem()` for interactive sessions

        ### `problem_val`; kwarg; str
            - Required
            - Node that failed validation and raised the `MissingNodeException`
            - Used to produce f-strings in `self.msg`
        '''
        self.msg = bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE + 'Process execution failed.\n' + bcolors.ENDC \
            + bcolors.FAIL + f'\n`{problem_val}`' + bcolors.FAIL + ' does not exist. \n'\
            + bcolors.OKBLUE + f'Enter a value for `{problem_val}` with ' + f'`set_{problem_val}()`' + bcolors.ENDC
        
    def _exit(self):
        sys.exit(1)


class MissingParent(Exception):
    '''
    # Sub-class of `Error` that handles Missing parent nodes

    ### `Error`; parent-class
        - `MissingParent` inherits `ValueError` from `Error` and is used to supply custom error handling for future date exceptions
    
    ### Examples
    ```
    import datetime
    # define a function that checks for future dates
    def myfunc(mydate):
        # `mydate` is a date string
        try:
            mydate = datetime.date.fromisoformat(mydate)
            if mydate > datetime.date.today():
                raise MissingParent
        except MissingParent:
            myerror = MissingParent()
            myerror.print_problem()
    # call function and supply a future date as an argument
    myfunc(mydate='5199-01-01')
    ```
    '''

    def __init__(self, problem_val:str):
        '''
        # Instantiate `MissingNodeException`

        Produces `self.msg` which is a str that is printed to console via `print_problem()` for interactive sessions

        ### `problem_val`; kwarg; str
            - Required
            - Node that failed validation and raised the `MissingNodeException`
            - Used to produce f-strings in `self.msg`
        '''
        self.msg = bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE + 'Process execution failed.\n' + bcolors.ENDC \
            + bcolors.FAIL + f'\n`{problem_val}`' + bcolors.FAIL + ' does not exist. \n'\
            + bcolors.OKBLUE + f'Enter a value for `{problem_val}` with ' + f'`set_{problem_val}()`' + bcolors.ENDC
    
    def _exit(self):
        sys.exit(1)

class StopError(AssertionError):
    def __init__(self):
        self.__cause__ = None