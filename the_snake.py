import sys
from random import randint
from typing import List, Tuple

import pygame

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

INITIAL_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 10

# Инициализация экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position: Tuple[int, int] = INITIAL_POSITION,
                 body_color: Tuple[int, int, int] = None) -> None:
        """Инициализация объекта."""
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position: Tuple[int, int],
                  color: Tuple[int, int, int]) -> None:
        """Отрисовка ячейки."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        
    def draw(self) -> None:
        """Метод Draw"""



class Apple(GameObject):
    """Класс для яблока, которое змейка может съесть."""

    def __init__(self, body_color: Tuple[int, int, int] = APPLE_COLOR,
                 occupied_positions: List[Tuple[int, int]] = None) -> None:
        """Инициализация яблока."""
        super().__init__(body_color=body_color)
        self.occupied_positions = occupied_positions
        self.randomize_position()

    def draw(self) -> None:
        """Отрисовка яблока на экране."""
        self.draw_cell(self.position, self.body_color)

    def randomize_position(self,
                           occupied_positions: List[Tuple[int, int]]
                           = None) -> None:
        """Установка случайной позиции для яблока."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if not occupied_positions:
                break
            if self.position not in occupied_positions:
                break


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self, body_color: Tuple[int, int, int] = SNAKE_COLOR) -> None:
        """Инициализация змейки."""
        super().__init__(body_color=body_color)
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def draw(self) -> None:
        """Отрисовка змейки на экране."""
        for position in self.positions:
            self.draw_cell(position, self.body_color)

    def update_direction(self) -> None:
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, ate_apple: bool = False) -> None:
        """Движение змейки."""
        head = self.get_head_position()
        new_head = (
            (head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        if not ate_apple:
            self.positions.pop()

    def get_head_position(self) -> Tuple[int, int]:
        """Получение позиции головы змейки."""
        return self.positions[0]

    def reset(self) -> None:
        """Сброс змейки в начальное состояние."""
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(snake: Snake) -> None:
    """Обработка нажатий клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main() -> None:
    """Основная функция игры."""
    pygame.init()
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()

        if snake.get_head_position() == apple.position:
            apple.randomize_position(occupied_positions=snake.positions)
            snake.move(ate_apple=True)
        else:
            snake.move()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
