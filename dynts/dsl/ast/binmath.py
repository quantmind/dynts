from dynts.dsl.ast.astbase import *

class BinMathOp(BinOp):
    
    def __init__(self,left,right,op):
        super(BinMathOp,self).__init__(left,right,op)
    
    def dooper(self, le, ri, unwind):
        if isinstance(self.left,Number) and isinstance(self.right,Number):
            return unwind.numberData(self.simpleoper(le,ri))
        else:
            return unwind.tsData(data = self.complexoper(le,ri), label = str(self))
    
    def _unwind(self, values, unwind, full = False, **kwargs):
        le = self.left.unwind(values, unwind, **kwargs)
        ri = self.right.unwind(values, unwind, **kwargs)
        res = self.dooper(le.data,ri.data, unwind)
        if full:
            res.applyoper()
        return res
    
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
    
    def simpleoper(self,le,ri):
        pass
    
    def complexoper(self,le,ri):
        return self.simpleoper(le,ri)
            
    

class PlusOp(BinMathOp):
    
    def __init__(self,left,right):
        BinMathOp.__init__(self,left,right,'+')
    
    def simpleoper(self, le, ri):
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

    def simpleoper(self, le, ri):
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
        
    def simpleoper(self, le, ri):
        return le*ri
    
    def lineardecomp(self):
        return linearDecomp().append(self)
    
    
class DivideOp(BinMathOp):
    
    def __init__(self,left,right):
        BinMathOp.__init__(self,left,right,'/')
        
    def simpleoper(self, le, ri):
        return le/ri
    
    def lineardecomp(self):
        return linearDecomp().append(self)

