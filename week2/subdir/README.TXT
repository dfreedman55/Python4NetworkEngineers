In this method, you must get 'pwd' for the current directory and add this to the 
PYTHONPATH environment variable as follows:

env | grep PYTHONPATH
export PYTHONPATH=/path/to/dir/here
python
import pprint
import sys
pprint.pprint(sys.path)		# /path/to/dir/here should be reflected in the output
exit()

mv ../exercise1c_my_func.py .
python exercise1c_a_new_python_script.py
