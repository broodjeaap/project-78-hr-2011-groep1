#copyright ReportLab Inc. 2000
#see license.txt for license details
#history http://cvs.sourceforge.net/cgi-bin/cvsweb.cgi/reportlab/lib/abag.py?cvsroot=reportlab
#$Header: /cvsroot/reportlab/reportlab/lib/abag.py,v 1.8 2002/07/24 19:56:37 andy_robinson Exp $
__version__=''' $Id: abag.py,v 1.8 2002/07/24 19:56:37 andy_robinson Exp $ '''

class ABag:
    """
    'Attribute Bag' - a trivial BAG class for holding attributes.

    You may initialize with keyword arguments.
    a = ABag(k0=v0,....,kx=vx,....) ==> getattr(a,'kx')==vx

    c = a.clone(ak0=av0,.....) copy with optional additional attributes.
    """
    def __init__(self,**attr):
        for k,v in attr.items():
            setattr(self,k,v)

    def clone(self,**attr):
        n = apply(ABag,(),self.__dict__)
        if attr != {}: apply(ABag.__init__,(n,),attr)
        return n

    def __repr__(self):
        import string
        n = self.__class__.__name__
        L = [n+"("]
        keys = self.__dict__.keys()
        for k in keys:
            v = getattr(self, k)
            rk = repr(k)
            rv = repr(v)
            rk = "  "+string.replace(rk, "\n", "\n  ")
            rv = "    "+string.replace(rv, "\n", "\n    ")
            L.append(rk)
            L.append(rv)
        L.append(") #"+n)
        return string.join(L, "\n")

if __name__=="__main__":
    AB = ABag(a=1, c="hello")
    CD = AB.clone()
    print AB
    print CD