# Assignment 3a Unit Tests
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
# `pytest test_assignment3a.py`
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
    assignment_number = "3a" 
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

    ### first, task 1.1

    def test_have_is_prime(self, student_code):
        """
        checks that you have define a function called `is_prime`

        for more on `callable()`, see:
        https://stackoverflow.com/questions/624926/how-do-i-detect-whether-a-python-variable-is-a-function
        """
        assert callable(student_code.is_prime)


    def test_not_prime_0(self, student_code):
        is_prime = student_code.is_prime
        assert not is_prime(0)

    def test_not_prime_1(self, student_code):
        is_prime = student_code.is_prime
        assert not is_prime(1)

    def test_is_prime_2(self, student_code):
        is_prime = student_code.is_prime
        assert is_prime(2)

    def test_is_prime_3(self, student_code):
        is_prime = student_code.is_prime
        assert is_prime(3)

    def test_not_prime_10(self, student_code):
        is_prime = student_code.is_prime
        assert not is_prime(10)


    def test_not_prime_21(self, student_code):
        is_prime = student_code.is_prime
        assert not is_prime(21)


    def test_not_prime_21(self, student_code):
        is_prime = student_code.is_prime
        assert not is_prime(21)

    def test_is_prime_61(self, student_code):
        is_prime = student_code.is_prime
        assert is_prime(61)

    def test_is_prime_449(self, student_code):
        is_prime = student_code.is_prime
        assert is_prime(449)

    def test_not_prime_852(self, student_code):
        is_prime = student_code.is_prime
        assert not is_prime(852)





    # next, task 1.2, num_primes_to(n)
    def test_have_num_primes_to(self, student_code):
        """
        checks that you have define a function called `num_primes_to`

        for more on `callable()`, see:
        https://stackoverflow.com/questions/624926/how-do-i-detect-whether-a-python-variable-is-a-function
        """
        assert callable(student_code.num_primes_to)







    def test_num_primes_to_negative_5(self, student_code):
        num_primes_to = student_code.num_primes_to # unpack for next line
        assert num_primes_to(-5) == 0

    def test_num_primes_to_2(self, student_code):
        num_primes_to = student_code.num_primes_to # unpack for next line
        assert num_primes_to(2) == 1

    def test_num_primes_to_3(self, student_code):
        num_primes_to = student_code.num_primes_to # unpack for next line
        assert num_primes_to(3) == 2

    def test_num_primes_to_10(self, student_code):
        num_primes_to = student_code.num_primes_to # unpack for next line
        assert num_primes_to(10) == 4

    def test_num_primes_to_5(self, student_code):
        num_primes_to = student_code.num_primes_to # unpack for next line
        assert num_primes_to(5) == 3

    def test_num_primes_to_20(self, student_code):
        num_primes_to = student_code.num_primes_to # unpack for next line
        assert num_primes_to(20) == 8

    def test_num_primes_to_100(self, student_code):
        num_primes_to = student_code.num_primes_to # unpack for next line
        assert num_primes_to(100) == 25

    def test_num_primes_to_812(self, student_code):
        num_primes_to = student_code.num_primes_to # unpack for next line
        assert num_primes_to(812) == 141























@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask2:





    def test_have_valuation(self, student_code):
        assert callable(student_code.valuation)

    def test_can_call_valuation(self, student_code):
        valuation = student_code.valuation

        valuation(5,2)  # the divisor `d` comes second
        valuation(8,2)  # the divisor `d` comes second
        valuation(15,3)  # the divisor `d` comes second
        valuation(15,5) # the divisor `d` comes second

    def test_can_call_valuation_argnames(self, student_code):
        valuation = student_code.valuation

        valuation(n=5,d=2) # the arguments must be named `n` and `d`
        valuation(n=8,d=2) # the arguments must be named `n` and `d`
        valuation(n=15,d=3) # the arguments must be named `n` and `d`
        valuation(n=15,d=5) # the arguments must be named `n` and `d`




    def test_valuation_8_2(self, student_code):
        valuation = student_code.valuation
        assert valuation(8,2) == 3

    def test_valuation_8_3(self, student_code):
        valuation = student_code.valuation
        assert valuation(8,3) == 0

    def test_valuation_8_4(self, student_code):
        valuation = student_code.valuation
        assert valuation(8,4) == 1

    def test_valuation_50_2(self, student_code):
        valuation = student_code.valuation
        assert valuation(50,2) == 1

    def test_valuation_50_5(self, student_code):
        valuation = student_code.valuation
        assert valuation(50,5) == 2

    def test_valuation_50_3(self, student_code):
        valuation = student_code.valuation
        assert valuation(50,3) == 0

    def test_valuation_50_3_named(self, student_code):
        valuation = student_code.valuation
        assert valuation(n=50,d=3) == 0

    def test_valuation_192_2_named(self, student_code):
        valuation = student_code.valuation
        assert valuation(d=2,n=64*3) == 6









    def test_have_fizzbuzz_adv(self, student_code):
        assert callable(student_code.fizzbuzz_adv)

    def test_can_call_fizzbuzz_adv(self, student_code):
        fizzbuzz_adv = student_code.fizzbuzz_adv

        fizzbuzz_adv(5)
        fizzbuzz_adv(8)
        fizzbuzz_adv(15)
        fizzbuzz_adv(15)


    def test_can_call_fizzbuzz_adv_named(self, student_code):
        fizzbuzz_adv = student_code.fizzbuzz_adv

        fizzbuzz_adv(n=5) # the argument must be named `n`
        fizzbuzz_adv(n=8) # the argument must be named `n`
        fizzbuzz_adv(n=15) # the argument must be named `n`
        fizzbuzz_adv(n=15) # the argument must be named `n`



    def test_fizzbuzz_adv_3(self, student_code):    
        fizzbuzz_adv = student_code.fizzbuzz_adv # unpack
        assert fizzbuzz_adv(3) == "fizz1"

    def test_fizzbuzz_adv_25(self, student_code):        
        fizzbuzz_adv = student_code.fizzbuzz_adv # unpack
        assert fizzbuzz_adv(25) == "buzz2"

    def test_fizzbuzz_adv_75(self, student_code):        
        fizzbuzz_adv = student_code.fizzbuzz_adv # unpack
        assert fizzbuzz_adv(75) == "fizz1buzz2"

    def test_fizzbuzz_adv_1(self, student_code):        
        fizzbuzz_adv = student_code.fizzbuzz_adv # unpack
        assert fizzbuzz_adv(1) == ""

    def test_fizzbuzz_adv_pi(self, student_code):        
        fizzbuzz_adv = student_code.fizzbuzz_adv # unpack
        assert fizzbuzz_adv(3.1415) == "invalid"

    def test_fizzbuzz_adv_minus_15(self, student_code):        
        fizzbuzz_adv = student_code.fizzbuzz_adv # unpack
        assert fizzbuzz_adv(-15) == "invalid"


    def test_fizzbuzz_adv_positive_integers_given_valid(self, student_code):
        fizzbuzz_adv = student_code.fizzbuzz_adv # unpack so shorter lines

        assert fizzbuzz_adv(3) == "fizz1"
        assert fizzbuzz_adv(25) == "buzz2"
        assert fizzbuzz_adv(75) == "fizz1buzz2"

        assert fizzbuzz_adv(1) == ""

    def test_fizzbuzz_adv_zero_invalid(self, student_code):
        fizzbuzz_adv = student_code.fizzbuzz_adv # unpack so shorter lines
        assert fizzbuzz_adv(0) == "invalid"
        assert fizzbuzz_adv(-0) == "invalid"


    def test_fizzbuzz_adv_negative_integer_invalid(self, student_code):
        fizzbuzz_adv = student_code.fizzbuzz_adv # unpack so shorter lines
        assert fizzbuzz_adv(-1) == "invalid"
        assert fizzbuzz_adv(-3) == "invalid"
        assert fizzbuzz_adv(-5) == "invalid"
        assert fizzbuzz_adv(-15) == "invalid"
        assert fizzbuzz_adv(-127223) == "invalid"

    def test_fizzbuzz_adv_negative_float_invalid(self, student_code):
        fizzbuzz_adv = student_code.fizzbuzz_adv # unpack so shorter lines

        assert fizzbuzz_adv(-.0123) == "invalid"
        assert fizzbuzz_adv(-1.0123) == "invalid"
        assert fizzbuzz_adv(-234.0123) == "invalid"

    def test_fizzbuzz_adv_positive_float_invalid(self, student_code):
        fizzbuzz_adv = student_code.fizzbuzz_adv # unpack so shorter lines

        assert fizzbuzz_adv(.0123) == "invalid"
        assert fizzbuzz_adv(1.0123) == "invalid"
        assert fizzbuzz_adv(234.0123) == "invalid"

        import math
        pi = math.acos(-1)

        assert fizzbuzz_adv(pi) == "invalid"
        assert fizzbuzz_adv(-pi) == "invalid"




    def test_fizzbuzz_adv_more_hardcoded_examples_just_3_5(self, student_code):
        fizzbuzz_adv = student_code.fizzbuzz_adv # unpack so shorter lines

        assert fizzbuzz_adv(3**2) == f"fizz2"
        assert fizzbuzz_adv(5**2) == f"buzz2"

        assert fizzbuzz_adv(3**3) == f"fizz3"
        assert fizzbuzz_adv(5**3) == f"buzz3"


        assert fizzbuzz_adv(3**2 * 5**3) == f"fizz2buzz3"
        assert fizzbuzz_adv(3**4 * 5**3) == f"fizz4buzz3"

        assert fizzbuzz_adv(3**10 * 5**2) == f"fizz10buzz2"



    def test_fizzbuzz_adv_more_hardcoded_examples_extra_factors(self, student_code):

        fizzbuzz_adv = student_code.fizzbuzz_adv # unpack so shorter lines
        # now more, with other prime numbers thrown in

        assert fizzbuzz_adv(2*7* 3**2) == f"fizz2"
        assert fizzbuzz_adv(2*7* 5**2) == f"buzz2"

        assert fizzbuzz_adv(2*7* 3**3) == f"fizz3"
        assert fizzbuzz_adv(2*7* 5**3) == f"buzz3"


        assert fizzbuzz_adv(2*7* 3**2 * 5**3) == f"fizz2buzz3"
        assert fizzbuzz_adv(2*7* 3**4 * 5**3) == f"fizz4buzz3"

        assert fizzbuzz_adv(2*7* 3**10 * 5**2) == f"fizz10buzz2"












@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask3: 

    def test_have_minutes_to_midnight(self, student_code):
        assert callable(student_code.minutes_to_midnight)



    def test_can_call_zero_arguments(self, student_code):
        from datetime import datetime
        minutes_to_midnight = student_code.minutes_to_midnight
        minutes_to_midnight() # the 0-ary version



    def test_can_call_one_argument(self, student_code):
        from datetime import datetime
        minutes_to_midnight = student_code.minutes_to_midnight
        minutes_to_midnight( datetime.fromisoformat('2011-11-04T05:23:47') ) # takes one argument



    def test_explicit_now_matches(self, student_code):
        from datetime import datetime
        minutes_to_midnight = student_code.minutes_to_midnight
        assert minutes_to_midnight( datetime.now() ) == minutes_to_midnight( ) # calling with `now` should give same as not passing argument.  There's an edge case in this test -- if the two calls happen in different seconds, this will fail though the code is correct...  This should rarely happen, though.  


    def test_example_1(self, student_code):
        minutes_to_midnight = student_code.minutes_to_midnight
        from datetime import datetime
        assert minutes_to_midnight( datetime.fromisoformat('2011-11-04T00:05:23')) == 1434

    def test_example_2(self, student_code):
        minutes_to_midnight = student_code.minutes_to_midnight
        from datetime import datetime
        assert minutes_to_midnight( datetime.fromisoformat('2011-11-04T05:23:47')) == 1440 - 324

    def test_example_3(self, student_code):
        minutes_to_midnight = student_code.minutes_to_midnight
        from datetime import datetime
        assert minutes_to_midnight( datetime.fromisoformat('2011-11-04T23:59:00')) == 1

    def test_example_4(self, student_code):
        minutes_to_midnight = student_code.minutes_to_midnight
        from datetime import datetime
        assert minutes_to_midnight( datetime.fromisoformat('2011-11-04T23:59:01')) == 0

    def test_example_5(self, student_code):
        minutes_to_midnight = student_code.minutes_to_midnight
        from datetime import datetime
        assert minutes_to_midnight( datetime.fromisoformat('2011-11-04T23:59:59')) == 0

    def test_example_6(self, student_code):
        minutes_to_midnight = student_code.minutes_to_midnight
        from datetime import datetime
        assert minutes_to_midnight( datetime.fromisoformat('2011-11-04T00:00:00')) == 1440

    def test_example_7(self, student_code):
        minutes_to_midnight = student_code.minutes_to_midnight
        from datetime import datetime
        assert minutes_to_midnight( datetime.fromisoformat('2011-11-04T00:00:01')) == 1440-1








@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask4Amortization:

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
        length, total  = student_code.amortization(principal=100000, monthly_payment=100, annual_rate=0.05)



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





    def test_given_case_500_1_005_insufficient_payment_returns_none_none(self, student_code):
        """
        make sure that the tuple (None,None) is returned in the infinite case
        """

        amortization = student_code.amortization

        assert amortization(500, 1, 0.05) == (None,None) # this is an infinite loop case, should return None, None.



    def test_random_case(self, student_code):

        amortization = student_code.amortization

        assert amortization(128378,2181,0.0412)[0] ==  66 # the length
        assert round(amortization(128378,2181,0.0412)[1],2) ==  143660.79 # the length



