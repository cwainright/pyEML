"""A python source module to hold custom error classes for emld.py"""

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
    """Custom error handling for missing xml nodes

    Args:
        Exception (class): parent class

    Examples:
        try:
            if node is None or len(node) == 0:
                    raise MissingNodeException(node_target)
        except MissingNodeException as e:
            print(e.msg)

    """
    def __init__(self, problem_val:str):
        """Produces `self.msg` which is a str that is printed to console via `print_problem()` for interactive sessions

        Args:
            problem_val (str): Node that failed validation and raised the `MissingNodeException`. Used to produce f-strings in `self.msg`.
        """
        
        self.msg = bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE + 'Process execution failed.\n' + bcolors.ENDC \
            + bcolors.FAIL + f'\n`{problem_val}`' + bcolors.FAIL + ' does not exist. \n'\
            + bcolors.OKBLUE + f'Enter a value for `{problem_val}` with ' + f'`set_{problem_val}()`' + bcolors.ENDC
        
class InvalidDataStructure(Exception):
    '''Custom error handling for invalid xml data structures

    Args:
        Exception (class): parent class
    
    Examples:
        try:
            mydata = [[[['my value']]]] # a deeply nested list will deparse erroneously to xml because there's no Element.tag information
            raise InvalidDataStructure('mydata')
        except InvalidDataStructure as e:
            print(e.msg)
    '''

    def __init__(self, problem_val:str):
        '''Produces `self.msg` which is a str that is printed to console via `print_problem()` for interactive sessions

        Args:
            problem_val (str): Node that failed validation and raised the `InvalidDataStructure`. Used to produce f-strings in `self.msg`.
        '''
        self.msg = bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE + 'Process execution failed.\n' + bcolors.ENDC \
            + bcolors.FAIL + f'\n`{problem_val}`' + bcolors.FAIL + ' does not exist. \n'\
            + bcolors.OKBLUE + f'Enter a value for `{problem_val}` with ' + f'`set_{problem_val}()`' + bcolors.ENDC

class AllBlanks(Exception):
    '''Custom error handling for creating empty class instances

    Args:
        Exception (class): parent class
    
    Examples:
        try:
            yourcreator = Creator()
            raise AllBlanks()
        except AllBlanks as e:
            print(e.msg)
    '''

    def __init__(self):
        '''Produces `self.msg` which is a str that is printed to console via `print_problem()` for interactive sessions

        Args:
            problem_val (str): Node that failed validation and raised the `InvalidDataStructure`. Used to produce f-strings in `self.msg`.
        '''
        self.msg = bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE + 'Process execution failed.\n' + bcolors.ENDC +\
            bcolors.FAIL + 'You entered blanks for all attributes. You must enter a value for at least one attribute. \n' + bcolors.ENDC
    