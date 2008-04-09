#!/usr/bin/python -O

import re, os, sys, tempfile
from optparse import OptionParser
from os import path

def main():
    # ############################################ #
    #           Command Line Interface             #
    # ############################################ #
    
    parser = OptionParser(usage="usage: %prog [-f fragment] sourcefile.[py|c|ada]")
    parser.add_option("-f", "--fragment", dest="fragment", default="",
                      help="operate only on regex match")
    (options, args) = parser.parse_args()
    
    # ############################################ #
    #                Actual Program                #
    # ############################################ #
    
    for srcfile in args:
        try:
            print get_tmsource(srcfile, options.fragment)
        except EmptyFragmentError:
            sys.stderr.write("*** Empty Fragment processing %s\n" % srcfile)

class EmptyFragmentError(Exception):
    """Error processing an empty fragment"""

def get_tmsource(srcfile, fragment):
    code, mode, title = get_code_and_mode(srcfile)
    if fragment:
        try:
            code = get_section(code, fragment)
            title = title + " [%s]" % fragment
        except:
            raise EmptyFragmentError
    
    xml = get_highlight_output(code, mode)
    tmsource = xml2tm(xml, title, mode)
    return tmsource

def get_code_and_mode(srcfile):
    name, ext = path.splitext(srcfile)
    if ext in (".py"):
        mode = "py"
        title = "Python code: %s" % srcfile
    elif ext in (".pyx"):
        mode = "pyx"
        title = "Pyrex code: %s" % srcfile
    elif ext in (".adb",".ads",".ada",".ts"):
        mode = "ada"
        title = "Ada code: %s" % srcfile
    elif ext in (".c",".h",".cpp",".C"):
        mode = "c"
        title = "C code: %s" % srcfile
    elif ext in (".sh",".bash"):
        mode = "sh"
        title = "Bash code: %s" % srcfile
    else:
        mode = "c"
        title = "Code:"
    srcstream = file(srcfile)
    code = "\n".join(srcstream.readlines())
    srcstream.close()
    return code, mode, title
    
def get_section(code, fragment):
    regex = "(?:--|#)start \*%(fragment)s\*.*?\n(.*)\n.*(?:--|#)end \*%(fragment)s\*" % {"fragment": fragment}
    match = re.search(regex, code, re.S)
    try:
        return match.group(1)
    except:
        raise EmptyFragmentError, "Empty Fragment!!"

def get_highlight_output(code, mode):
    cmdline = "echo '%s' | highlight -f -Z -S %s" % (code, mode)
    postream_in, postream_out = os.popen2(cmdline, bufsize=4096)
    #postream_in.write(code)
    postream_in.close()
    xml = "\n".join(postream_out.readlines())
    postream_out.close()
    return xml

match_source = re.compile('\n*<[/]?source>\n*')
match_def = re.compile('<[/]?def>')
match_empty_tag = re.compile('<(?P<tag>[^>]*)></(?P=tag)>')
match_tag = re.compile('<(?P<tag>[^>]*)>(?P<data>[^<]*)</(?P=tag)>')
match_front_spaces = re.compile('\ {2,}')

def xml2tm(xml, title, mode):
    xml = match_empty_tag.sub("", xml)
    xml = match_source.sub("", xml)
    xml = match_def.sub("", xml)
    xml = match_tag.sub("<\g<tag>|\g<data>>", xml)
    
    def escape_spaces(match):
        res = match.group()
        res = '\ '.join(res.split(' '))
        return res
        
    xml = match_front_spaces.sub(escape_spaces, xml)
    xml = xml.replace("<br />","\n")
    xml = xml.replace("\n\n\n","\n\n\;\n")
    xml = xml.replace("&lt;","\<less\>")
    xml = xml.replace("&gt;","\<gtr\>")
    xml = xml.replace("&quot;","\"")
    xml = xml.replace("&amp;","&")
    
    tmsource = """<TeXmacs|1.0.5>
    
<\\body>

<\\%(mode)s-fragment|%(title)s>
%(code)s

</%(mode)s-fragment>

</body>
""" % {"code":xml,"title":title,"mode":mode}
    tmsource = tmsource.replace("\n\;\n","")
    return tmsource
    
if __name__ == "__main__":
    main()
