import pygame
import random
import copy

from pygame.locals import *

pygame.init()

# 格子长宽
cell = 10
snake_position = [[250, 250], [240, 250], [230, 250], [220, 250]]
snake_head = copy.deepcopy(snake_position[0])
# snake_head = [250, 250]

# 屏幕
screen_size = (500, 500)

food_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]


def draw_rect(color: tuple, position: list):
    """
    画矩形
    :param color:
    :param position:
    :return:
    """
    pygame.draw.rect(caption, color, pygame.Rect(position[0], position[1], cell, cell))


def allow_run(pos: list, now_snake: list):
    """
    是否允许前进
    判断逆向前进，而不是蛇头撞到蛇身
    :param pos: 下一步的位置
    :param now_snake: 目前snake的区域
    :return:
    """
    if pos == now_snake[1]:
        return False
    return True


def against_wall(snake: list):
    """
    撞墙
    :param snake:
    :return:
    """
    if snake[0][0] >= screen_size[0] or snake[0][1] >= screen_size[1] or snake[0][0] < 0 or snake[0][1] < 0:
        return True
    return False


def against_self(snake: list):
    """
    撞自己
    :param snake:
    :return:
    """
    if snake[0] in snake[1:]:
        return True
    return False


def end_game(snake: list):
    """
    游戏结束标准
    :param snake:
    :return:
    """
    if against_self(snake) or against_wall(snake):
        return True
    return False


def auto_forward(direction: str, snake: list):
    """
    自动前进
    :param direction: 方向
    :param snake: 蛇体
    :return:
    """
    if direction == "up":
        snake_head[1] -= cell
        snake_position.insert(0, list(snake_head))
        snake.pop()
    elif direction == "down":
        snake_head[1] += cell
        snake_position.insert(0, list(snake_head))
        snake.pop()
    elif direction == "left":
        snake_head[0] -= cell
        snake_position.insert(0, list(snake_head))
        snake.pop()
    elif direction == "right":
        snake_head[0] += cell
        snake_position.insert(0, list(snake_head))
        snake.pop()


def speed_level(snake: list):
    """
    蛇体前进等级
    根据蛇体长度判断：
    s < 10: 5
    10 <= s < 30: 4
    30 <= s < 60: 3
    60 <= s < 100: 2
    100 <= s: 1
    :param snake:
    :return:
    """
    if len(snake) < 10:
        return 5
    elif 10 <= len(snake) < 30:
        return 4
    elif 10 <= len(snake) < 30:
        return 3
    elif 10 <= len(snake) < 30:
        return 2
    else:
        return 1


if __name__ == '__main__':
    caption = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Gluttonous Snake")

    # background = pygame.Surface(caption.get_size())
    # background = background.convert()
    # background.fill((0, 0, 0))
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)
    direction = "right"

    clock = pygame.time.Clock()

    s = 0

    while True:
        clock.tick(20)
        caption.fill(black)

        for pos in snake_position:
            draw_rect(white, pos)

        # todo: 食物不出现在蛇体上
        if food_position in snake_position:
            food_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
        draw_rect(green, food_position)
        # pygame.display.update()
        # 窗口无响应是因为没有任何注册在窗口上的事件
        # 为当前窗口增加事件
        # 利用pygame注册事件，其返回值是一个列表，
        # 存放当前注册时获取的所有事件
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            # 蛇体前进
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print("左")
                    next_step = [snake_head[0] - cell, snake_head[1]]
                    if allow_run(next_step, snake_position):
                        snake_head[0] -= cell
                        snake_position.insert(0, list(snake_head))
                        if food_position not in snake_position:
                            snake_position.pop()
                        direction = "left"
                elif event.key == pygame.K_RIGHT:
                    print("右")
                    next_step = [snake_head[0] + cell, snake_head[1]]
                    if allow_run(next_step, snake_position):
                        snake_head[0] +=  cell
                        snake_position.insert(0, list(snake_head))
                        if food_position not in snake_position:
                            snake_position.pop()
                        direction = "right"
                elif event.key == pygame.K_UP:
                    print("上")
                    next_step = [snake_head[0], snake_head[1] - cell]
                    if allow_run(next_step, snake_position):
                        snake_head[1] -= cell
                        snake_position.insert(0, list(snake_head))
                        if food_position not in snake_position:
                            snake_position.pop()
                        direction = "up"
                elif event.key == pygame.K_DOWN:
                    print("下")
                    next_step = [snake_head[0], snake_head[1] + cell]
                    if allow_run(next_step, snake_position):
                        snake_head[1] += cell
                        snake_position.insert(0, list(snake_head))
                        if food_position not in snake_position:
                            snake_position.pop()
                        direction = "down"
        # 自动前进
        # todo: 前进速度增快（根据长度判断？）
        s += 1
        speed = speed_level(snake_position)
        if s % speed == 0:
            s = 0
            auto_forward(direction, snake_position)
        if end_game(snake_position):
            pygame.quit()

        pygame.display.update()
        # pygame.display.flip()



# """ drawDemo.py
#     demonstrate using the drawing
#     features in pygame"""
#
# import pygame, math
#
# pygame.init()
#
#
# def drawStuff(background):
#     """ given a surface, draws a bunch of things on it """
#
#     # draw a line from (5, 100) to (100, 100)
#     pygame.draw.line(background, (255, 0, 0), (5, 100), (100, 100))
#
#     # draw an unfilled square
#     pygame.draw.rect(background, (0, 255, 0), ((200, 5), (100, 100)), 3)
#
#     # draw a filled circle
#     pygame.draw.circle(background, (0, 0, 255), (400, 50), 45)
#
#     # draw an arc
#     pygame.draw.arc(background, (0, 0, 0), ((5, 150), (100, 200)), 0, math.pi / 2, 5)
#
#     # draw an ellipse
#     pygame.draw.ellipse(background, (0xCC, 0xCC, 0x00), ((150, 150), (150, 100)), 0)
#
#     # draw lines,
#     points = (
#         (370, 160),
#         (370, 237),
#         (372, 193),
#         (411, 194),
#         (412, 237),
#         (412, 160),
#         (412, 237),
#         (432, 227),
#         (436, 196),
#         (433, 230)
#     )
#     pygame.draw.lines(background, (0xFF, 0x00, 0x00), False, points, 3)
#
#     # draw polygon
#     points = (
#         (137, 372),
#         (232, 319),
#         (383, 335),
#         (442, 389),
#         (347, 432),
#         (259, 379),
#         (220, 439),
#         (132, 392)
#     )
#     pygame.draw.polygon(background, (0x33, 0xFF, 0x33), points)
#
#     # compare normal and anti-aliased diagonal lines
#     pygame.draw.line(background, (0, 0, 0), (480, 425), (550, 325), 1)
#     pygame.draw.aaline(background, (0, 0, 0), (500, 425), (570, 325), 1)
#
#
# def main():
#     screen = pygame.display.set_mode((640, 480))
#     pygame.display.set_caption("Drawing commands")
#
#     background = pygame.Surface(screen.get_size())
#     background = background.convert()
#     background.fill((255, 255, 255))
#
#     drawStuff(background)
#
#     clock = pygame.time.Clock()
#     keepGoing = True
#     while keepGoing:
#         clock.tick(30)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 keepGoing = False
#             elif event.type == pygame.MOUSEBUTTONUP:
#                 print
#                 pygame.mouse.get_pos()
#         screen.blit(background, (0, 0))
#         pygame.display.flip()
#
#
# if __name__ == "__main__":
#     main()
