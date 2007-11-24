#!/usr/bin/python -O

import os, sys, tmcolorizer, re, glob

frag_re = re.compile("(?:--|#)start \*(?P<frag>[^\*]+)\*(.*)(?:--|#)end \*(?P=frag)\*", re.S)

def get_frags_from_file(srcfile):
    code = file(srcfile, "r").read()
    return get_frags_from_txt(code)   
    
def get_frags_from_txt(code):
    frags, insides = [], []
    all = frag_re.findall(code) + [("",""),]
    if all:
        frags, insides = zip(*all)
    for icode in [i for i in insides if i != ""]:
        tmpfrags = get_frags_from_txt(icode)
        for ifrag in [i for i in tmpfrags if i != ""]:
            frags = frags + tmpfrags
    return frags

def process_files(filelist):
    for srcfile in filelist:
        sys.stdout.write("Processing %s... \n" % srcfile)
        sys.stdout.flush()
        for frag in get_frags_from_file(srcfile):
            if frag:
                outname = srcfile + "." + frag.replace(" ","") + ".tm"
            else:
                outname = srcfile + ".tm"            
            try:
                tmsource = tmcolorizer.get_tmsource(srcfile, frag)
                tmfile = file("./tm/%s" % outname, "w+")
                tmfile.write(tmsource)
                tmfile.close()
                sys.stdout.write(".. %s\n" % outname)
                sys.stdout.flush()
            except tmcolorizer.EmptyFragmentError:
                pass
    sys.stdout.write("*** Done! ***\n")    

def main():
    process_files(glob.glob("*.py"))

if __name__ == "__main__":
    main()
