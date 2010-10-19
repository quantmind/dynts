from dynts.dsl.ast.astbase import *

class BinMathOp(BinOp):
    
    def __init__(self,left,right,op):
        super(BinMathOp,self).__init__(left,right,op)
    
    def dooper(self, le, ri):
        raise NotImplementedError
    
    def _unwind(self, values, backend, full = False, **kwargs):
        le = self.left.unwind(values, backend, **kwargs)
        ri = self.right.unwind(values, backend, **kwargs)
        return self.dooper(le,ri)
    
    def lineardecomp(self):
        if isinstance(self.left,Number):
            if isinstance(self.right,Number):
                raise ValueError
            nv = self.left.value
            d1 = self.right.lineardecomp()
            dr = {}
            for k,v in d1.items():
                dr[k] = nv*v
            return dr
    

class PlusOp(BinMathOp):
    
    def __init__(self,left,right):
        BinMathOp.__init__(self,left,right,'+')
    
    def dooper(self, le, ri):
        return le+ri
    
    def lineardecomp(self):
        ls = self.left.lineardecomp()
        rs = self.right.lineardecomp()
        if ls and rs:
            lc = linearDecomp()
            lc.expand(ls).expand(rs)
            return lc
        else:
            return None
    
    
class MinusOp(BinMathOp):
    def __init__(self,left,right):
        BinMathOp.__init__(self,left,right,'-')

    def dooper(self, le, ri):
        return le-ri
    
    def lineardecomp(self):
        ls = self.left.lineardecomp()
        rs = self.right.lineardecomp()
        if ls and rs:
            lc = linearDecomp()
            lc.expand(ls).expand(rs.changesign())
            return lc
        else:
            return None
        
        
class MultiplyOp(BinMathOp):
    
    def __init__(self,left,right):
        BinMathOp.__init__(self,left,right,'*')
        
    def dooper(self, le, ri):
        return le*ri
    
    def lineardecomp(self):
        return linearDecomp().append(self)
    
    
class DivideOp(BinMathOp):
    
    def __init__(self,left,right):
        BinMathOp.__init__(self,left,right,'/')
        
    def dooper(self, le, ri):
        return le/ri
    
    def lineardecomp(self):
        return linearDecomp().append(self)

