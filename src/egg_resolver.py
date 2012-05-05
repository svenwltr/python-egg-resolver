"""
This could be a possible alternative to virtual env. It is a small
&quot;bootstrap&quot; file, that takes care about loading the right egg files
in the pythonpath.
"""

__author__ = "Sven Walter <sven.walter@wltr.eu>"
__copyright__ = "Copyright 2012, Sven Walter"
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Sven Walter"
__email__ = "sven.walter@wltr.eu"
__date__ = "2012-05-05"
__url__ = "https://github.com/svenwltr/python-egg-resolver"


import os
import re
import sys

from distutils.version import StrictVersion


RE_FIND = re.compile(r"^(([\-\w]+)(<=?|>=?|==|!=)([\w\.]+))$", re.MULTILINE).match
PYTHON_VERSION = "%s.%s" % sys.version_info[0:2]


class EggResolveError(ImportError): pass

class EggResolver(object):

    @staticmethod
    def resolve(*args, **kwargs):
        return EggResolver(*args, **kwargs).start()

    def __init__(self, file_name=None, search_paths=None, throw_exception=False,
                 exit_code=None):
        self.throw_exception = throw_exception
        self.exit_code = exit_code or 1
        self.search_paths = search_paths or sys.path
        file_name = file_name or "requires.txt"
        
        self.file_path = os.path.join(os.path.dirname(__file__), file_name)
        
    
    def start(self):
        self.found_eggs = []
        self.filelist = []

        try:        
            self.build_filelist(self.search_paths)
            self.search_requirements(self.file_path)
        except EggResolveError, e:
            if self.throw_exception is True:
                raise e
            else:
                print >>sys.stderr, "ERROR: %s" % e.message
                sys.exit(self.exit_code)

        sys.path = sys.path[0:1] + self.found_eggs + sys.path[1:]
        
    
    def build_filelist(self, search_paths):
        for p in search_paths:
            if not os.path.exists(p): continue
            if not os.path.isdir(p): continue # TODO
    
            for f in os.listdir(p):
                if f.endswith('.egg'):
                    self.filelist.append(os.path.join(p, f))
                
                
    def search_requirements(self, file_path):
        lines = []
        with open(file_path) as f:
            for l in f:
                l = l.strip()
                m = RE_FIND(l)
                if m:
                    lines.append(m.groups())
                else:
                    print >>sys.stderr, 'WARNING: Line "%s" in line "%s" not identified!' % (l, file_path)
                
        for line, pkg, cmp, ver in lines: #@ReservedAssignment
            ver_need = StrictVersion(ver)
            
            for path in self.filelist:
                re_match = re.compile(r"^%s\-([\w\.]+)\-py%s\.egg$" % (re.escape(pkg),
                                                                     re.escape(PYTHON_VERSION))).match
                m = re_match(os.path.basename(path))
                if not m: continue
                
                ver_found = StrictVersion(m.group(1))
                
                if ((cmp == '==' and ver_found == ver_need) or
                    (cmp == '!=' and ver_found != ver_need) or
                    (cmp == '<=' and ver_found <= ver_need) or
                    (cmp == '>=' and ver_found >= ver_need) or
                    (cmp == '<' and ver_found < ver_need) or
                    (cmp == '>' and ver_found > ver_need)):
                    
                    self.found_eggs.append(path)
                    
                    sub = os.path.join(path, "EGG-INFO", 'requires.txt')
                    if os.path.exists(sub):
                        self.search_requirements(sub)
                    
                    break
            else:
                raise EggResolveError("Could not find an egg for %s'!" % line)
        

resolve = EggResolver.resolve