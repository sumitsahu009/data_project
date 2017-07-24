
class stringDatabase(object):  
    def __init__(self):
        pass
        
    def get_file(self):
        self.words= open('four_letters.txt').read().split()
        return self.words