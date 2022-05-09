from dataclasses import dataclass, field
from enum import Enum
from random import randint
from time import sleep
import sys
import pygame

MAX_FPS = 10

WINDOW_HEIGHT = 500
WINDOW_WIDTH = 500
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WIN = pygame.display.set_mode(WINDOW_SIZE, 0, 12)

DISPLAY_WIDTH = 20
DISPLAY_HEIGHT = 20
DISPLAY_SIZE = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
DISPLAY = pygame.Surface(DISPLAY_SIZE)

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Cell(Enum):
    EMPTY = 0
    FRUIT = 1
    HEAD = 2
    BODY = 3
    TAIL = 4

RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def random_pos():
    return [
        randint(0, DISPLAY_WIDTH - 1),
        randint(0, DISPLAY_HEIGHT - 1)
    ]

Part = list[int]
DIE_EVENT = pygame.USEREVENT + 1

def out_of_bounds(part: Part):
    return part[0] < 0 or part[0] >= DISPLAY_WIDTH or part[1] < 0 or part[1] >= DISPLAY_HEIGHT

@dataclass(slots=True)
class Snake:
    body: list[Part] = field(default_factory=list)
    direction: Direction = Direction.DOWN
    _will_grow: bool = False

    def __post_init__(self):
        self.body = [[0, 2], [0, 1], [0, 0]]

    def move(self):
        add = 1
        index = 0
        if self.direction == Direction.DOWN:
            add = 1
            index = 1
        elif self.direction == Direction.UP:
            add = -1
            index = 1
        elif self.direction == Direction.RIGHT:
            add = 1
            index = 0
        elif self.direction == Direction.LEFT:
            add = -1
            index = 0
        
        new_head = self.head().copy()
        new_head[index] += add

        if new_head in self.body or out_of_bounds(new_head):
            pygame.event.post(pygame.event.Event(DIE_EVENT))
        else:
            self.body.insert(0, new_head)
            
            if self._will_grow:
                self._will_grow = False
            else:
                self.body.pop()

    
    def grow(self):
        self._will_grow = True
    
    def head(self):
        return self.body[0]
    
    def tail(self):
        return self.body[-1]
    
    def draw(self):
        for i, part in enumerate(self.body):
            color = GREEN
            if i == 0:
                color = WHITE
            r = pygame.Rect(part[0], part[1], 1, 1)
            pygame.draw.rect(DISPLAY, color, r)
    
        

class Grid:
    def __init__(self):
        self.grid: list[list[Cell]] = [[Cell.EMPTY for _ in range(DISPLAY_WIDTH)] for _ in range(DISPLAY_HEIGHT)]
        self.fruit_pos = random_pos()
        self.grid[self.fruit_pos[1]][self.fruit_pos[0]] = RED
        self.snake = Snake()
    
    def draw(self):
        r = pygame.Rect(self.fruit_pos[0], self.fruit_pos[1], 1, 1)
        pygame.draw.rect(DISPLAY, RED, r)

    def get_new_fruit(self, snake):
        while self.fruit_pos in snake.body:
            self.fruit_pos = random_pos()
    

def snake_on_fruit(snake: Snake, grid: Grid):
    if snake.head() == grid.fruit_pos:
        snake.grow()
        grid.get_new_fruit(snake)


def main():
    clock = pygame.time.Clock()
    grid = Grid()
    snake = Snake()
    
    while True:
        DISPLAY.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == DIE_EVENT:
                sleep(1)
                grid = Grid()
                snake = Snake()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and snake.direction != Direction.DOWN:
                    snake.direction = Direction.UP
                elif event.key == pygame.K_s and snake.direction != Direction.UP:
                    snake.direction = Direction.DOWN
                elif event.key == pygame.K_a and snake.direction != Direction.RIGHT:
                    snake.direction = Direction.LEFT
                elif event.key == pygame.K_d and snake.direction != Direction.LEFT:
                    snake.direction = Direction.RIGHT
        
        grid.draw()
        snake.draw()
        snake.move()
        snake_on_fruit(snake, grid)
        
        surf = pygame.transform.scale(DISPLAY, WINDOW_SIZE)
        WIN.blit(surf, (0, 0))
        pygame.display.update()
        
        clock.tick(MAX_FPS)


if __name__ == "__main__":
    main()
