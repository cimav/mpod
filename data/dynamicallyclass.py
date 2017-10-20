'''
Created on Aug 18, 2017

@author: admin
'''

def add_list_attributes(klass):
    def new(cls, *args, **kwargs):
        result = super(cls, cls).__new__(cls)
        for attribute in klass.list_attributes:
            setattr(result, attribute, [])
        return result
    klass.__new__ = staticmethod(new)
    return klass

def addprop(inst, name, method):
  cls = type(inst)
  if not cls.hasattr('__perinstance'):
    cls = type(cls.__name__, (cls,), {})
    cls.__perinstance = True
  setattr(cls, name, property(method))

@addprop
@add_list_attributes
class Person(object):
    list_attributes = [
        'phone_numbers'
    ]
    def __init__(self):
        pass
    