from numpy import asarray
from numpy import savetxt
from numpy import loadtxt


class Parking_lot:
    def __init__(self):
        self.storage = [-9223372036854775807]
        for i in range(101, 201):
            self.storage.append(i)
        self.capacity = len(self.storage)
        self.size = len(self.storage)
    
    def getParentIndex(self, index):
        return (index - 1) // 2
    
    def getLeftChildIndex(self, index):
        return 2 * index + 1
    
    def getRightChildIndex(self, index):
        return 2 * index + 2
    
    def hasParent(self, index):
        return self.getParentIndex(index) >= 0
    
    def hasLeftChild(self, index):
        return self.getLeftChildIndex(index) < self.size
    
    def hasRightChild(self, index):
        return self.getRightChildIndex(index) < self.size
    
    def parent(self, index):
        return self.storage[self.getParentIndex(index)]
    
    def leftChild(self, index):
        return self.storage[self.getLeftChildIndex(index)]
    
    def rightChild(self, index):
        return self.storage[self.getRightChildIndex(index)]
    
    def isFull (self):
        return self.size == self.capacity
    
    def swap(self, index1, index2):
        temp = self.storage[index1]
        self.storage[index1] = self.storage[index2]
        self.storage[index2] = temp
    
    def insert(self, data):
        if (self.isFull()):
            print("Heap is full")
        else:
            self.storage[self.size] = data
            self.size += 1
            self.heapifyUp()
    
    def heapifyUp(self):
        index = self.size - 1
        while(self.hasParent(index) and self.parent(index) > self.storage[index]):
            self.swap(self.getParentIndex(index), index)
            index = self.getParentIndex(index)
    
    def removeMin(self):
        if (self.size == 0):
            print("Empty heap")
        else:
            data = self.storage[0]
            self.storage[0] = self.storage[self.size - 1]
            self.size -= 1
            self.heapifyDown()
            return data
    
    def heapifyDown(self):
        index = 0
        while(self.hasLeftChild(index)):
            smallerChildIndex = self.getLeftChildIndex(index)
            if (self.hasRightChild(index) and self.rightChild(index) < self.leftChild(index)):
                smallerChildIndex = self.getRightChildIndex(index)
            if (self.storage[index] < self.storage[smallerChildIndex]):
                break
            else:
                self.swap(index, smallerChildIndex)
            index = smallerChildIndex

p1 = Parking_lot()

data = asarray(p1.storage)
# save to csv file
savetxt('data.csv', data, delimiter=',')

# load array
data = loadtxt('data.csv', delimiter=',')
# print the array
data1 = list(data)
data1 = [int(x) for x in data1]
print(data1)
print(type(data1))