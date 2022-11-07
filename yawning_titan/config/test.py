from dataclasses import dataclass
from yawning_titan.config.config_group_class import ConfigGroupABC

def myprop(x, doc):
    def getx(self):
        return getattr(self, '_' + x)

    def setx(self, val):
        setattr(self, '_' + x, val)

    def delx(self):
        delattr(self, '_' + x)

    return property(getx, setx, delx, doc)
    
@dataclass
class C(ConfigGroupABC):
    a:int = myprop("a", "Hi, I'm A!")
    b:int = myprop("b", "Hi, I'm B!")

    @classmethod
    def create(cls):
        c = C(a=1,b=2)
        return c

    @classmethod
    def _validate(cls):
        pass

print(C.b.__doc__)
c = C.create()
print(C.b.__doc__)