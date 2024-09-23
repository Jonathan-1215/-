import pygame
import sys
import os
import random
import time, datetime
from pygame.locals import *

# 游戏设置
background_color = (255, 255, 255)

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BUTTON_COLOR = (200, 200, 200)  # 按钮默认颜色
BUTTON_HOVER_COLOR = (180, 180, 255)  # 按钮悬停颜色
BUTTON_ACTIVE_COLOR = (150, 150, 230)  # 按钮点击颜色


FPS = 90

# 设置图片文件夹路径
image_folder_path = 'images'  # 替换为你的图片文件夹路径

# 获取所有图片文件路径
image_files = [os.path.join(image_folder_path, f) for f in os.listdir(image_folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

# 随机选择一张图片
selected_image_path = random.choice(image_files)

# 定义拼图碎片的大小和数量
ROWS, COLS = 3, 3
cell_nums = ROWS * COLS
max_rand_time = 100

# 初始化
pygame.init()
mainClock = pygame.time.Clock()

# 加载图片
gameImage = pygame.image.load(selected_image_path)
gameRect = gameImage.get_rect()

# 设置窗口
windowSurface = pygame.display.set_mode((gameRect.width, gameRect.height))
pygame.display.set_caption('拼图游戏')

#设置每个块的大小
cellWidth = int(gameRect.width / ROWS)
cellHeight = int(gameRect.height / ROWS)

# 记录开始时间
startTime = time.time()
# 答题时间
totalTime = 60*60

# 字体设置
font = pygame.font.SysFont('SimHei', 20, True, True)

# 完成标志
finish = False


# 按钮类
class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = BUTTON_COLOR
        self.hover = False
        self.active = False

    def draw(self, surface):
        # 绘制按钮背景
        if self.active:
            pygame.draw.rect(surface, BUTTON_ACTIVE_COLOR, self.rect)
        elif self.hover:
            pygame.draw.rect(surface, BUTTON_HOVER_COLOR, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

        # 绘制文本
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

        # 绘制边框
        pygame.draw.rect(surface, BLACK, self.rect, 2)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.active = True
            return True
        if event.type == pygame.MOUSEBUTTONUP and self.active:
            self.active = False
            return True
        return False

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEMOTION and self.rect.collidepoint(event.pos):
                self.hover = True
            else:
                self.hover = False

# 创建按钮
button = Button(350, 550, 100, 50, "确定", font)

# 随机生成游戏盘面
def newGameBoard():
    # 生成一个新的游戏盘面。首先创建一个长度为cell_nums的列表，其中每个元素都是其在列表中的位置。然后将最后一个元素（即右下角的空白块）的值设为-1
    board = []
    for i in range(cell_nums):
        board.append(i)
    black_cell = cell_nums - 1
    board[black_cell] = -1

    # 随机移动拼图块max_rand_time次，生成随机的游戏盘面
    for i in range(max_rand_time):
        direction = random.randint(0, 3)
        if direction == 0:
            black_cell = moveLeft(board, black_cell)
        elif direction == 1:
            black_cell = moveRight(board, black_cell)
        elif direction == 2:
            black_cell = moveUp(board, black_cell)
        elif direction == 3:
            black_cell = moveDown(board, black_cell)
    return board, black_cell


# 若空白图像块不在最左边，则将空白块左边的块移动到空白块位置
def moveRight(board, black_cell):
    if black_cell % ROWS == 0:
        return black_cell
    board[black_cell - 1], board[black_cell] = board[black_cell], board[black_cell - 1]
    return black_cell - 1


# 若空白图像块不在最右边，则将空白块右边的块移动到空白块位置
def moveLeft(board, black_cell):
    if black_cell % ROWS == ROWS - 1:
        return black_cell
    board[black_cell + 1], board[black_cell] = board[black_cell], board[black_cell + 1]
    return black_cell + 1


# 若空白图像块不在最上边，则将空白块上边的块移动到空白块位置
def moveDown(board, black_cell):
    if black_cell < ROWS:
        return black_cell
    board[black_cell - ROWS], board[black_cell] = board[black_cell], board[black_cell - ROWS]
    return black_cell - ROWS


# 若空白图像块不在最下边，则将空白块下边的块移动到空白块位置
def moveUp(board, black_cell):
    if black_cell >= cell_nums - ROWS:
        return black_cell
    board[black_cell + ROWS], board[black_cell] = board[black_cell], board[black_cell + ROWS]
    return black_cell + ROWS


# 是否完成
def isFinished(board):
    for i in range(cell_nums - 1):
        if board[i] != i:
            return False
    return True

gameBoard, black_cell = newGameBoard()

# 游戏主循环
while True:
    for event in pygame.event.get():
        # 显示倒计时
        elapsed_time = int(time.time() - startTime)
        remaining_time = totalTime - elapsed_time
        hours = remaining_time // 3600
        minutes = (remaining_time % 3600) // 60
        seconds = remaining_time % 60
        # 退出
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # 如果时间到了，并且按钮被点击，则退出游戏
        if remaining_time <= 0 :
            if finish:
                button = Button(150, 450, 100, 50, "成功", pygame.font.Font(None, 36), GREEN, BUTTON_COLOR)
                button.draw(windowSurface)
                continue
            if  button.is_clicked(event):
                print("按钮被点击了")
                pygame.quit()
                sys.exit()


        else:

                # 更新按钮的悬停状态
            button.update(pygame.event.get())

            # 按下方向键或者字母键，则移动方块
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == ord('a'):
                    black_cell = moveLeft(gameBoard, black_cell)
                if event.key == K_RIGHT or event.key == ord('d'):
                    black_cell = moveRight(gameBoard, black_cell)
                if event.key == K_UP or event.key == ord('w'):
                    black_cell = moveUp(gameBoard, black_cell)
                if event.key == K_DOWN or event.key == ord('s'):
                    black_cell = moveDown(gameBoard, black_cell)

            # 点击鼠标左键，则移动方块
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                col = int(x / cellWidth)
                row = int(y / cellHeight)
                index = col + row * ROWS
                if index == black_cell - 1 or index == black_cell + 1 or index == black_cell - ROWS or index == black_cell + ROWS:
                    gameBoard[black_cell], gameBoard[index] = gameBoard[index], gameBoard[black_cell]
                    black_cell = index

        # 如果拼图已经完成，则将黑色方块移回右下角，并标记游戏结束
        if isFinished(gameBoard):
            gameBoard[black_cell] = cell_nums - 1
            finish = True

        # 填充游戏窗口
        windowSurface.fill(background_color)

        # 将拼图中的每个小块绘制到游戏窗口中
        for i in range(cell_nums):
            rowDst = int(i / ROWS)
            colDst = int(i % ROWS)
            rectDst = pygame.Rect(colDst * cellWidth, rowDst * cellHeight, cellWidth, cellHeight)

            if gameBoard[i] == -1:
                continue

            rowArea = int(gameBoard[i] / ROWS)
            colArea = int(gameBoard[i] % ROWS)
            rectArea = pygame.Rect(colArea * cellWidth, rowArea * cellHeight, cellWidth, cellHeight)
            windowSurface.blit(gameImage, rectDst, rectArea)

        # 绘制拼图的网格线
        for i in range(ROWS + 1):
            pygame.draw.line(windowSurface, BLACK, (i * cellWidth, 0), (i * cellWidth, gameRect.height))
        for i in range(ROWS + 1):
            pygame.draw.line(windowSurface, BLACK, (0, i * cellHeight), (gameRect.width, i * cellHeight))

        # 如果时间到了，显示游戏结束消息
        if remaining_time <= 0:
            end_surface = font.render("时间到游戏结束", True, BLACK)
            windowSurface.blit(end_surface, (windowSurface.get_width() / 2 - 100, windowSurface.get_height() / 2 - 25))
            button.draw(windowSurface)  # 绘制按钮
            # 更新游戏窗口
            pygame.display.update()

        else:
            time_text = font.render(f'剩余时间: {hours:02d}:{minutes:02d}:{seconds:02d}', True, RED)
            windowSurface.blit(time_text, (10, 10))
            pygame.display.update()
        # 控制游戏的帧率
        mainClock.tick(FPS)
