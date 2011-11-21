#!/bin/env python
#copyright ReportLab Inc. 2000
#see license.txt for license details
#history http://cvs.sourceforge.net/cgi-bin/cvsweb.cgi/reportlab/lib/fonts.py?cvsroot=reportlab
#$Header: /cvsroot/reportlab/reportlab/lib/fonts.py,v 1.15 2002/11/16 18:56:42 andy_robinson Exp $
__version__=''' $Id: fonts.py,v 1.15 2002/11/16 18:56:42 andy_robinson Exp $ '''
import string, sys, os
###############################################################################
#   A place to put useful font stuff
###############################################################################
#
#      Font Mappings
# The brute force approach to finding the correct postscript font name;
# much safer than the rule-based ones we tried.
# preprocessor to reduce font face names to the shortest list
# possible.  Add any aliases you wish; it keeps looking up
# until it finds no more translations to do.  Any input
# will be lowercased before checking.
_family_alias = {
            'serif':'times',
            'sansserif':'helvetica',
            'monospaced':'courier',
            'arial':'helvetica'
            }
#maps a piddle font to a postscript one.
_tt2ps_map = {
            #face, bold, italic -> ps name
            ('times', 0, 0) :'Times-Roman',
            ('times', 1, 0) :'Times-Bold',
            ('times', 0, 1) :'Times-Italic',
            ('times', 1, 1) :'Times-BoldItalic',

            ('courier', 0, 0) :'Courier',
            ('courier', 1, 0) :'Courier-Bold',
            ('courier', 0, 1) :'Courier-Oblique',
            ('courier', 1, 1) :'Courier-BoldOblique',

            ('helvetica', 0, 0) :'Helvetica',
            ('helvetica', 1, 0) :'Helvetica-Bold',
            ('helvetica', 0, 1) :'Helvetica-Oblique',
            ('helvetica', 1, 1) :'Helvetica-BoldOblique',
  
            # TTF fonts
            ('timesnew', 0, 0) :'Times New Roman',
            ('timesnew', 1, 0) :'Times New Roman-Bold',
            ('timesnew', 0, 1) :'Times New Roman-Italic',
            ('timesnew', 1, 1) :'Times New Roman-BoldItalic',
 
            ('courier new', 0, 0) :'Courier New',
            ('courier new', 1, 0) :'Courier New-Bold',
            ('courier new', 0, 1) :'Courier New-Italic',
            ('courier new', 1, 1) :'Courier New-BoldItalic',

            ('verdana', 0, 0) :'Verdana',
            ('verdana', 1, 0) :'Verdana-Bold',
            ('verdana', 0, 1) :'Verdana-Italic',
            ('verdana', 1, 1) :'Verdana-BoldItalic',
 
            ('arial', 0, 0) :'Arial',
            ('arial', 1, 0) :'Arial-Bold',
            ('arial', 0, 1) :'Arial-Italic',
            ('arial', 1, 1) :'Arial-BoldItalic',
 
            ('arialnarrow', 0, 0) :'Arial Narrow',
            ('arialnarrow', 1, 0) :'Arial Narrow-Bold',
            ('arialnarrow', 0, 1) :'Arial Narrow-Italic',
            ('arialnarrow', 1, 1) :'Arial Narrow-BoldItalic',
 
            ('bookmanos', 0, 0) :'Bookman Old Style',
            ('bookmanos', 1, 0) :'Bookman Old Style-Bold',
            ('bookmanos', 0, 1) :'Bookman Old Style-Italic',
            ('bookmanos', 1, 1) :'Bookman Old Style-BoldItalic',
 
            ('georgia', 0, 0) :'Georgia',
            ('georgia', 1, 0) :'Georgia-Bold',
            ('georgia', 0, 1) :'Georgia-Italic',
            ('georgia', 1, 1) :'Georgia-BoldItalic',
 
            ('trebuchet', 0, 0) :'Trebuchet MS',
            ('trebuchet', 1, 0) :'Trebuchet MS-Bold',
            ('trebuchet', 0, 1) :'Trebuchet MS-Italic',
            ('trebuchet', 1, 1) :'Trebuchet MS-BoldItalic',

            # there is only one Symbol font
            ('symbol', 0, 0) :'Symbol',
            ('symbol', 1, 0) :'Symbol',
            ('symbol', 0, 1) :'Symbol',
            ('symbol', 1, 1) :'Symbol',

            # ditto for dingbats
            ('zapfdingbats', 0, 0) :'ZapfDingbats',
            ('zapfdingbats', 1, 0) :'ZapfDingbats',
            ('zapfdingbats', 0, 1) :'ZapfDingbats',
            ('zapfdingbats', 1, 1) :'ZapfDingbats',
            }

_ps2tt_map={}
for k,v in _tt2ps_map.items():
    if not _ps2tt_map.has_key(k):
        _ps2tt_map[string.lower(v)] = k

def ps2tt(psfn):
    'ps fontname to family name, bold, italic'
    psfn = string.lower(psfn)
    if _ps2tt_map.has_key(psfn):
        return _ps2tt_map[psfn]
    raise ValueError, "Can't map PS font %s" % psfn

def tt2ps(fn,b,i):
    'family name + bold & italic to ps font name'
    K = (string.lower(fn),b,i)
    if _tt2ps_map.has_key(K):
        return _tt2ps_map[K]
    else:
        fn, b1, i1 = ps2tt(K[0])
        K = fn, b1|b, i1|i
        if _tt2ps_map.has_key(K):
            return _tt2ps_map[K]
    raise ValueError, "Can't map TT font %s" % fn

def addMapping(face, bold, italic, psname):
    'allow a custom font to be put in the mapping -- ONLY IF NOT ALREADY PRESENT!'
    k = (string.lower(face), bold, italic)
    if not _tt2ps_map.has_key(k):
        _tt2ps_map[k] = psname
        # rebuild inverse - inefficient
        for k,v in _tt2ps_map.items():
            if not _ps2tt_map.has_key(k):
                _ps2tt_map[string.lower(v)] = k
    elif _tt2ps_map[k]!=psname:
        raise ValueError, "_tt2ps_map[%s]==%s already, not %s" % (repr(k), _tt2ps_map[k], psname)