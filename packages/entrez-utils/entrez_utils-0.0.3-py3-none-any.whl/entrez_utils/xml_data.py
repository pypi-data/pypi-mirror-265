def cached_from_root(name, type_):
    def inner(self):
        if getattr(self, f"_{name}", None) is None:
            setattr(self, f"_{name}", type_(self.xml.getroot().attrib[name]))
        return getattr(self, f"_{name}")
    return inner

class XMLDataMetaclass(type):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for k, t in self.__annotations__.items():
            setattr(self, k, property(cached_from_root(k, t)))

class XMLDataObject(metaclass=XMLDataMetaclass):
    def __init__(self, xml, *attribs, **kwattribs):
        self.xml =  xml
        attrib_keys = list(type(self).__annotations__)
        for k, v in zip(attrib_keys, attribs):
            setattr(self, f"_{k}", v)
        for k, v in kwattribs.items():
            if k not in type(self).__annotations__:
                raise TypeError(
                    ("{}.__init__() got an unexpected keyword argument"
                     "{}").format(type(self), repr(k))
                )
            setattr(self, f"_{k}", v)
