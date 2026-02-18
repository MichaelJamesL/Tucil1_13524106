import pygame
import tkinter as tk
from tkinter import filedialog
import random

class GUI:
    def __init__(self, rows, cols):
        pygame.init()

        self.WIDTH = 1000
        self.HEIGHT = 600
        self.rows = rows
        self.cols = cols

        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        pygame.display.set_caption("LinkedIn's Queens Game Solver")

        self.queens = []
        self.on_import = None
        self.on_solve = None

        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.medium_font = pygame.font.Font('freesansbold.ttf', 40)
        self.big_font = pygame.font.Font('freesansbold.ttf', 50)

        self.timer = pygame.time.Clock()
        self.fps = 60
        
        self.import_button = pygame.Rect(self.WIDTH - 180, 20, 160, 50)
        self.solve_full_button = pygame.Rect(self.WIDTH - 180, 90, 160, 50)
        self.solve_opt_button = pygame.Rect(self.WIDTH - 180, 160, 160, 100)

        self.regions = None
        self.colors = None
        self.arr = None

    def generate_colors(self):
        if not self.regions:
            return
        
        self.colors = {}
        for region in self.regions:
            self.colors[region] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def draw_board(self):
        cell_size = min(self.WIDTH // self.cols, self.HEIGHT // self.rows)
        # Draw checkerboard pattern
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * cell_size
                y = row * cell_size
                if self.colors and self.regions is not None:
                    region = self.arr[row][col]
                    color = self.colors.get(region, (200, 200, 200))
                    pygame.draw.rect(self.screen, color, [x, y, cell_size, cell_size])
                else :
                    if (row + col) % 2 == 0:
                        pygame.draw.rect(self.screen, 'light gray', [x, y, cell_size, cell_size])
        
        # Draw grid lines
        for i in range(self.rows + 1):
            pygame.draw.line(self.screen, 'black', (0, cell_size * i), (self.cols * cell_size, cell_size * i), 2)
        for i in range(self.cols + 1):
            pygame.draw.line(self.screen, 'black', (cell_size * i, 0), (cell_size * i, self.rows * cell_size), 2)

    def draw_queens(self):
        queens = self.queens
        cell_size = min(self.WIDTH // self.cols, self.HEIGHT // self.rows)
        for queen in queens:
            row, col = queen
            x = col * cell_size + cell_size // 2
            y = row * cell_size + cell_size // 2
            pygame.draw.circle(self.screen, 'red', (x, y), cell_size // 3)

    def draw_buttons(self):
        # Draw import button
        pygame.draw.rect(self.screen, 'light blue', self.import_button)
        import_text = self.font.render('Import TXT', True, 'black')
        text_rect = import_text.get_rect(center=self.import_button.center)
        self.screen.blit(import_text, text_rect)
        
        # Draw solve full button
        pygame.draw.rect(self.screen, 'light green', self.solve_full_button)
        solve_text = self.font.render('Solve Full', True, 'black')
        text_rect = solve_text.get_rect(center=self.solve_full_button.center)
        self.screen.blit(solve_text, text_rect)

        # Draw solve optimized button
        pygame.draw.rect(self.screen, 'light green', self.solve_opt_button)
        solve_text1 = self.font.render('Solve', True, 'black')
        solve_text2 = self.font.render('Optimized', True, 'black')
        text_rect1 = solve_text1.get_rect(center=(self.solve_opt_button.centerx, self.solve_opt_button.centery - 15))
        text_rect2 = solve_text2.get_rect(center=(self.solve_opt_button.centerx, self.solve_opt_button.centery + 15))
        self.screen.blit(solve_text1, text_rect1)
        self.screen.blit(solve_text2, text_rect2)
    
    def handle_import(self):
        root = tk.Tk()
        root.withdraw()
        
        file_path = filedialog.askopenfilename(
            title="Select a text file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        root.destroy()
        
        if file_path and self.on_import:
            self.on_import(file_path)
    
    def handle_solve(self, optimized=False):
        """Trigger solve callback"""
        if self.on_solve:
            self.on_solve(optimized=optimized)

    def run(self):
        run = True
        while run:
            self.timer.tick(self.fps)
            self.screen.fill('white')
            
            # Event Handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.import_button.collidepoint(event.pos):
                            self.handle_import()
                        elif self.solve_full_button.collidepoint(event.pos):
                            self.handle_solve(optimized=False)
                        elif self.solve_opt_button.collidepoint(event.pos):
                            self.handle_solve(optimized=True)
            
            self.draw_board()
            self.draw_queens()
            self.draw_buttons()
            
            pygame.display.flip()   

        pygame.quit()
