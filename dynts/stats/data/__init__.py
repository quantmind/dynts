from decimal import Decimal


def topython(fname = 'qn'):
    f = open(fname+'.txt')
    r = f.read()
    f.close()
    rs = r.split('\n')
    pytxt = '%s = [' % fname
    vals  = []
    for r in rs:
        kv = r.split(' ')
        l  = []
        for k in kv:
            if k:
                d = Decimal(k)
                l.append(k)
        if len(l) != 2:
            break
        vals.append('      (%s)' % ', '.join(l))
    vals = ',\n'.join(vals)
    return '%s\n%s\n     ]' % (pytxt,vals)
    
    
    
if __name__ == '__main__':
    qn = topython('qn')
    qp = topython('qp')
    f = open('qpqn.py','w')
    qpqn = '%s\n\n%s' % (qp,qn)
    f.write(qpqn)
    f.close()