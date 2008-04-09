deps = [(1, (2,)), (2, (3,)), (3, (4,)), (4, (5,)), (5, (0,))]

def find_order(deps):
    i, c = 0, 0
    _len = len(deps)
    while i < _len:
        if set(deps[i][1]) & set([a for a, b in deps[i:]]):
            deps.append(deps.pop(i))
        else:
            i += 1
        c += 1
        if c > (_len*(_len+1))/2:
            return False
        print i, c, deps
    return deps


class Pkg:
    def __init__(self, name, depends=[]):
        self.name = name
        assert(type(depends) in (list, tuple))
        self.depends = depends
    def __cmp__(self, other):
        if self.name in other.depends:
            return -1
        elif other.name in self.depends:
            return 1
        else:
            return 0
    def __repr__(self):
        return "<Pkg:%s %s>" % (self.name, self.depends)

packages = []
for name, depends in deps:
    if depends == (0,):
        depends = []
    packages.append(Pkg(name, depends))
    
def findBuildOrder(packages):
    i, c = 0, 0
    _len = len(packages)
    while i < _len:
        if set(packages[i].depends) & set([p.name for p in packages[i:]]):
            packages.append(packages.pop(i))
        else:
            i += 1
        c += 1
        if c > (_len*(_len+1))/2:
            return False
        print i, c, packages
    return packages

print findBuildOrder(packages)

