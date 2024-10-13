import types
class A:
    def f(self, func):
        self.f = func

a = A()
print(isinstance(a.f, types.MethodType)) # True

b = A()
@b.f
def g():
    pass
print(isinstance(b.f, types.MethodType)) # False