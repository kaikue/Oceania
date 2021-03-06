#Data structure for world chunks. Can add to beginning or end, and access from negative or positive indices.

class TwoWayList(object):
    
    def __init__(self, elements=None, start=0):
        if elements is None:
            self.elements = []
        else:
            self.elements = elements
        self.update_start(start)
    
    def append(self, element):
        self.elements.append(element)
        self.end += 1
    
    def prepend(self, element):
        self.elements.insert(0, element)
        self.update_start(self.start + 1)
    
    def get(self, index):
        return self.elements[index + self.start]
    
    def get_range(self, start, end):
        return TwoWayList(self.elements[start + self.start:end + self.start], start)
    
    def set(self, index, element):
        self.elements[index + self.start] = element
    
    def contains_index(self, index):
        return self.first <= index and index < self.end
    
    def update_start(self, start):
        self.start = start
        self.first = -start
        self.end = len(self.elements) + self.first
    
    def clone(self):
        clone = TwoWayList()
        for e in self.elements:
            clone.append(e)
        clone.update_start(self.start)
        return clone
    
    def __str__(self):
        s = "Start: " + str(self.start) + ", first: " + str(self.first) + ", end: " + str(self.end) + " ["
        for element in self.elements:
            s += str(element) + ", "
        s = s[:len(s) - 2]
        s += "]"
        return s
    
    def __len__(self):
        return len(self.elements)

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
    print(l.contains_index(0))
    print(l.contains_index(-1))
    print(l.contains_index(1))
    print(l.contains_index(-2))
    print(l.contains_index(2))