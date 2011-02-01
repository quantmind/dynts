from dynts.conf import settings
import ply.lex as lex


class rules(object):
    
    # Regular expression rules for simple tokens
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_LSQUARE = r'\['
    t_RSQUARE = r'\]'
    t_EQUAL   = r'\='
    t_QUOTE   = r'\"'
    t_CONCAT  = r'\%s' % settings.concat_operator
    t_SPLIT   = r'\%s' % settings.separator_operator

    def __init__(self, oper = None):
        self.lexer = None
        self.oper  = oper or {}
        
    def reserved(self):
        return {}
    
    def __get_tokens(self):
        re = self.reserved()
        tokens = [
              'NUMBER',
              'PLUS',
              'MINUS',
              'TIMES',
              'DIVIDE',
              'LPAREN',
              'RPAREN',
              'LSQUARE',
              'RSQUARE',
              'EQUAL',
              'CONCAT',
              'SPLIT',
              'QUOTE',
              'ID',
              'FUNCTION'
              ] + re.values() 
        return tokens
    tokens = property(fget = __get_tokens)
    
    def __get_precedence(self):
        return (('left','QUOTE'),
                ('left','SPLIT'),
                ('left','CONCAT'),
                ('left','EQUAL'),
                ('left','PLUS','MINUS'),
                ('left','TIMES','DIVIDE'),
                )
    precedence = property(fget = __get_precedence)

    # A regular expression rule with some action code
    def t_NUMBER(self, t):
        r'([0-9]+\.?[0-9]*|\.[0-9]+)([eE](\+|-)?[0-9]+)?'
        try:
            sv = t.value
            v = float(sv)
            iv = int(v)
            t.value = (iv if iv == v else v,sv)
        except ValueError:
            print("Number %s is too large!" % t.value)
            t.value = 0
        return t

    def t_ID(self, t):
        r'`[^`]*`|[a-zA-Z_][a-zA-Z_0-9:@]*'
        res    = self.oper.get(t.value, None) # Check for reserved words (operations)
        if res == None:
            res = t.value.upper()
            if res == 'FALSE':
                r.type = 'BOOL'
                r.value = False
            elif res == 'TRUE':
                r.type = 'BOOL'
                r.value = True
            else:
                t.type = 'ID'
        else:
            t.value = res
            t.type  = 'FUNCTION'
        return t
    
    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        
    # Error handling rule
    def t_error(self, t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)
    
    def build(self, **kwargs):
        self.lexer = lex.lex(object=self, **kwargs)

    def input(self, data):
        self.lexer.input(data)
    

