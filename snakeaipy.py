import pygame
import random

from collections import deque

pygame.init()

WINDOW_WIDTH ,WINDOW_HEIGHT =800, 600
BLOCK_SIZE = 20
SPEED = 1000  

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake AI Player')

class Snake:
    def __init__(self):
        self.body = [(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        self.direction = "RIGHT"
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]

        if self.direction == "RIGHT":
            new_head = (head_x + BLOCK_SIZE, head_y)
        elif self.direction == "LEFT":
            new_head = (head_x - BLOCK_SIZE, head_y)
        elif self.direction == "UP":
            new_head = (head_x, head_y - BLOCK_SIZE)
        elif self.direction == "DOWN":
            new_head = (head_x, head_y + BLOCK_SIZE)

        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        self.grow = False

    def get_head(self):
        return self.body[0]

    def draw(self, screen):
        for i, segment in enumerate(self.body):
            color = GREEN 
            pygame.draw.rect(screen, color, 
                           (segment[0], segment[1], BLOCK_SIZE-1, BLOCK_SIZE-1))

class Food:
    def __init__(self, snake_body):
        self.snake_body = snake_body
        self.position = self.generate_position()

    def generate_position(self):
        while True:
            x = random.randint(0, (WINDOW_WIDTH-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (WINDOW_HEIGHT-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
            if (x, y) not in self.snake_body:
                return (x, y)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, 
                        (self.position[0], self.position[1], BLOCK_SIZE-1, BLOCK_SIZE-1))

class SnakeAI:
    def __init__(self, snake, food):
        self.snake = snake
        self.food = food

    def get_next_direction(self):

        path = self.find_path_to_food()
        if not path:

            path = self.find_safe_path()
            if not path:

                return self.follow_tail()

        if path:
            next_move = path[1]  
            current = self.snake.get_head()

            if next_move[0] > current[0]:
                return "RIGHT"
            elif next_move[0] < current[0]:
                return "LEFT"
            elif next_move[1] < current[1]:
                return "UP"
            else:
                return "DOWN"

        return self.snake.direction  

    def find_path_to_food(self):
        start = self.snake.get_head()
        goal = self.food.position

        return self.bfs(start, goal)

    def find_safe_path(self):
        start = self.snake.get_head()
        longest_path = []

        for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
            for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
                if (x, y) not in self.snake.body:
                    path = self.bfs(start, (x, y))
                    if path and len(path) > len(longest_path):
                        longest_path = path

        return longest_path

    def follow_tail(self):

        tail = self.snake.body[-1]
        head = self.snake.get_head()

        if tail[0] > head[0] and self.is_move_safe((head[0] + BLOCK_SIZE, head[1])):
            return "RIGHT"
        elif tail[0] < head[0] and self.is_move_safe((head[0] - BLOCK_SIZE, head[1])):
            return "LEFT"
        elif tail[1] < head[1] and self.is_move_safe((head[0], head[1] - BLOCK_SIZE)):
            return "UP"
        elif tail[1] > head[1] and self.is_move_safe((head[0], head[1] + BLOCK_SIZE)):
            return "DOWN"

        return self.snake.direction

    def bfs(self, start, goal):
        queue = deque([[start]])
        visited = set([start])

        while queue:
            path = queue.popleft()
            current = path[-1]

            if current == goal:
                return path

            for dx, dy in [(0, BLOCK_SIZE), (0, -BLOCK_SIZE), (BLOCK_SIZE, 0), (-BLOCK_SIZE, 0)]:
                next_pos = (current[0] + dx, current[1] + dy)

                if self.is_move_safe(next_pos) and next_pos not in visited:
                    queue.append(path + [next_pos])
                    visited.add(next_pos)

        return None

    def is_move_safe(self, pos):
        x, y = pos

        if x < 0 or x >= WINDOW_WIDTH or y < 0 or y >= WINDOW_HEIGHT:
            return False

        if pos in self.snake.body[:-1]:  
            return False

        return True

def show_score(screen, score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food(snake.body)
    ai = SnakeAI(snake, food)
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        snake.direction = ai.get_next_direction()

        snake.move()

        if snake.get_head() == food.position:
            snake.grow = True
            food.position = food.generate_position()
            score += 10

        head_x, head_y = snake.get_head()
        if (head_x < 0 or head_x >= WINDOW_WIDTH or 
            head_y < 0 or head_y >= WINDOW_HEIGHT or 
            snake.get_head() in snake.body[1:]):
            running = False

        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        show_score(screen, score)
        pygame.display.flip()

        clock.tick(SPEED)

    print(f"Final Score: {score}")
    pygame.quit()

if __name__ == "__main__":
    main()