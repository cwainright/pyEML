"""A python source module to hold custom error classes for emld.py

Raises:
    ForceProblem: _description_
    VerboseProblem: _description_
    FutureDateProblem: _description_
"""

class Error(Exception):
    '''
    # Parent class for `Emld`-specific exceptions

    ### `Exception`; parent-class
        - `Error` is an `Emld` sub-class that inherits python's built-in `Exception` class that handles non-system-exiting try/except exceptions
        - `Error` inherits `Exception`'s sub-classes so they are available for custom `Emld` exception handling

    ### Examples
    ```
    class Error(Exception)
    class ForceProblem(Error)
    class VerboseProblem(Error)
    ```
    '''
    pass

class ForceProblem(Error):
    '''
    # Sub-class of `Error` that handles TypeErrors for parameter `force`

    ### `Error`; parent-class
        - `ForceProblem` inherits `TypeError` from `Error` and is used to supply custom error handling for parameter `force`
    ### Examples
    ```
    # define a function that takes parameter `force`
    def myfunc(force):
        try:
            if force not in (True, False): # define acceptable `force` arguments
                raise ForceProblem
        except ForceProblem:
            myerror = ForceProblem()
            myerror.print_problem()
    # call the function and supply a prohibited `force` argument
    myfunc(force=42)
    ```
    '''

    def __init__(self):
        '''
        # Instantiate `ForceProblem`

        Produces `self.msg` which is a str that is printed to console via `print_problem()` for interactive sessions
        '''
        self.msg = bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE + 'Process execution failed.' + bcolors.ENDC \
            + bcolors.FAIL + ' Parameter ' \
            + bcolors.OKBLUE + '`force` ' \
            + bcolors.FAIL + 'must be either ' \
            + bcolors.OKBLUE + bcolors.UNDERLINE + 'True' + bcolors.ENDC \
            + bcolors.FAIL + ' or ' + bcolors.ENDC \
            + bcolors.OKBLUE + bcolors.UNDERLINE + 'False' + bcolors.ENDC
    
    def print_problem(self):
        print(self.msg)

class VerboseProblem(Error):
    '''
    # Sub-class of `Error` that handles TypeErrors for parameter `verbose`

    ### `Error`; parent-class
        - `ForceProblem` inherits `TypeError` from `Error` and is used to supply custom error handling for parameter `verbose`

    ### Examples
    ```
    # define a function that takes parameter `verbose`
    def myfunc(verbose):
        try:
            if verbose not in (True, False): # define acceptable `verbose` arguments
                raise VerboseProblem
        except VerboseProblem:
            myerror = VerboseProblem()
            myerror.print_problem()
    # call the function and supply a prohibited `verbose` argument
    myfunc(verbose=42)
    ```
    '''

    def __init__(self):
        '''
        # Instantiate `VerboseProblem`

        Produces `self.msg` which is a str that is printed to console via `print_problem()` for interactive sessions
        '''
        self.msg = bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE + 'Process execution failed.' + bcolors.ENDC \
            + bcolors.FAIL + ' Parameter ' \
            + bcolors.OKBLUE + '`force` ' \
            + bcolors.FAIL + 'must be either ' \
            + bcolors.OKBLUE + bcolors.UNDERLINE + 'True' + bcolors.ENDC \
            + bcolors.FAIL + ' or ' + bcolors.ENDC \
            + bcolors.OKBLUE + bcolors.UNDERLINE + 'False' + bcolors.ENDC
    
    def print_problem(self):
        print(self.msg)

class FutureDateProblem(Error):
    '''
    # Sub-class of `Error` that handles ValueErrors future dates

    Some methods (e.g., `set_begin_date()`) accept dates as arguments and check whether the date is after today.
    A `FutureDateProblem` exception is raised when the argument fails that check.
    
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
        # Instantiate `FutureDateProblem`

        Produces `self.msg` which is a str that is printed to console via `print_problem()` for interactive sessions

        ### `problem_val`; kwarg; str
            - Required
            - The value (a date type-casted to str) that failed validation and raised the `FutureDateProblem`
            - Used to produce f-strings in `self.msg`
        '''
        self.problem_val = problem_val
        self.msg = bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE + 'Process execution failed.\n' + bcolors.ENDC \
            + bcolors.FAIL + '\n`date_string` entered: ' + bcolors.WARNING + f'{self.problem_val}' \
            + bcolors.FAIL + '\nParameter ' \
            + bcolors.OKBLUE + '`date_string` ' \
            + bcolors.FAIL + 'cannot be in the future.' + bcolors.ENDC
        
    def print_problem(self):
        print(f"{self.msg}")

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

class MissingNodeException(Error):
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
            + bcolors.FAIL + '\n`node`: ' + bcolors.WARNING + f'{problem_val}' \
            + bcolors.FAIL + '\ndoes not exist. ' \
            + bcolors.OKBLUE + 'Enter a value for this `node` with' \
            + f'`set_{problem_val}()`' + bcolors.ENDC
        