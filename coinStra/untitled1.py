class a:
    def __init__(self):
        global _global_dict
        _global_dict = {}
    
    def set_value(self,name, value):
        _global_dict[name] = value
    
    def get_value(name, defValue=None):
        try:
            return _global_dict[name]
        except KeyError:
            return defValue
        
class b:
    def __init__(self):
        global _global_dict
        self.d = _global_dict
        
    def set_value(name, value):
        _global_dict[name] = value
    
    def get_value(name, defValue=None):
        try:
            return _global_dict[name]
        except KeyError:
            return defValue
        
    def printf(self):
        print(self.d)
        
aa = a()
aa.set_value('first',1)
bb = b()
bb.printf()