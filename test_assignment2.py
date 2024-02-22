# Assignment 2 Unit Tests
# authors: silviana amethyst and Mckenzie West
#
#
# This set of unit tests is provided to you as a student in DS710,
# to have a check on whether your code for the assignment
# passes some basic checks for correctness.
#
# This file must be executed from the same path
# as the code it's checking
#
# Note that passing all tests in this checker does *not* imply that you will
# receive a perfect score on the assignment. 
# 
# Your code is still manually graded for both style and correctness.
# The checkers only provide a starting point for the grading process.
#
# Important note:
# The right way to invoke this set of unit tests is 
#
# `pytest test_assignment2.py`
#
# this set of unit tests requires packages:
# * `pytest`


###################
# begin checker
######################





###########
#
# first, a bunch of infrastructure to get everything lined up correctly
#
########

def default_code_filename():
    assignment_number = "2" 
    return f"assignment{assignment_number}"

# some code to deal with filename extensions
def filename_checker(ext,name):
    if name.endswith(ext):
        return name
    else:
        if ext.startswith('.'):
            return name+ext
        else:
            return name+"."+ext

with_dotpy = lambda name: filename_checker('py',name)





# construct the expected filename
import sys

student_code_filename = None

if len(sys.argv)>2:

    for N in range(2,len(sys.argv)):
        argname = sys.argv[N]
        if argname.endswith('.py') and 'test_' not in argname:

            student_code_filename = argname[:-3] # strip off the `.py` with that there -3
            if student_code_filename.startswith('./'):
                student_code_filename = student_code_filename[2:]
            break

if not student_code_filename:
    student_code_filename = default_code_filename()


# a function that tells whether the indicated file actually exists
# used in conditional running of code below
def student_code_exists():

    try:
        with open(with_dotpy(student_code_filename), 'r', encoding='utf8') as f:
            return True
    except FileNotFoundError as e:
        raise FileNotFoundError(f"unable to read your code file to run unit tests.  Ensure that your code file is in the same folder as this checker, and that it's called `{with_dotpy(default_code_filename())}`")




import pytest



# the following "fixture" allows us to pass the imported library
# to tests later, and refer to the contents in the tests

# the stuff before the `yield` is essentially the setup code
# and the stuff after the `yield` is the teardown.

# see https://stackoverflow.com/questions/26405380/how-do-i-correctly-setup-and-teardown-for-my-pytest-class-with-tests
@pytest.fixture(scope='class')
def student_code():

    # up here in this function is setup code
    try:
        from importlib import import_module, reload

        try: # first, we try to reload, and if it fails then we'll regular load.
            # it's possible (probable) that a student is running this in Spyder, in which case
            # the previous instance of their assignment is still loaded,
            # and we need to REload to overwrite things

            sys.modules.pop(student_code_filename) # delete from the modules list.  might trigger the `except`.
            imported_student_code = import_module(student_code_filename) # might also trigger the `except`.
        except:
            # unable to reload, so we'll just do a fresh import
            imported_student_code = import_module(student_code_filename)


    except ImportError:
        raise ImportError(f"Bad import, or missing specified file {student_code_filename}.  Is your file named {student_code_filename}, and are you running this checker from the same location as {student_code_filename}?")

    print(f"testing code from file `{with_dotpy(student_code_filename)}`")


    # imported_student_code = pytest.importorskip(student_code_filename, reason=f"unable to import your code from file named {student_code_filename}")
    yield imported_student_code


    # teardown code goes here
    print("done with testing")




@pytest.fixture(scope='class')
def submitted_source_code():
    with open(with_dotpy(student_code_filename), 'r', encoding='utf8') as f:
        return f.read()

@pytest.fixture(scope='class')
def submitted_source_code_as_lines():
    with open(with_dotpy(student_code_filename), 'r', encoding='utf8') as f:
        return f.readlines()









############
#
# begin actual tests!!!!!!!!!!!!
#
#############





# universal tests


@pytest.fixture(scope='class',autouse=True)
def test_verify_no_re(submitted_source_code_as_lines):

    for line in submitted_source_code_as_lines:
        line_before_hash = line.split('#')[0]

        student_imported_re = False
        if "import re" in line_before_hash:
            import string
            loc = line_before_hash.find("import re")
            next_char = line_before_hash[loc+len("import re")]
            if next_char in string.whitespace:
                student_imported_re = True
                break

        if "from re import" in line_before_hash:
            student_imported_re = True
            break
        
        if "regex=True" in line_before_hash:
            student_imported_re = True
            break

    assert not student_imported_re, "It looks like you imported the regular expression library.  In this course, we do not allow the use of regular expressions."



@pytest.fixture(scope='class',autouse=True)
def test_verify_no_breakpoints(submitted_source_code_as_lines):
    '''Verifies that the student does not use a `breakpoint` which would stop the checker in its tracks.
    '''

    for line in submitted_source_code_as_lines:
        line_before_hash = line.split('#')[0]

        assert not ("breakpoint(" in line_before_hash) , "Please remove breakpoints from your code before submitting."


@pytest.fixture(scope='class',autouse=True)
def test_verify_no_hardcoded_paths(submitted_source_code_as_lines):
    '''
    Verifies the student does not use hardcoded paths in their submission, as they will not work on our computers.
    
    Here we verify that you are not including global paths to file locations.
    Note that this test will fail even if the line is commented.
    Make sure to delete all referenes to global paths before submitting.
    '''

    import string

    for line in submitted_source_code_as_lines:
        line_before_hash = line.split('#')[0]
        
        for A in string.ascii_uppercase:
            assert not (A+":/" in line_before_hash), "In this class we do not accept the use of hardcoded paths.  remove the hardcoded path and try again.  most tests were skipped until this issue is corrected."
        assert not ("/Users" in line_before_hash), "In this class we do not accept the use of hardcoded paths.  remove the hardcoded path and try again.  most tests were skipped until this issue is corrected."
        assert not ("/Volumes" in line_before_hash), "In this class we do not accept the use of hardcoded paths.  remove the hardcoded path and try again.  most tests were skipped until this issue is corrected."



@pytest.fixture(scope='class',autouse=True)
def test_verify_no_global_keyword(submitted_source_code_as_lines):
    '''
    Verifies that the student does not use `global`, which has the potential to break the checkers.
    '''
    for line in submitted_source_code_as_lines:
        line_before_hash = line.split('#')[0]

        assert not ("global " in line_before_hash), "Do not use the global keyword"


@pytest.fixture(scope='class',autouse=True)
def test_verify_no_input_function(submitted_source_code_as_lines):
    '''
    Verifies that the student does not use `input()`, which breaks computer-assisted grading.
    '''
    for line in submitted_source_code_as_lines:
        line_before_hash = line.split('#')[0]

        assert not ("input()" in line_before_hash), "Do not use the `input()` function"




@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask0:


    def test_has_first_last_name(self, student_code):
        '''
        checks if you have the variables `first_name` and `last_name`.
        it cannot possibly check if these are defined correctly,
        just that they are both strings.
        '''

        assert isinstance(student_code.first_name, str) and "please define the variable `first_name` in your source code"
        assert isinstance(student_code.last_name, str) and "please define the variable `last_name` in your source code"






# task 1 tests




# this suite is conditional on finding the code file specified.
#
# https://stackoverflow.com/questions/38966785/it-is-possible-to-skip-fail-test-in-setup-using-pytest
@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask1:


    def test_val_2_24_is_int(self, student_code):
        val_2_24 = student_code.val_2_24 # unpack
        assert isinstance(val_2_24,int), 'greatest power dividing should be an integer'
        
    def test_val_5_24_is_int(self, student_code):
        val_5_24 = student_code.val_5_24 # unpack
        assert isinstance(val_5_24,int), 'greatest power dividing should be an integer'
        
    def test_val_3_30_is_int(self, student_code):
        val_3_30 = student_code.val_3_30 # unpack
        assert isinstance(val_3_30,int), 'greatest power dividing should be an integer'
        
    def test_val_2_10540974080_is_int(self, student_code):
        val_2_10540974080 = student_code.val_2_10540974080 # unpack
        assert isinstance(val_2_10540974080,int), 'greatest power dividing should be an integer'


    def test_val_2_24_at_least_0(self, student_code):
        val_2_24 = student_code.val_2_24 # unpack
        assert val_2_24 >= 0, 'the greatest power dividing is always at least 0, since d^0 = 1, and 1 divides every number'
        
    def test_val_5_24_at_least_0(self, student_code):
        val_5_24 = student_code.val_5_24 # unpack
        assert val_5_24 >= 0, 'the greatest power dividing is always at least 0, since d^0 = 1, and 1 divides every number'
        
    def test_val_3_30_at_least_0(self, student_code):
        val_3_30 = student_code.val_3_30 # unpack
        assert val_3_30 >= 0, 'the greatest power dividing is always at least 0, since d^0 = 1, and 1 divides every number'
        
    def test_val_2_10540974080_at_least_0(self, student_code):
        val_2_10540974080 = student_code.val_2_10540974080 # unpack
        assert val_2_10540974080 >= 0, 'the greatest power dividing is always at least 0, since d^0 = 1, and 1 divides every number'






    def test_val_2_24_lower_bound(self, student_code):
        val_2_24 = student_code.val_2_24 # unpack
        assert val_2_24 > 2, 'your value for the greatest power dividing is too low'

    def test_val_2_24_upper_bound(self, student_code):
        val_2_24 = student_code.val_2_24 # unpack
        assert val_2_24 < 4, 'your value for the greatest power dividing is too high'



    def test_val_5_24_lower_bound(self, student_code):
        val_5_24 = student_code.val_5_24 # unpack
        assert val_5_24 >= 0, 'your value for the greatest power dividing is too low'

    def test_val_5_24_upper_bound(self, student_code):
        val_5_24 = student_code.val_5_24 # unpack
        assert val_5_24 < 1, 'your value for the greatest power dividing is too high'


    def test_val_3_30_lower_bound(self, student_code):
        val_3_30 = student_code.val_3_30 # unpack
        assert val_3_30 > 0, 'your value for the greatest power dividing is too low'

    def test_val_3_30_upper_bound(self, student_code):
        val_3_30 = student_code.val_3_30 # unpack
        assert val_3_30 < 2, 'your value for the greatest power dividing is too high'



    def test_val_2_10540974080_lower_bound(self, student_code):
        val_2_10540974080 = student_code.val_2_10540974080 # unpack
        assert val_2_10540974080 > 14, 'your value for the greatest power dividing is too low'

    def test_val_2_10540974080_upper_bound(self, student_code):
        val_2_10540974080 = student_code.val_2_10540974080 # unpack
        assert val_2_10540974080 < 16, 'your value for the greatest power dividing is too high'











@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask2:

    def test_num_primes_type(self, student_code):
        assert isinstance(student_code.num_primes, int), "`num_primes` should be an integer"

    def test_num_primes_positive(self, student_code):
        assert student_code.num_primes > 0, "there's at least one prime number between 1 and 999"


    def test_num_primes_lower_bound(self, student_code):
        assert student_code.num_primes > 167, "there are more than 167 primes in the range from 1 to 999"

    def test_num_primes_upper_bound(self, student_code):
        assert student_code.num_primes < 169, "there are fewer than 169 primes in the range from 1 to 999.  watch out, 1 is NOT prime."















@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask3:





    def test_given_values_500_5_100(self, student_code):
        """
        tests that the values of variables test_p500_r5_mp100_number_of_months, etc, have values as given in the assignment, for the $500, 5%, $100 case.
        """

        assert student_code.test_p500_r5_mp100_number_of_months == 6
        assert round(student_code.test_p500_r5_mp100_total_paid,2) == 506.35



    def test_given_values_500_5_100(self, student_code):
        """
        tests that the values of variables test_p500_r5_mp100_number_of_months, etc, have values as given in the assignment, for the $500, 5%, $500 case
        """

        assert student_code.test_p500_r5_mp500_number_of_months == 2
        assert round(student_code.test_p500_r5_mp500_total_paid,2) == 502.09







    def test_length_of_loan_type(self, student_code):
        assert isinstance(student_code.length_of_loan, int), "the number of months should be an integer"

    def test_length_of_loan_lower_bound(self, student_code):
        length_of_loan = student_code.length_of_loan
        assert length_of_loan > 538, "the total number of payments for $250,000 at 4%, with $1000 monthly payment, is greater than 538."

    def test_length_of_loan_upper_bound(self, student_code):
        length_of_loan = student_code.length_of_loan
        assert length_of_loan < 540, "the total number of payments for $250,000 at 4%, with $1000 monthly payment, is less than 540."

    def test_total_paid_lower_bound_1(self, student_code):
        """
        provides a loose lower/upper bound on the total paid for the $250,000, 4%, $1000 case.
        """
        total_paid = student_code.total_paid
        assert total_paid > 500000, "the total paid for $250,000 at 4%, with $1000 monthly payment, is greater than $500,000."

    def test_total_paid_lower_bound_2(self, student_code):
        """
        provides a medium lower/upper bound on the total paid for the $250,000, 4%, $1000 case.
        """        
        total_paid = student_code.total_paid
        assert total_paid > 538000, "the total paid for $250,000 at 4%, with $1000 monthly payment, is greater than $538000."

    def test_total_paid_lower_bound_3(self, student_code):
        """
        provides a reasonably tight(within a dollar) lower/upper bound on the total paid for the $250,000, 4%, $1000 case.

        the exact value is not coded in the pre-submission unit tests.
        """
        total_paid = student_code.total_paid
        assert total_paid > 538423.00, "the total paid for $250,000 at 4%, with $1000 monthly payment, is greater than $538423.00."

    def test_total_paid_upper_bound_1(self, student_code):
        """
        provides a loose lower/upper bound on the total paid for the $250,000, 4%, $1000 case.
        """
        total_paid = student_code.total_paid
        assert total_paid < 600000, "the total paid for $250,000 at 4%, with $1000 monthly payment, is less than $600000."

    def test_total_paid_upper_bound_2(self, student_code):
        """
        provides a medium lower/upper bound on the total paid for the $250,000, 4%, $1000 case.
        """
        total_paid = student_code.total_paid
        assert total_paid < 539000, "the total paid for $250,000 at 4%, with $1000 monthly payment, is less than $539000."

    def test_total_paid_upper_bound_3(self, student_code):
        """
        provides a reasonably tight(within a dollar) lower/upper bound on the total paid for the $250,000, 4%, $1000 case.

        the exact value is not coded in the pre-submission unit tests.
        """
        total_paid = student_code.total_paid
        assert total_paid < 538424.00, "the total paid for $250,000 at 4%, with $1000 monthly payment, is less than $538424.00."








