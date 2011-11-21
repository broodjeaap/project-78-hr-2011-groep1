#!/bin/env python
#copyright ReportLab Inc. 2000
#see license.txt for license details
#history http://cvs.sourceforge.net/cgi-bin/cvsweb.cgi/reportlab/lib/logger.py?cvsroot=reportlab
#$Header: /cvsroot/reportlab/reportlab/lib/logger.py,v 1.5 2002/07/24 19:56:37 andy_robinson Exp $
__version__=''' $Id: logger.py,v 1.5 2002/07/24 19:56:37 andy_robinson Exp $ '''

from sys import stderr
class Logger:
    '''
    An extended file type thing initially equivalent to sys.stderr
    You can add/remove file type things; it has a write method
    '''
    def __init__(self):
        self._fps = [stderr]
        self._fns = {}

    def add(self,fp):
        '''add the file/string fp to the destinations'''
        if type(fp) is StringType:
            if fp in self._fns: return
            fp = open(fn,'wb')
            self._fns[fn] = fp
        self._fps.append(fp)

    def remove(self,fp):
        '''remove the file/string fp from the destinations'''
        if type(fp) is StringType:
            if fp not in self._fns: return
            fn = fp
            fp = self._fns[fn]
            del self.fns[fn]
        if fp in self._fps:
            del self._fps[self._fps.index(fp)]

    def write(self,text):
        '''write text to all the destinations'''
        if text[-1]!='\n': text=text+'\n'
        map(lambda fp,t=text: fp.write(t),self._fps)

    def __call__(self,text):
        self.write(text)

logger=Logger()

class WarnOnce:

    def __init__(self,kind='Warn'):
        self.uttered = {}
        self.pfx = '%s: '%kind
        self.enabled = 1

    def once(self,warning):
        if not self.uttered.has_key(warning):
            if self.enabled: logger.write(self.pfx + warning)
            self.uttered[warning] = 1

    def __call__(self,warning):
        self.once(warning)

warnOnce=WarnOnce()
infoOnce=WarnOnce('Info')