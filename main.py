# ------------------------------ Initialization ------------------------------ #
import copy
import pprint
import time
import threading
from gui import GUI

# Global variables
arr = None
solver = None
solver_thread = None
on_exit = threading.Event()

def load_file(file_path):
    global arr
    try:
        with open(file_path, "r") as f:
            text = f.read()
        lines = text.split('\n')
        arr = [list(x.strip()) for x in lines if x.strip()]
        print(f"Loaded file: {file_path}")
        print(arr)
        return arr
    except Exception as e:
        print(f"Error loading file: {e}")
        return None
class Algo:
    def __init__(self, arr, gui=None):
        self.arr = [[ord(item) - ord('A') for item in rows] for rows in arr]
        self.ans = arr
        self.coordinate = list()
        self.num_regions = max(max(row) for row in self.arr)
        self.region = list(False for i in range(self.num_regions + 1))
        self.rows = len(arr)
        self.cols = len(arr[0])
        self.gui = gui

        self.optimizer = False

    def checkInputValid(self):
        if(self.num_regions >= self.rows or self.num_regions >= self.cols): return False

    # --------------------------------- Main Algo -------------------------------- #
    def checkOutputValid(self):
        coordinates = self.coordinate
        if coordinates == []: return False
        if len(coordinates) != self.num_regions + 1: return False
        for i in range(len(coordinates)):
            for j in range(i + 1, len(coordinates)):
                if(coordinates[i][0] == coordinates[j][0]): return False
                if(coordinates[i][1] == coordinates[j][1]): return False
                if(abs(coordinates[i][0] - coordinates[j][0]) == 1 and abs(coordinates[i][1] - coordinates[j][1]) == 1): return False
        
        if not self.optimizer:
            for i in range(len(coordinates)):
                if self.arr[coordinates[i][0]][coordinates[i][1]] != i: return False

        return True

    def solve(self, region_idx):
        if on_exit.is_set():
            return False
        
        if(region_idx > self.num_regions):
            if self.gui:
                self.gui.queens = self.coordinate
            return self.checkOutputValid()
        
        ans = self.ans
        region = self.region
        coordinates = self.coordinate
        for i in range(self.rows):
            for j in range(self.cols):
                if(not self.optimizer or self.arr[i][j] == region_idx):
                    ans[i][j] = "X"
                    region[self.arr[i][j]] = True
                    coordinates.append([i, j])

                    if self.solve(region_idx+1): return True

                    coordinates.pop()
                    region[region_idx] = False
                    ans[i][j] = chr(self.arr[i][j] + ord('A'))
        return False

def run_solver(solver):
    start_time = time.perf_counter()
    result = solver.solve(0)
    end_time = time.perf_counter()
    if(not on_exit.is_set()):
        print(f"Solution found: {result}")
        print("Time Elapsed:", f"{((end_time-start_time)*1000):.4f}", "ms")
        print("Coordinates:", solver.coordinate)

def on_import_callback(file_path):
    global arr, solver, on_exit
    arr = load_file(file_path)
    if arr:
        solver = Algo(arr, gui=gui)
        on_exit.set()
        gui.rows = len(arr)
        gui.cols = len(arr[0])
        gui.arr = solver.arr
        gui.regions = [i for i in range(solver.num_regions)]
        gui.generate_colors()


def on_solve_callback(optimized=False):
    global solver, solver_thread, arr
    
    if arr is None:
        print("Please import a file first")
        return
    
    if solver_thread and solver_thread.is_alive():
        print("Solver already running")
        return
    
    if optimized:
        solver.optimizer = True

    on_exit.clear()
    solver_thread = threading.Thread(target=run_solver, args=(solver,), daemon=True)
    solver_thread.start()

gui = GUI(5, 5)
gui.on_import = on_import_callback
gui.on_solve = on_solve_callback

gui.run()
