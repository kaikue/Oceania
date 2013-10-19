#Data structure for world chunks. Can add to beginning or end, and access from negative or positive indices.

class TwoWayList(object):
    
    def __init__(self):
        self.elements = []
        self.start = 0
        self.first = 0
        self.last = 0
    
    def append(self, element):
        self.elements.append(element)
        self.last += 1
    
    def prepend(self, element):
        self.elements.insert(0, element)
        self.start += 1
        self.first -= 1
    
    def get(self, index):
        return self.elements[index + self.start]
    
    def set(self, index, element):
        self.elements[index + self.start] = element

if __name__ == "__main__":
    l = TwoWayList()
    l.append("Zero")
    l.append("One")
    l.prepend("Negative One")
    print(l.get(-1))
    print(l.get(0))
    print(l.get(1))
    l.set(-1, "Negative Point Five")
    print(l.elements)
