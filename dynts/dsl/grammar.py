from dynts.dsl.ast import *

def p_expression_string(p):
    '''expression : QUOTE expression QUOTE'''
    p[0] = String(p[2])
    

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EQUAL expression
                  | expression CONCAT expression
                  | expression SPLIT expression'''
    v = p[2]
    if v == '+':
        p[0] = PlusOp(p[1],p[3])
    elif v == '-':
        p[0] = MinusOp(p[1],p[3])
    elif v == '*':
        p[0] = MultiplyOp(p[1],p[3])
    elif v == '/':
        p[0] = DivideOp(p[1],p[3])
    elif v == '=':
        p[0] = EqualOp(p[1],p[3])
    elif v == settings.concat_operator:
        p[0] = ConcatenationOp(p[1],p[3])
    elif v == settings.separator_operator:
        p[0] = SplittingOp(p[1],p[3])
    elif v == settings.field_operator:
        p[0] = Symbol(p[1], field = p[3])
        

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN
                  | LSQUARE expression RSQUARE'''
    v = p[1]
    if v == '(':
        p[0] = functionarguments(p[2])
    elif v == '[':
        p[0] = tsentry(p[2])


def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = Number(p[1][0])

    
def p_expression_id(p):
    '''expression : ID'''
    p[0] = Symbol(p[1])


def p_expression_id2(p):
    '''expression : ID ID'''
    p[0] = Symbol(p[1]+p[2])

    
def p_expression_id_number1(p):
    '''expression : NUMBER ID'''
    p[0] = Symbol('%s%s' % (p[1][1],p[2]))

    
def p_expression_id_number2(p):
    '''expression : ID NUMBER'''
    p[0] = Symbol('%s%s' % (p[1],p[2][1]))

    
def p_expression_function(p):
    '''expression : FUNCTION LPAREN expression RPAREN'''
    func = p[1]
    p[0] = Function(p[1],p[3],p[2],p[4])
    
    
def p_expression_bad_function(p):
    '''expression : FUNCTION LPAREN expression'''
    func = p[1]
    p[0] = BadExpression('Unclosed parenthesis for function {0}'.format(p[1]))
    
    
def p_expression_bad_function2(p):
    '''expression : ID LPAREN expression RPAREN'''
    p[0] = BadExpression(str(p[1]))


def p_expression_bad_function3(p):
    '''expression : ID LPAREN expression'''
    p[0] = BadExpression(str(p[1]))


def p_error(p):
    '''expression'''
    raise ExpressionError('Could not parse %s' % p)
    
