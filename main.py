import random
import pygame
import pymunk
import pymunk.pygame_util

pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
game_over_color = (171, 235, 198)

# Creating window
screen_width = 900
screen_height = 600
text_offset = 30
back_image_width = screen_width - (2 * text_offset)
back_image_height = screen_height - (2 * text_offset)
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Game Title
pygame.display.set_icon(pygame.image.load("resources/snake.ico").convert_alpha())
pygame.display.set_caption("Snake Game By Anand")
pygame.display.update()

# Game specific variables

font = pygame.font.SysFont(None, 55)
start_image = pygame.image.load("resources/start_screen.png").convert()


def start_screen(background):
    background = pygame.transform.scale(background, (screen_width, screen_height)).convert_alpha()
    gameWindow.blit(background, (0, 0))
    pygame.mixer.Sound("resources/back.mp3").play()
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_RETURN:
                    waiting = False
                    pygame.mixer.stop()


def game_background():
    background_image = pygame.image.load("resources/game_back.png")
    background_image = pygame.transform.scale(background_image, (back_image_width, back_image_height)).convert_alpha()
    gameWindow.blit(background_image, (text_offset, text_offset))
    pygame.display.update()


def text_screen(text, color, x, y, font="Courier New", font_size=36):
    font = pygame.font.SysFont(font, font_size)
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def get_highscore():
    with open("resources/highScore.txt", "r") as f:
        highscore = f.read()
        return int(highscore)


old_highscore = get_highscore()


def save_highscore(score):
    with open("resources/highScore.txt", "w") as f:
        f.write(str(score))


def plot_snake(gameWindow, color, snake_list, size):
    for x, y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, size, size])


def hit_wall(snake_x, snake_y):
    if snake_x < text_offset + 5 or snake_x > back_image_width - 5 or snake_y < text_offset + 5 or snake_y > back_image_height - 5:
        return True
    return False


def hit_self(head, snake_list):
    if head in snake_list[:-1]:
        return True
    return False


def get_food_position():
    food_x = random.randint(text_offset + 10, back_image_width - 10)
    food_y = random.randint(text_offset + 10, back_image_height - 10)
    return food_x, food_y


def game_loop():
    start_screen(start_image)
    running = True
    game_over = False
    size_snake = 20
    snake_x = screen_width / 2
    snake_y = screen_height / 2
    velocity_x = 0
    velocity_y = 0
    snake_velocity_change = 4
    food_x = random.randint(text_offset + 10, screen_width)
    food_y = random.randint(text_offset + 10, screen_height)
    clock = pygame.time.Clock()
    score = 0
    fps = 60

    snake_list = []
    snake_length = 1
    while running:
        if game_over:
            gameover_sound = pygame.mixer.Sound("resources/gameover.mp3")
            gameover_sound.set_volume(0.1)  # Set volume (0.0 to 1.0)
            gameover_sound.play()
            gameWindow.fill(game_over_color)
            highscore = get_highscore()
            if score > highscore:
                save_highscore(score)
                highscore = score
                text_screen("You Created a new HighScore!", red, screen_width / 3, screen_height / 3)
            game_over_text = "Game Over! Press Enter to Play Again"
            text_screen(
                "Game Over! Press Enter to Play Again",
                red,
                screen_width // 2 - len(game_over_text) * 10 - 20,
                250,
                "Courier New",
                36,
            )
            score_text = "Your Score: " + str(score * 10)
            text_screen(
                score_text,
                black,
                screen_width // 2 - len(score_text) * 10 - 20,
                320,
                "Courier New",
                36,
            )
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.stop()
                        game_loop()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_RIGHT:
                        if velocity_x == 0:
                            velocity_x = snake_velocity_change
                            velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        if velocity_x == 0:
                            velocity_x = -snake_velocity_change
                            velocity_y = 0
                    if event.key == pygame.K_UP:
                        if velocity_y == 0:
                            velocity_x = 0
                            velocity_y = -snake_velocity_change
                    if event.key == pygame.K_DOWN:
                        if velocity_y == 0:
                            velocity_x = 0
                            velocity_y = snake_velocity_change
            if abs(snake_x - food_x) < 12 and abs(snake_y - food_y) < 12:
                score += 1
                pygame.mixer.Sound("resources/food.wav").play()
                food_x, food_y = get_food_position()
                snake_length += 8

            snake_color = (random.randint(100, 190), random.randint(100, 190), random.randint(100, 190))
            food_color = (random.randint(50, 255), random.randint(0, 80), random.randint(50, 255))
            gameWindow.fill(white)
            game_background()
            text_screen("Score: " + str(score * 10), red, 35, 1)
            text_screen("HighScore: " + str(old_highscore * 10), red, screen_width - 450, 1)
            snake_x += velocity_x
            snake_y += velocity_y
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)
            if len(snake_list) > snake_length:
                del snake_list[0]
            if hit_wall(snake_x, snake_y) or hit_self(head, snake_list):
                game_over = True
            plot_snake(gameWindow, snake_color, snake_list, size_snake)
            pygame.draw.rect(gameWindow, food_color, [food_x, food_y, 15, 15])
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


game_loop()
