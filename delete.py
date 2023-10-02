import sqlite3
from numpy import asarray
from numpy import savetxt
from numpy import loadtxt
import sys

class MinHeap:
    def __init__(self, data):
        self.maxsize = 110
        self.size = len(data)
        self.Heap = data
        self.FRONT = 1
 
    # Function to return the position of
    # parent for the node currently
    # at pos
    def parent(self, pos):
        return pos//2
 
    # Function to return the position of
    # the left child for the node currently
    # at pos
    def leftChild(self, pos):
        return 2 * pos
 
    # Function to return the position of
    # the right child for the node currently
    # at pos
    def rightChild(self, pos):
        return (2 * pos) + 1
 
    # Function that returns true if the passed
    # node is a leaf node
    def isLeaf(self, pos):
        if pos >= (self.size//2) and pos <= self.size:
            return True
        return False
 
    # Function to swap two nodes of the heap
    def swap(self, fpos, spos):
        self.Heap[fpos], self.Heap[spos] = self.Heap[spos], self.Heap[fpos]
 
    # Function to heapify the node at pos
    def minHeapify(self, pos):
 
        # If the node is a non-leaf node and greater
        # than any of its child
        if not self.isLeaf(pos):
            if (self.Heap[pos] > self.Heap[self.leftChild(pos)] or
               self.Heap[pos] > self.Heap[self.rightChild(pos)]):
 
                # Swap with the left child and heapify
                # the left child
                if self.Heap[self.leftChild(pos)] < self.Heap[self.rightChild(pos)]:
                    self.swap(pos, self.leftChild(pos))
                    self.minHeapify(self.leftChild(pos))
 
                # Swap with the right child and heapify
                # the right child
                else:
                    self.swap(pos, self.rightChild(pos))
                    self.minHeapify(self.rightChild(pos))
 
    # Function to insert a node into the heap
    def insert(self, element):
        if self.size >= self.maxsize :
            print("Heap id full")
        self.size+= 1
        self.Heap.append(element)
 
        current = self.size - 1
 
        while self.Heap[current] < self.Heap[self.parent(current)]:
            self.swap(current, self.parent(current))
            current = self.parent(current)
 
    # Function to build the min heap using
    # the minHeapify function
    def minHeap(self):
 
        for pos in range(self.size//2, 0, -1):
            self.minHeapify(pos)
 
    # Function to remove and return the minimum
    # element from the heap
    def remove(self):
 
        popped = self.Heap[self.FRONT]
        self.Heap[self.FRONT] = self.Heap[self.size - 1]
        self.size-= 1
        self.minHeapify(self.FRONT)
        return popped



def deleteSqliteTableRow(plate_number):
    try:
        sqliteConnection = sqlite3.connect('db.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_delete_query = """Delete from Vehicle_Parkings where plate_number = ?"""
        data = (plate_number,)
        cursor.execute(sql_delete_query, data)
        sqliteConnection.commit()
        print("Record Deleted successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete sqlite table record", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def readSqliteTable(plate_number):
    try:
        sqliteConnection = sqlite3.connect('db.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT parking_spot from Vehicle_Parkings where plate_number = ?"""
        cursor.execute(sqlite_select_query, (plate_number,))
        spot = int(cursor.fetchone()[0])
        print("Record Deleted successfully ")
        cursor.close()
        return spot

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def delete(plate_number):
    data = loadtxt('data.csv', delimiter=',')
    data_list = list(data)
    data_list = [int(x) for x in data_list]

    pl = MinHeap(data_list)
    spot = readSqliteTable(plate_number)
    pl.insert(spot)
    deleteSqliteTableRow(plate_number)


    # save to csv file
    data = asarray(pl.Heap)
    savetxt('data.csv', data, delimiter=',')

    data = loadtxt('data.csv', delimiter=',')
    # print the array
    data1 = list(data)
    data1 = [int(x) for x in data1]
    print(data1)