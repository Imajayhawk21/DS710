# Assignment 1 Unittests
# authors: silviana amethyst and Mckenzie West

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
# `pytest test_assignment1.py`
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
    assignment_number = "1" 
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

    def test_capitalized_correctly(self, student_code):
        assert student_code.first_name_capitalized == student_code.first_name_lowercase.capitalize(), "be sure to call the `.capitalize()` function to capitalize your first and last name"
        assert student_code.last_name_capitalized == student_code.last_name_lowercase.capitalize(), "be sure to call the `.capitalize()` function to capitalize your first and last name"

    def test_actually_used_dot_capitalize(self, submitted_source_code):
        assert "first_name_lowercase.capitalize()" in submitted_source_code, "don't manually capitalize.  use the `.capitalize()` function."
        assert "last_name_lowercase.capitalize()" in submitted_source_code, "don't manually capitalize.  use the `.capitalize()` function."

    def test_first_last_names_no_leading_trailing_space(self, student_code):
        assert student_code.first_name_lowercase == student_code.first_name_lowercase.strip(), "don't include any leading or trailing spaces in `first_name_lowercase`."
        assert student_code.last_name_lowercase == student_code.last_name_lowercase.strip(), "don't include any leading or trailing spaces in `last_name_lowercase`."

    def test_full_name_has_single_space(self, student_code):
        assert student_code.full_name == student_code.first_name_capitalized + ' ' + student_code.last_name_capitalized
        
    def test_full_name_has_no_leading_trailing_space(self, student_code):
        assert student_code.full_name == student_code.full_name.strip(), "variable `full_name` shouldn't include any leading or trailing whitespace."


    def test_name_pieces_is_list(self, student_code):
        assert isinstance(student_code.name_pieces, list), "variable `name_pieces` should be a list.  did you call the `.split()` function?"
        assert isinstance(student_code.name_pieces[0], str), "values in the `name_pieces` list should be strings"
        assert isinstance(student_code.name_pieces[1], str), "values in the `name_pieces` list should be strings"

    def test_split_correctly(self, student_code):
        assert student_code.name_pieces[0] == student_code.first_name_capitalized.split()[0]
        assert student_code.name_pieces[-1] == student_code.last_name_capitalized.split()[-1]
    













# task 2 tests





@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask2:

    def test_have_given_variables(self, student_code):

        assert student_code.lime_density_grams_per_cup == 248, "don't forget to copy in the given variables, exactly as given"
        assert student_code.grapefruit_density_grams_per_cup == 226.8, "don't forget to copy in the given variables, exactly as given"
        assert student_code.grams_per_pound == 453.592, "don't forget to copy in the given variables, exactly as given"
        assert student_code.oz_per_cup == 8, "don't forget to copy in the given variables, exactly as given"
        assert student_code.ml_per_oz == 29.574, "don't forget to copy in the given variables, exactly as given"




    def test_ml_per_cup(self, student_code):    
        assert abs(student_code.ml_per_cup - 236.592) < 1e-5

    def test_lime_density_grams_per_ml(self, student_code):    
        assert abs(student_code.lime_density_grams_per_ml - 1.0482180293501047) < 1e-5

    def test_lime_density_pounds_per_oz(self, student_code):    
        assert abs(student_code.lime_density_pounds_per_oz - 0.0683433570256971) < 1e-5

    def test_mixed_density_grams_per_cup(self, student_code):    
        assert abs(student_code.mixed_density_grams_per_cup - 237.4) < 1e-5

    def test_mixed_mass_grams(self, student_code):    
        assert abs(student_code.mixed_mass_grams - 178.05) < 1e-5

    def test_mixed_weight_pounds(self, student_code):    
        assert abs(student_code.mixed_weight_pounds - 0.3925333780137216) < 1e-5

    def test_mixed_density_pounds_per_oz(self, student_code):    
        assert abs(student_code.mixed_density_pounds_per_oz - 0.0654222296689536) < 1e-5





# task 3 tests

@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask3:

    # for more on `callable()`, see:
    # https://stackoverflow.com/questions/624926/how-do-i-detect-whether-a-python-variable-is-a-function
    def test_have_robot_message_function(self, student_code):
        assert callable(student_code.generate_robot_message), "make sure you copy in the `generate_robot_message` function"

    def test_didnt_modify_function_def(self, submitted_source_code):
        assert "def generate_robot_message(first_name, last_name, possible_messages_init, possible_messages_term):" in submitted_source_code, "copy in the generate_robot_message function, and don't modify the names of the function parameters"

    def test_capitalized_name_in_message(self, student_code):
        assert f'{student_code.first_name_capitalized} {student_code.last_name_capitalized}' in student_code.message_result, "your full capitalized name should appear in the generated message, with a space between first and last."


    def test_call_to_robot_message_function_is_as_expected(self, submitted_source_code):
        assert("generate_robot_message(first_name_capitalized, last_name_capitalized," in submitted_source_code), "i didn't see a call to the `generate_robot_message` function in your source code using your capitalized first and last name.  also, be sure that arguments to the generate_robot_message() function are separated by exactly one space after the comma."

    def test_capturing_result_of_robot_message(self, submitted_source_code):
        assert("message_result = generate_robot_message(" in submitted_source_code), "be sure to capture the result of the call to the `generate_robot_message` function, and call the resulting variable `message_result`.  also, put one space before and after the = sign."


    def test_message_result_is_str(self, student_code):
        assert isinstance(student_code.message_result, str)

    def test_added_options_to_lists_message_options(self, student_code):
        assert len(student_code.possible_messages_init)>4, "i don't think you added any options to the list of possible initial messages"
        assert len(student_code.possible_messages_term)>3, "i don't think you added any options to the list of possible terminal messages"



















