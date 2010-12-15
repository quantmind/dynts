'''Test for rolling min/max/mean/median functions via DSL'''
import functions

class TestMeanFunction(functions.SimpleFunctionTest):
    function = 'ma'

class TestMaxFunction(functions.SimpleFunctionTest):
    function = 'max'
    
class TestMedFunction(functions.SimpleFunctionTest):
    function = 'med'

class TestMinFunction(functions.SimpleFunctionTest):
    function = 'min'
