# ------------------------------ Initialization ------------------------------ #
import copy
import pprint
import time

f = open("test2.txt", "r")
text = f.read()
arr = [[]]
lines = text.split('\n')
arr = [list(x.strip()) for x in lines]
print(arr)
class Algo:
    def __init__(self, arr):
        self.arr = [[ord(item) - ord('A') for item in rows] for rows in arr]
        self.ans = arr
        self.coordinate = list()
        self.num_regions = max(max(row) for row in self.arr)
        self.region = list(False for i in range(self.num_regions + 1))
        self.rows = len(arr)
        self.cols = len(arr[0])
        self.visited = [[False for i in range(self.cols)] for j in range(self.rows)]

    def checkInputValid(self):
        if(self.num_regions >= self.rows or self.num_regions >= self.cols): return False

    def checkOutputValid(self):
        coordinates = self.coordinate
        if coordinates == []: return False
        if len(coordinates) != self.num_regions + 1: return False
        for i in range(len(coordinates)):
            for j in range(i + 1, len(coordinates)):
                if(coordinates[i][0] == coordinates[j][0]): return False
                if(coordinates[i][1] == coordinates[j][1]): return False
                if(abs(coordinates[i][0] - coordinates[j][0]) == 1 and abs(coordinates[i][1] - coordinates[j][1]) == 1): return False
                # if(abs(coordinates[i][0] - coordinates[j][0]) == abs(coordinates[i][1] - coordinates[j][1])): return False
        return True

    def solve(self, region_idx):
        if(region_idx > self.num_regions):
            return self.checkOutputValid()
        
        ans = self.ans
        region = self.region
        coordinates = self.coordinate
        for i in range(self.rows):
            for j in range(self.cols):
                if(self.arr[i][j] == region_idx):
                    ans[i][j] = "X"
                    region[self.arr[i][j]] = True
                    coordinates.append([i, j])

                    if self.solve(region_idx+1): return True

                    coordinates.pop()
                    region[region_idx] = False
                    ans[i][j] = chr(self.arr[i][j] + ord('A'))
        
solver = Algo(arr)
start_time = time.perf_counter()
solver.solve(0)
end_time = time.perf_counter()
pprint.pprint(solver.ans)
print("Time Elapsed: ", f"{((end_time-start_time)*1000):.2f}", " ms")