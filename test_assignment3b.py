# Assignment 3b Unit Tests
# authors: silviana amethyst and  Mckenzie West
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
# `pytest test_assignment3b.py`
#
# this set of unit tests requires packages:
# * `pytest`

#


###################
# begin checker
######################





###########
#
# first, a bunch of infrastructure to get everything lined up correctly
#
########

def default_code_filename():
    assignment_number = "3b" 
    return f"assignment{assignment_number}"


# some code to deal with filename extensions
def checker_add_filename_extension(ext,name):
    if name.endswith(ext):
        return name
    else:
        if ext.startswith('.'):
            return name+ext
        else:
            return name+"."+ext

with_dotpy = lambda name: checker_add_filename_extension('py',name)





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











from pathlib import Path

def remove_file_if_exists(filename):
    Path(filename).unlink(missing_ok=True)


possible_generated_files = ['am_table_500_100_5_csv',
                            'am_table_500_100_5_csv.txt'
                            'am_table_500_100_5_tsv',
                            'am_table_500_100_5_tsv.txt'
                            'am_table_500_100_5_aligned',
                            'am_table_500_100_5_aligned.txt',
                            'exception_should_have_been_raised'
                            'exception_should_have_been_raised.txt']

for f in possible_generated_files:
    remove_file_if_exists(f)




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
class TestTask1IsPrime:


    def test_have_is_prime(self, student_code):
        assert callable(student_code.is_prime)

    def test_can_call(self, student_code):
        is_prime = student_code.is_prime

        is_prime(15)
        is_prime(100)
        is_prime(101)
        is_prime(7)
        is_prime(13)
        is_prime(97)


    def test_known_primes(self, student_code):
        is_prime = student_code.is_prime

        assert is_prime(2)
        assert is_prime(3)
        assert is_prime(5)
        assert is_prime(7)
        assert is_prime(11)
        assert is_prime(13)
        assert is_prime(97)
        assert is_prime(307)

    def test_known_not_primes(self, student_code):
        is_prime = student_code.is_prime

        assert not is_prime(1)
        assert not is_prime(4)
        assert not is_prime(8)
        assert not is_prime(15)
        assert not is_prime(525)
        assert not is_prime(11 * 13**2 * 29)

    def test_raises_if_not_positive_int___negative(self, student_code):
        is_prime = student_code.is_prime
        with pytest.raises(ValueError): # if this trips, you didn't raise correctly.  read this line in source to find the offending call
            is_prime(-1) # should raise a ValueError.  Input is an int, but value is unacceptable
            is_prime(-2) # should raise a ValueError.  Input is an int, but value is unacceptable
            is_prime(-5) # should raise a ValueError.  Input is an int, but value is unacceptable

    def test_raises_if_not_positive_int___zero(self, student_code):
        is_prime = student_code.is_prime
        with pytest.raises(ValueError):# if this trips, you didn't raise correctly.  read this line in source to find the offending call
            is_prime(0) # should raise a ValueError.  Input is an int, but value is unacceptable

    def test_raises_if_not_positive_int___pos_float(self, student_code):
        is_prime = student_code.is_prime
        with pytest.raises(TypeError):# if this trips, you didn't raise correctly.  read this line in source to find the offending call
            is_prime(1.22) # should raise a TypeError.  cannot operate on floats.
            is_prime(0.22) # should raise a TypeError.  cannot operate on floats.
            is_prime(1234.22) # should raise a TypeError.  cannot operate on floats.

    def test_raises_if_not_positive_int___neg_float(self, student_code):
        is_prime = student_code.is_prime
        with pytest.raises(TypeError):# if this trips, you didn't raise correctly.  read this line in source to find the offending call
            is_prime(-1.22) # should raise a TypeError.  cannot operate on floats.
            is_prime(-0.22) # should raise a TypeError.  cannot operate on floats.
            is_prime(-1234.22) # should raise a TypeError.  cannot operate on floats.



# task 2 tests

# this suite is conditional on finding the code file specified.
#
# https://stackoverflow.com/questions/38966785/it-is-possible-to-skip-fail-test-in-setup-using-pytest

@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask2FizzbuzzAdvanced:


    def test_have_function(self, student_code):
        assert callable(student_code.fizzbuzz_adv)


    def test_given_examples(self, student_code):
        fizzbuzz_adv = student_code.fizzbuzz_adv # unpack so shorter lines
        assert fizzbuzz_adv(3) == "fizz1"
        assert fizzbuzz_adv(25) == "buzz2"
        assert fizzbuzz_adv(75) == "fizz1buzz2"
        assert fizzbuzz_adv(1) == ""

    def test_given_examples_should_raise_zero(self, student_code):
        fizzbuzz_adv = student_code.fizzbuzz_adv # unpack so shorter lines
        
        with pytest.raises(ValueError):  # open the unit tests and read this line if this trips and you want to see the call that SHOULD have raised an exception.
            fizzbuzz_adv(0)



    def test_given_examples_should_raise_negative_integer(self, student_code):
        fizzbuzz_adv = student_code.fizzbuzz_adv # unpack so shorter lines
        
        with pytest.raises(ValueError):  # open the unit tests and read this line if this trips and you want to see the call that SHOULD have raised an exception.
            fizzbuzz_adv(-1)
            fizzbuzz_adv(-2)
            fizzbuzz_adv(-3)
            
    def test_given_examples_should_raise_positive_float(self, student_code):
        fizzbuzz_adv = student_code.fizzbuzz_adv # unpack so shorter lines
        
        with pytest.raises(TypeError):  # open the unit tests and read this line if this trips and you want to see the call that SHOULD have raised an exception.
            fizzbuzz_adv(.0123) # should raise a TypeError
            fizzbuzz_adv(1.0123) # should raise a TypeError
            fizzbuzz_adv(2.0123) # should raise a TypeError

    def test_given_examples_should_raise_negative_float(self, student_code):
        fizzbuzz_adv = student_code.fizzbuzz_adv # unpack so shorter lines
        
        with pytest.raises(TypeError):  # open the unit tests and read this line if this trips and you want to see the call that SHOULD have raised an exception.
            fizzbuzz_adv(-.0123) # should raise a TypeError
            fizzbuzz_adv(-1.0123) # should raise a TypeError
            fizzbuzz_adv(-2.0123) # should raise a TypeError




    def test_more_hardcoded_examples_one_factor(self, student_code):
        fizzbuzz_adv = student_code.fizzbuzz_adv # unpack so shorter lines

        assert fizzbuzz_adv(3**2) == f"fizz2"
        assert fizzbuzz_adv(5**2) == f"buzz2"

        assert fizzbuzz_adv(3**3) == f"fizz3"
        assert fizzbuzz_adv(5**3) == f"buzz3"


    def test_more_hardcoded_examples_two_factors(self, student_code):
        fizzbuzz_adv = student_code.fizzbuzz_adv # unpack so shorter lines
        assert fizzbuzz_adv(3**2 * 5**3) == f"fizz2buzz3"
        assert fizzbuzz_adv(3**4 * 5**3) == f"fizz4buzz3"

        assert fizzbuzz_adv(3**10 * 5**2) == f"fizz10buzz2"





    def test_more_hardcoded_examples_three_factors(self, student_code):
        fizzbuzz_adv = student_code.fizzbuzz_adv # unpack so shorter lines
        # now more, with other prime numbers thrown in

        assert fizzbuzz_adv(2*7* 3**2) == f"fizz2"
        assert fizzbuzz_adv(2*7* 5**2) == f"buzz2"

        assert fizzbuzz_adv(2*7* 3**3) == f"fizz3"
        assert fizzbuzz_adv(2*7* 5**3) == f"buzz3"



    def test_more_hardcoded_examples_many_factors(self, student_code):
        fizzbuzz_adv = student_code.fizzbuzz_adv # unpack so shorter lines

        assert fizzbuzz_adv(2*7* 3**2 * 5**3) == f"fizz2buzz3"
        assert fizzbuzz_adv(2*7* 3**4 * 5**3) == f"fizz4buzz3"

        assert fizzbuzz_adv(2*7* 3**10 * 5**2) == f"fizz10buzz2"







def islambda(testme):
    LAMBDA = lambda:0
    return isinstance(testme, type(LAMBDA)) and testme.__name__ == LAMBDA.__name__




@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask3FilenameFunction:


    def test_have_function(self, student_code):
        assert callable(student_code.add_filename_extension)



    def test_can_call_add_extension(self, student_code):
        '''Verifies `add_filename_extension('csv','file.csv')` runs.`'''
        add_filename_extension = student_code.add_filename_extension
        add_filename_extension('csv','file.csv') and "unable to call `add_filename_extension('csv','file.csv')`"





    def test_add_extension_py(self, student_code):
        '''Verifies that `add_filename_extension('py','file')` returns `'file.py'`'''
        add_filename_extension = student_code.add_filename_extension
        assert add_filename_extension('file','py') == 'file.py'


    def test_add_extension_csv(self, student_code):
        add_filename_extension = student_code.add_filename_extension
        assert add_filename_extension('my_csv','csv' ) == 'my_csv.csv'

    def test_add_extension_csv_with_dot(self, student_code):
        add_filename_extension = student_code.add_filename_extension
        assert add_filename_extension('my_csv','.csv' ) == 'my_csv.csv'



    def test_add_extension_csv_already_there(self, student_code):
        add_filename_extension = student_code.add_filename_extension
        assert add_filename_extension('my_csv.csv','csv')  == 'my_csv.csv'


    def test_add_extension_csv_already_there_with_dot(self, student_code):
        add_filename_extension = student_code.add_filename_extension
        assert add_filename_extension('my_csv.csv','.csv')  == 'my_csv.csv'


    def test_add_extension_py_different_already_there(self, student_code):
        add_filename_extension = student_code.add_filename_extension
        assert add_filename_extension('my_csv.csv','py')  == 'my_csv.csv.py'

    def test_add_extension_py_different_already_there_with_dot(self, student_code):
        add_filename_extension = student_code.add_filename_extension
        assert add_filename_extension('my_csv.csv','.py')  == 'my_csv.csv.py'



    def test_add_extension_csv_already_there_several_times(self, student_code):
        add_filename_extension = student_code.add_filename_extension
        assert add_filename_extension('my_csv.csv.csv','csv')  == 'my_csv.csv.csv'

    def test_add_extension_csv_already_there_several_times_with_dot(self, student_code):
        add_filename_extension = student_code.add_filename_extension
        assert add_filename_extension('my_csv.csv.csv','.csv')  == 'my_csv.csv.csv'















    def test_add_txt_is_lambda(self, student_code):
        '''Verifies that `add_txt` is a lambda.'''
        add_txt = student_code.add_txt

        assert islambda(add_txt), '`add_txt` must be a lambda'


    def test_add_csv_is_lambda(self, student_code):
        '''Verifies that `add_csv` is a lambda.'''

        add_csv = student_code.add_csv

        assert islambda(add_csv), '`add_csv` must be a lambda'








    def test_add_txt_already_had(self, student_code):
        '''Verifies that `add_txt('file.txt')` returns `'file.txt'`.'''
        add_txt = student_code.add_txt

        assert add_txt('file.txt') == 'file.txt'

    def test_add_txt_not_already_there(self, student_code):
        '''Verifies that `add_txt('file')` returns `'file.txt'`.'''
        add_txt = student_code.add_txt

        assert add_txt('file') == 'file.txt'


    def test_add_txt_already_had_twice(self, student_code):
        '''Verifies that `add_txt('file.txt.txt')` returns `'file.txt.txt'`.'''
        add_txt = student_code.add_txt

        assert add_txt('file.txt.txt') == 'file.txt.txt'


    def test_add_txt_already_had_diff_ext(self, student_code):
        '''Verifies that `add_txt('file.csv')` returns `'file.csv.txt'`.'''
        add_txt = student_code.add_txt

        assert add_txt('file.csv') == 'file.csv.txt'


    def test_add_txt_already_had_diff_ext_twice(self, student_code):
        '''Verifies that `add_txt('file.csv.txt')` returns `'file.csv.txt'`.'''
        add_txt = student_code.add_txt

        assert add_txt('file.csv.txt') == 'file.csv.txt'




    def test_add_csv_already_had(self, student_code):
        '''Verifies that `add_csv('file.csv')` returns `'file.csv'`.'''
        add_csv = student_code.add_csv

        assert add_csv('file.csv') == 'file.csv'

    def test_add_csv_not_already_there(self, student_code):
        '''Verifies that `add_csv('file')` returns `'file.csv'`.'''
        add_csv = student_code.add_csv

        assert add_csv('file') == 'file.csv'


    def test_add_csv_already_had_twice(self, student_code):
        '''Verifies that `add_csv('file.csv.csv')` returns `'file.csv.csv'`.'''
        add_csv = student_code.add_csv

        assert add_csv('file.csv.csv') == 'file.csv.csv'


    def test_add_csv_already_had_diff_ext_twice(self, student_code):
        '''Verifies that `add_csv('file.mp4')` returns `'file.mp4.csv'`.'''
        add_csv = student_code.add_csv

        assert add_csv('file.mp4') == 'file.mp4.csv'

    def test_add_csv_already_had_diff_ext_twice(self, student_code):
        '''Verifies that `add_csv('file.mp4.csv')` returns `'file.mp4.csv'`.'''
        add_csv = student_code.add_csv

        assert add_csv('file.mp4.csv') == 'file.mp4.csv'










@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask4AmortizationNoFile:



    def test_have_function(self, student_code):
        assert callable(student_code.amortization)



    def test_can_call_no_names(self, student_code):
        """
        test that one can call the required function
        """
        length, total  = student_code.amortization(100000, 500, .05)



    def test_can_call_with_names(self, student_code):
        """
        test that one can call the required function
        """
        length, total  = student_code.amortization(principal=100000, monthly_payment=417, annual_rate=0.05) # this should not generate an exception!!



    def test_given_case_500_500_005(self, student_code):
        amortization = student_code.amortization

        assert amortization(500, 500, 0.05)[0] == 2
        assert round(amortization(500, 500, 0.05)[1],2) == round(502.09,2)
        




    def test_given_case_100000_500_005_length(self, student_code):
        amortization = student_code.amortization

        assert amortization(100000, 500, 0.05)[0] == 431

    

    def test_given_case_100000_500_005_total(self, student_code):
        amortization = student_code.amortization

        assert round(amortization(100000, 500, 0.05)[1],2) == round(215458.84,2)      




    def test_given_case_500_100_005_length(self, student_code):
        amortization = student_code.amortization

        length, total = amortization(principal=500, monthly_payment=100, annual_rate=0.05)
        assert length == 6


    def test_given_case_500_100_005_total(self, student_code):
        amortization = student_code.amortization

        length, total = amortization(principal=500, monthly_payment=100, annual_rate=0.05)
        assert round(total,2) == 506.35





    def test_given_case_500_1_005_insufficient_payment_raises(self, student_code):
        """
        make sure that the tuple (None,None) is returned in the infinite case
        """

        amortization = student_code.amortization
        with pytest.raises(ValueError):  # open the unit tests and read this line if this trips and you want to see the call that SHOULD have raised an exception.
            amortization(500, 1, 0.05) # this is an infinite loop case, should `raise`
            amortization(50000, 1, 0.05) # this is an infinite loop case, should `raise`
            amortization(5000000, 1, 0.05) # this is an infinite loop case, should `raise`



    def test_random_case(self, student_code):

        amortization = student_code.amortization

        assert amortization(128378,2181,0.0412)[0] ==  66 # the length
        assert round(amortization(128378,2181,0.0412)[1],2) ==  143660.79 # the length






@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask4AmortizationFormattingFunctions:



    def test_have_format_csv(self, student_code):
        assert callable(student_code.format_csv)

    def test_format_csv_header(self, student_code):
        format_csv = student_code.format_csv
        assert format_csv("Month","Payment","Interest","Balance") == "Month,Payment,Interest,Balance\n"


    def test_format_csv_numbers(self, student_code):
        format_csv = student_code.format_csv
        assert format_csv(3,100.123123,12.1778212,20192.1029873) == "3,100.12,12.18,20192.1\n"






    def test_have_format_tsv(self, student_code):
        assert callable(student_code.format_tsv)

    def test_format_tsv_header(self, student_code):
        format_tsv = student_code.format_tsv
        assert format_tsv("Month","Payment","Interest","Balance") == "Month\tPayment\tInterest\tBalance\n"


    def test_format_tsv_numbers(self, student_code):
        format_tsv = student_code.format_tsv
        assert format_tsv(3,100.123123,12.1778212,20192.1029873) == "3\t100.12\t12.18\t20192.1\n"




    def test_have_format_tsv(self, student_code):
        assert callable(student_code.format_tsv)

    def test_format_tsv_header(self, student_code):
        format_tsv = student_code.format_tsv
        assert format_tsv("Month","Payment","Interest","Balance") == "Month\tPayment\tInterest\tBalance\n"


    def test_format_tsv_numbers(self, student_code):
        format_tsv = student_code.format_tsv
        assert format_tsv(3,100.123123,12.1778212,20192.1029873) == "3\t100.12\t12.18\t20192.1\n"




    def test_have_format_aligned(self, student_code):
        assert callable(student_code.format_aligned)

    def test_format_aligned_header(self, student_code):
        format_aligned = student_code.format_aligned
        'assert format_aligned("Month","Payment","Interest","Balance") == "  Month      Payment     Interest      Balance\n"'


    def test_format_aligned_numbers(self, student_code):
        format_aligned = student_code.format_aligned
        assert format_aligned(3,129.1823, 10192.1010192, 31.98989) == "      3       129.18     10192.10        31.99\n"







# amortization(500,100,0.05,"am_table_500_100_5_csv", format_csv)
# amortization(500,100,0.05,"am_table_500_100_5_tsv", format_tsv)
# amortization(500,100,0.05,"am_table_500_100_5_aligned", format_aligned)



@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask4AmortizationYesFileCSV:



    def test_have_function(self, student_code):
        assert callable(student_code.amortization)



    def test_can_call_no_names(self, student_code):
        """
        test that one can call the required function
        """
        format_csv = student_code.format_csv

        length, total  = student_code.amortization(100000, 500, .05, 'table')
        length, total  = student_code.amortization(100000, 500, .05, 'table', format_csv)



    def test_can_call_with_names(self, student_code):
        """
        test that one can call the required function
        """
        format_csv = student_code.format_csv

        length, total  = student_code.amortization(principal=100000, monthly_payment=417, annual_rate=0.05, filename='table') # this should not generate an exception!!
        length, total  = student_code.amortization(principal=100000, monthly_payment=417, annual_rate=0.05, filename='table', format_function=format_csv) # this should not generate an exception!!



    def test_given_case_500_100_005_produces_file(self, student_code):
        amortization = student_code.amortization


        amortization(500, 100, 0.05, 'am_table_500_100_5_csv')
        assert Path('am_table_500_100_5_csv.txt').exists() and "your code should have generated a .txt file"

        
    def test_given_case_500_100_005_file_contents_correct(self, student_code):
        amortization = student_code.amortization

        amortization(500, 100, 0.05, 'am_table_500_100_5_csv')
        
        with open('am_table_500_100_5_csv.txt','r') as file:
            as_lines = file.readlines()
            assert len(as_lines) == 7 # includes one for the blank line at the end

            as_lines[0] == 'Month,Payment,Interest,Balance'
            as_lines[1] == '1,100,2.08,402.08'
            as_lines[2] == '2,100,1.68,303.76'
            as_lines[3] == '3,100,1.27,205.02'
            as_lines[4] == '4,100,0.85,105.88'
            as_lines[5] == '5,100,0.44,6.32'
            as_lines[6] == '6,6.35,0.03,0.0'


        with open('am_table_500_100_5_csv.txt','r') as file:
            contents = file.read()
            assert contents.endswith('\n')




    def test_given_case_500_1_005_insufficient_payment_raises(self, student_code):
        """
        make sure that the tuple (None,None) is returned in the infinite case
        """

        amortization = student_code.amortization
        with pytest.raises(ValueError):  # open the unit tests and read this line if this trips and you want to see the call that SHOULD have raised an exception.
            amortization(500, 1, 0.05, "exception_should_have_been_raised") # this is an infinite loop case, should `raise`
            amortization(50000, 1, 0.05, "exception_should_have_been_raised") # this is an infinite loop case, should `raise`
            amortization(5000000, 1, 0.05, "exception_should_have_been_raised") # this is an infinite loop case, should `raise`

            amortization(500, 1, 0.05, "exception_should_have_been_raised.txt") # this is an infinite loop case, should `raise`
            amortization(50000, 1, 0.05, "exception_should_have_been_raised.txt") # this is an infinite loop case, should `raise`
            amortization(5000000, 1, 0.05, "exception_should_have_been_raised.txt") # this is an infinite loop case, should `raise`


        assert not Path("exception_should_have_been_raised").exists() and "in the infinite loop case, no file should be created"
        assert not Path("exception_should_have_been_raised.txt").exists() and "in the infinite loop case, no file should be created"






    def test_given_case_500_1_005_insufficient_payment_raises_with_function_name(self, student_code):
        """
        make sure that the tuple (None,None) is returned in the infinite case
        """

        amortization = student_code.amortization
        format_csv = student_code.format_csv

        with pytest.raises(ValueError):  # open the unit tests and read this line if this trips and you want to see the call that SHOULD have raised an exception.
            amortization(500, 1, 0.05, "exception_should_have_been_raised", format_csv) # this is an infinite loop case, should `raise`
            amortization(50000, 1, 0.05, "exception_should_have_been_raised", format_csv) # this is an infinite loop case, should `raise`
            amortization(5000000, 1, 0.05, "exception_should_have_been_raised", format_csv) # this is an infinite loop case, should `raise`

            amortization(500, 1, 0.05, "exception_should_have_been_raised.txt", format_csv) # this is an infinite loop case, should `raise`
            amortization(50000, 1, 0.05, "exception_should_have_been_raised.txt", format_csv) # this is an infinite loop case, should `raise`
            amortization(5000000, 1, 0.05, "exception_should_have_been_raised.txt", format_csv) # this is an infinite loop case, should `raise`


        assert not Path("exception_should_have_been_raised").exists() and "in the infinite loop case, no file should be created"
        assert not Path("exception_should_have_been_raised.txt").exists() and "in the infinite loop case, no file should be created"





















@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask4AmortizationYesFileTSV:



    def test_have_function(self, student_code):
        assert callable(student_code.amortization)



    def test_can_call_no_names(self, student_code):
        """
        test that one can call the required function
        """
        format_tsv = student_code.format_tsv

        length, total  = student_code.amortization(100000, 500, .05, 'table')
        length, total  = student_code.amortization(100000, 500, .05, 'table', format_tsv)



    def test_can_call_with_names(self, student_code):
        """
        test that one can call the required function
        """
        format_tsv = student_code.format_tsv

        length, total  = student_code.amortization(principal=100000, monthly_payment=417, annual_rate=0.05, filename='table') # this should not generate an exception!!
        length, total  = student_code.amortization(principal=100000, monthly_payment=417, annual_rate=0.05, filename='table', format_function=format_tsv) # this should not generate an exception!!



    def test_given_case_500_100_005_produces_file(self, student_code):
        amortization = student_code.amortization
        format_tsv = student_code.format_tsv

        amortization(500, 100, 0.05, 'am_table_500_100_5_tsv', format_tsv)
        assert Path('am_table_500_100_5_tsv.txt').exists() and "your code should have generated a .txt file"

        
    def test_given_case_500_100_005_file_contents_correct(self, student_code):
        amortization = student_code.amortization
        format_tsv = student_code.format_tsv

        amortization(500, 100, 0.05, 'am_table_500_100_5_tsv', format_tsv)
        
        with open('am_table_500_100_5_tsv.txt','r') as file:
            as_lines = file.readlines()
            assert len(as_lines) == 7 # includes one for the blank line at the end

            as_lines[0] == 'Month\tPayment\tInterest\tBalance'
            as_lines[1] == '1\t100\t2.08\t402.08'
            as_lines[2] == '2\t100\t1.68\t303.76'
            as_lines[3] == '3\t100\t1.27\t205.02'
            as_lines[4] == '4\t100\t0.85\t105.88'
            as_lines[5] == '5\t100\t0.44\t6.32'
            as_lines[6] == '6\t6.35\t0.03\t0.0'


        with open('am_table_500_100_5_tsv.txt','r') as file:
            contents = file.read()
            assert contents.endswith('\n')







    def test_given_case_500_1_005_insufficient_payment_raises_with_function_name(self, student_code):
        """
        make sure that the tuple (None,None) is returned in the infinite case
        """

        amortization = student_code.amortization
        format_tsv = student_code.format_tsv
        
        with pytest.raises(ValueError):  # open the unit tests and read this line if this trips and you want to see the call that SHOULD have raised an exception.
            amortization(500, 1, 0.05, "exception_should_have_been_raised", format_tsv) # this is an infinite loop case, should `raise`
            amortization(50000, 1, 0.05, "exception_should_have_been_raised", format_tsv) # this is an infinite loop case, should `raise`
            amortization(5000000, 1, 0.05, "exception_should_have_been_raised", format_tsv) # this is an infinite loop case, should `raise`

            amortization(500, 1, 0.05, "exception_should_have_been_raised.txt", format_tsv) # this is an infinite loop case, should `raise`
            amortization(50000, 1, 0.05, "exception_should_have_been_raised.txt", format_tsv) # this is an infinite loop case, should `raise`
            amortization(5000000, 1, 0.05, "exception_should_have_been_raised.txt", format_tsv) # this is an infinite loop case, should `raise`


        assert not Path("exception_should_have_been_raised").exists() and "in the infinite loop case, no file should be created"
        assert not Path("exception_should_have_been_raised.txt").exists() and "in the infinite loop case, no file should be created"

        remove_file_if_exists("exception_should_have_been_raised")
        remove_file_if_exists("exception_should_have_been_raised.txt")












@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask4AmortizationYesFileAligned:



    def test_have_function(self, student_code):
        assert callable(student_code.amortization)



    def test_can_call_no_names(self, student_code):
        """
        test that one can call the required function
        """
        format_aligned = student_code.format_aligned

        length, total  = student_code.amortization(100000, 500, .05, 'table')
        length, total  = student_code.amortization(100000, 500, .05, 'table', format_aligned)



    def test_can_call_with_names(self, student_code):
        """
        test that one can call the required function
        """
        format_aligned = student_code.format_aligned

        length, total  = student_code.amortization(principal=100000, monthly_payment=417, annual_rate=0.05, filename='table') # this should not generate an exception!!
        length, total  = student_code.amortization(principal=100000, monthly_payment=417, annual_rate=0.05, filename='table', format_function=format_aligned) # this should not generate an exception!!



    def test_given_case_500_100_005_produces_file(self, student_code):
        amortization = student_code.amortization
        format_aligned = student_code.format_aligned

        amortization(500, 100, 0.05, 'am_table_500_100_5_aligned', format_aligned)
        assert Path('am_table_500_100_5_aligned.txt').exists() and "your code should have generated a .txt file"

        
    def test_given_case_500_100_005_file_contents_correct(self, student_code):
        amortization = student_code.amortization
        format_aligned = student_code.format_aligned

        amortization(500, 100, 0.05, 'am_table_500_100_5_aligned', format_aligned)
        
        with open('am_table_500_100_5_aligned.txt','r') as file:
            as_lines = file.readlines()
            assert len(as_lines) == 7 # includes one for the blank line at the end

            as_lines[0] == '  Month      Payment     Interest      Balance'
            as_lines[1] == '      1       100.00         2.08       402.08'
            as_lines[2] == '      2       100.00         1.68       303.76'
            as_lines[3] == '      3       100.00         1.27       205.02'
            as_lines[4] == '      4       100.00         0.85       105.88'
            as_lines[5] == '      5       100.00         0.44         6.32'
            as_lines[6] == '      6         6.35         0.03         0.00'


        with open('am_table_500_100_5_aligned.txt','r') as file:
            contents = file.read()
            assert contents.endswith('\n')









    def test_given_case_500_1_005_insufficient_payment_raises_with_function_name(self, student_code):
        """
        make sure that the tuple (None,None) is returned in the infinite case
        """

        amortization = student_code.amortization
        format_aligned = student_code.format_aligned
        
        with pytest.raises(ValueError):  # open the unit tests and read this line if this trips and you want to see the call that SHOULD have raised an exception.
            amortization(500, 1, 0.05, "exception_should_have_been_raised", format_aligned) # this is an infinite loop case, should `raise`
            amortization(50000, 1, 0.05, "exception_should_have_been_raised", format_aligned) # this is an infinite loop case, should `raise`
            amortization(5000000, 1, 0.05, "exception_should_have_been_raised", format_aligned) # this is an infinite loop case, should `raise`

            amortization(500, 1, 0.05, "exception_should_have_been_raised.txt", format_aligned) # this is an infinite loop case, should `raise`
            amortization(50000, 1, 0.05, "exception_should_have_been_raised.txt", format_aligned) # this is an infinite loop case, should `raise`
            amortization(5000000, 1, 0.05, "exception_should_have_been_raised.txt", format_aligned) # this is an infinite loop case, should `raise`


        assert not Path("exception_should_have_been_raised").exists() and "in the infinite loop case, no file should be created"
        assert not Path("exception_should_have_been_raised.txt").exists() and "in the infinite loop case, no file should be created"

        remove_file_if_exists("exception_should_have_been_raised")
        remove_file_if_exists("exception_should_have_been_raised.txt")


