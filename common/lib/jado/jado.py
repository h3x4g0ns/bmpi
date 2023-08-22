class ArbitraryData:
    def __setattr__(self, key, value):
        if isinstance(value, dict):
            self.__dict__[key] = ArbitraryData.from_dict(value)
        else:
            self.__dict__[key] = value
        
    def __getattr__(self, key):
        return self.__dict__.get(key, None)

    def __repr__(self):
        return str(self.__dict__)

    @classmethod
    def from_dict(cls, data_dict):
        obj = cls()
        for key, value in data_dict.items():
            setattr(obj, key, value)
        return obj  # {'name': 'John', 'age': 25, 'country': 'USA', 'details': {'hobbies': ['reading', 'jogging'], 'address': {'street': 'Main St', 'number': 42}}}
