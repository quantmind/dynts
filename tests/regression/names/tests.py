import dynts
from dynts.conf import settings
from dynts.test import TestCase
from dynts.utils.populate import randomts


class names(TestCase):
    
    def testtsname(self):
        name = dynts.tsname('test')
        self.assertEqual(name,'test')
        name = dynts.tsname('test','ping','pong')
        self.assertEqual(name,'test__ping__pong')
        
    def testDataName(self):
        ts = randomts(100,3,name='test')
        self.assertEqual(ts.name,'test')
        self.assertEqual(ts.names(),['test','unnamed1','unnamed2'])
        ts.name = dynts.tsname('test','ping')
        self.assertEqual(ts.names(),['test','ping','unnamed1'])
        
    def testDataNameFull(self):
        names = dynts.tsname('test','ciao','ping')
        ts = randomts(100,3,name=names)
        self.assertEqual(ts.name,names)
        self.assertEqual(ts.names(),['test','ciao','ping'])
        
    def testComposedName(self):
        name  = dynts.composename('sqrt','test','ciao','ping')
        self.assertEqual(name,'sqrt(test)__sqrt(ciao)__sqrt(ping)')
        
    def testComposedNameComplex(self):
        name  = dynts.composename('ma','test','ciao','ping', window=30)
        self.assertEqual(name,'ma(test,window=30)__ma(ciao,window=30)__ma(ping,window=30)')
        
    
    