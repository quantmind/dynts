from timeseries import *
from dsl import *
from dataprovider import *
from testdynts import *
from testflot import *
from testop import *
from testcrossection import *
from test_datastructures import *

#from tsdev import *

import functions

class TestMeanFunction(functions.SimpleFunctionTest):
    function = 'ma'

class TestMaxFunction(functions.SimpleFunctionTest):
    function = 'max'
    
class TestMedFunction(functions.SimpleFunctionTest):
    function = 'med'

class TestMinFunction(functions.SimpleFunctionTest):
    function = 'min'
