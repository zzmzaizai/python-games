import pygame
import sys
import random

# 初始化 Pygame 游戏引擎
pygame.init()

# 定义游戏中使用的颜色（RGB格式）
WHITE = (255, 255, 255)  # 白色
BLACK = (0, 0, 0)      # 黑色
RED = (255, 0, 0)      # 红色，用于食物
GREEN = (0, 255, 0)    # 绿色，用于蛇身
BLUE = (0, 0, 255)     # 蓝色，用于按钮
GRAY = (128, 128, 128)  # 灰色，用于半透明遮罩

# 游戏窗口和网格设置
WINDOW_WIDTH = 800     # 游戏窗口宽度
WINDOW_HEIGHT = 600    # 游戏窗口高度
GRID_SIZE = 20        # 网格大小（像素）
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE   # 网格宽度数量
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE  # 网格高度数量

class Snake:
    """蛇类
    
    控制蛇的移动、生长和渲染等核心功能
    
    属性:
        length: 蛇的长度
        positions: 蛇身体各部分的位置列表，每个位置是一个(x,y)元组
        direction: 移动方向，可以是(0,1)向下,(0,-1)向上,(1,0)向右,(-1,0)向左
        color: 蛇的颜色
        score: 当前得分
    """
    def __init__(self):
        """初始化蛇的属性
        
        设置蛇的初始长度、位置、方向、颜色和分数
        """
        """初始化蛇的属性
        
        设置蛇的初始长度、位置、方向、颜色和分数
        """
        self.length = 1  # 初始长度为1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]  # 初始位置在屏幕中心
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # 随机初始方向
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        """获取蛇头位置
        
        返回:
            tuple: 蛇头的(x,y)坐标
        """
        return self.positions[0]

    def update(self):
        """更新蛇的位置
        
        根据当前方向移动蛇，检查是否撞到自己
        
        返回:
            bool: True表示移动成功，False表示游戏结束
        """
        cur = self.get_head_position()
        x, y = self.direction
        # 计算新的头部位置，使用取模运算实现穿墙
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
        # 检查是否撞到自己（从第三个位置开始检查，因为蛇不可能撞到自己的第一节和第二节）
        if new in self.positions[2:]:
            return False
        # 在列表开头插入新的头部位置
        self.positions.insert(0, new)
        # 如果超过当前长度，删除尾部
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        """重置蛇的状态
        
        在游戏重新开始时调用，重置蛇的长度、位置、方向和分数
        """
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.score = 0

    def render(self, surface):
        """渲染蛇的身体
        
        参数:
            surface: pygame的显示表面对象
        """
        for p in self.positions:
            rect = pygame.Rect(p[0] * GRID_SIZE, p[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.color, rect)

class Food:
    """食物类
    
    控制食物的生成和显示
    
    属性:
        position: 食物的位置，(x,y)元组
        color: 食物的颜色
    """
    def __init__(self):
        """初始化食物
        
        设置初始位置和颜色，并随机放置食物
        """
        self.position = (0, 0)
        self.color = RED
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        """随机生成食物位置
        
        确保食物不会出现在蛇身上
        
        参数:
            snake_positions: 蛇身体占据的所有位置列表
        """
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if self.position not in snake_positions:
                break

    def render(self, surface):
        """渲染食物
        
        参数:
            surface: pygame的显示表面对象
        """
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.color, rect)

class Game:
    """游戏主类
    
    控制游戏的主要逻辑，包括初始化、事件处理、更新和渲染
    
    属性:
        window: pygame显示窗口
        snake: 蛇对象
        food: 食物对象
        font: 字体对象，用于显示文本
        game_over: 游戏是否结束
        paused: 游戏是否暂停
        show_pause_menu: 是否显示暂停菜单
    """
    def __init__(self):
        """初始化游戏
        
        创建游戏窗口，初始化游戏对象和状态
        """
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('贪吃蛇')
        self.snake = Snake()
        self.food = Food()
        self.font = pygame.font.SysFont('SimHei', 36)  # 使用系统黑体字体
        self.game_over = False
        self.paused = False
        self.show_pause_menu = False

        # 初始化暂停菜单按钮
        button_width = 200
        button_height = 50
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        self.continue_button = pygame.Rect(button_x, WINDOW_HEIGHT // 2 - 60, button_width, button_height)
        self.menu_button = pygame.Rect(button_x, WINDOW_HEIGHT // 2 + 10, button_width, button_height)

    def handle_keys(self):
        """处理键盘和鼠标输入
        
        处理游戏的各种输入事件，包括移动、暂停、重启等
        
        返回:
            bool: True表示要返回主菜单，False表示继续游戏
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # ESC键控制暂停菜单
                if event.key == pygame.K_ESCAPE:
                    if self.show_pause_menu:
                        self.show_pause_menu = False
                        self.paused = False
                    else:
                        self.show_pause_menu = True
                        self.paused = True
                # R键重新开始游戏
                elif event.key == pygame.K_r and self.game_over:
                    self.snake.reset()
                    self.game_over = False
                # 方向键控制蛇的移动
                elif not self.game_over and not self.paused:
                    if event.key == pygame.K_UP and self.snake.direction != (0, 1):
                        self.snake.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                        self.snake.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                        self.snake.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                        self.snake.direction = (1, 0)
            # 处理手柄按钮事件
            elif event.type == pygame.JOYBUTTONDOWN:
                if self.show_pause_menu:
                    if event.button == 7:  # Start键
                        self.show_pause_menu = False
                        self.paused = False
                    elif event.button == 1:  # B键
                        return True  # 返回主菜单
                else:
                    if event.button == 7:  # Start键
                        self.show_pause_menu = True
                        self.paused = True
                    elif event.button == 0 and self.game_over:  # A键重新开始
                        self.snake.reset()
                        self.game_over = False
            # 处理暂停菜单的鼠标点击
            elif event.type == pygame.MOUSEBUTTONDOWN and self.show_pause_menu:
                mouse_pos = pygame.mouse.get_pos()
                if self.continue_button.collidepoint(mouse_pos):
                    self.show_pause_menu = False
                    self.paused = False
                elif self.menu_button.collidepoint(mouse_pos):
                    return True  # 返回主菜单
        
        # 处理手柄摇杆和方向键输入
        if not self.game_over and not self.paused:
            for joystick in pygame.joystick.get_count() and [pygame.joystick.Joystick(0)]:
                # 处理左摇杆
                axis_x = joystick.get_axis(0)  # 水平轴
                axis_y = joystick.get_axis(1)  # 垂直轴
                if abs(axis_x) > 0.5 or abs(axis_y) > 0.5:
                    if abs(axis_x) > abs(axis_y):
                        if axis_x < -0.5 and self.snake.direction != (1, 0):
                            self.snake.direction = (-1, 0)
                        elif axis_x > 0.5 and self.snake.direction != (-1, 0):
                            self.snake.direction = (1, 0)
                    else:
                        if axis_y < -0.5 and self.snake.direction != (0, 1):
                            self.snake.direction = (0, -1)
                        elif axis_y > 0.5 and self.snake.direction != (0, -1):
                            self.snake.direction = (0, 1)
                
                # 处理方向键
                hat = joystick.get_hat(0)
                if hat[0] != 0 or hat[1] != 0:
                    if abs(hat[0]) > abs(hat[1]):
                        if hat[0] < 0 and self.snake.direction != (1, 0):
                            self.snake.direction = (-1, 0)
                        elif hat[0] > 0 and self.snake.direction != (-1, 0):
                            self.snake.direction = (1, 0)
                    else:
                        if hat[1] > 0 and self.snake.direction != (0, 1):
                            self.snake.direction = (0, -1)
                        elif hat[1] < 0 and self.snake.direction != (0, -1):
                            self.snake.direction = (0, 1)
        return False

    def run(self):
        """运行游戏主循环
        
        控制游戏的主要流程，包括更新游戏状态、处理碰撞、渲染画面等
        """
        clock = pygame.time.Clock()

        while True:
            # 处理输入事件
            if self.handle_keys():  # 如果返回True，表示要返回主菜单
                break

            # 游戏逻辑更新
            if not self.game_over and not self.paused:
                # 更新蛇的位置，检查是否撞到自己
                if not self.snake.update():
                    self.game_over = True

                # 检查是否吃到食物
                if self.snake.get_head_position() == self.food.position:
                    self.snake.length += 1  # 蛇长度加1
                    self.snake.score += 10  # 得分加10
                    self.food.randomize_position(self.snake.positions)  # 重新放置食物

            # 渲染游戏画面
            self.window.fill(BLACK)  # 清空屏幕
            self.snake.render(self.window)
            self.food.render(self.window)

            # 显示分数
            score_text = self.font.render(f'得分: {self.snake.score}', True, WHITE)
            self.window.blit(score_text, (10, 10))

            # 显示游戏结束信息
            if self.game_over:
                game_over_text = self.font.render('游戏结束! 按R重新开始', True, WHITE)
                text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                self.window.blit(game_over_text, text_rect)

            # 绘制暂停菜单
            if self.show_pause_menu:
                # 创建半透明遮罩层
                overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                overlay.fill(GRAY)
                overlay.set_alpha(128)
                self.window.blit(overlay, (0, 0))
                
                # 绘制暂停菜单按钮
                pygame.draw.rect(self.window, BLUE, self.continue_button)
                pygame.draw.rect(self.window, BLUE, self.menu_button)
                
                # 绘制按钮文本
                continue_text = self.font.render('继续游戏', True, WHITE)
                menu_text = self.font.render('返回主菜单', True, WHITE)
                
                # 居中显示文本
                continue_text_rect = continue_text.get_rect(center=self.continue_button.center)
                menu_text_rect = menu_text.get_rect(center=self.menu_button.center)
                
                self.window.blit(continue_text, continue_text_rect)
                self.window.blit(menu_text, menu_text_rect)

            pygame.display.flip()  # 更新显示
            clock.tick(10)  # 控制游戏速度，10帧每秒

if __name__ == '__main__':
    game = Game()
    game.run()