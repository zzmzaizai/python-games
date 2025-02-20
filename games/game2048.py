import pygame
import sys
import random

# 初始化 Pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# 游戏窗口设置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 4  # 4x4的网格
CELL_SIZE = 100  # 每个格子的大小
CELL_MARGIN = 10  # 格子之间的间距

# 定义数字对应的颜色
TILE_COLORS = {
    0: (205, 193, 180),    # 空格子颜色
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

class Game:
    """2048游戏类
    
    控制游戏的主要逻辑，包括初始化、更新和渲染
    
    属性:
        window: pygame显示窗口
        grid: 游戏网格
        score: 当前得分
        game_over: 游戏是否结束
        paused: 游戏是否暂停
        show_pause_menu: 是否显示暂停菜单
    """
    def __init__(self):
        """初始化游戏
        
        创建游戏窗口，初始化游戏状态
        """
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('2048')
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.game_over = False
        self.paused = False
        self.show_pause_menu = False
        self.font = pygame.font.SysFont('SimHei', 36)
        self.number_font = pygame.font.SysFont('Arial', 48, bold=True)
        
        # 计算游戏区域的起始位置（居中显示）
        self.board_width = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * CELL_MARGIN
        self.board_height = self.board_width
        self.board_start_x = (WINDOW_WIDTH - self.board_width) // 2
        self.board_start_y = (WINDOW_HEIGHT - self.board_height) // 2
        
        # 初始化暂停菜单按钮
        button_width = 200
        button_height = 50
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        self.continue_button = pygame.Rect(button_x, WINDOW_HEIGHT // 2 - 60, button_width, button_height)
        self.menu_button = pygame.Rect(button_x, WINDOW_HEIGHT // 2 + 10, button_width, button_height)
        
        # 添加两个初始数字
        self.add_new_tile()
        self.add_new_tile()
    
    def add_new_tile(self):
        """在空格子中随机添加一个新数字（2或4）"""
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4
    
    def move(self, direction):
        """移动并合并数字
        
        参数:
            direction: 移动方向，'up', 'down', 'left', 'right'
        
        返回:
            bool: True表示有移动或合并发生，False表示没有变化
        """
        moved = False
        if direction in ['up', 'down']:
            for j in range(GRID_SIZE):
                # 获取当前列的非零数字
                column = [self.grid[i][j] for i in range(GRID_SIZE)]
                column = [x for x in column if x != 0]
                
                # 合并相同的数字
                i = 0
                while i < len(column) - 1:
                    if column[i] == column[i + 1]:
                        column[i] *= 2
                        self.score += column[i]
                        column.pop(i + 1)
                        moved = True
                    i += 1
                
                # 填充零
                while len(column) < GRID_SIZE:
                    if direction == 'up':
                        column.append(0)
                    else:
                        column.insert(0, 0)
                
                # 更新网格
                for i in range(GRID_SIZE):
                    if self.grid[i][j] != column[i]:
                        moved = True
                    self.grid[i][j] = column[i]
        
        else:  # left or right
            for i in range(GRID_SIZE):
                # 获取当前行的非零数字
                row = [self.grid[i][j] for j in range(GRID_SIZE)]
                row = [x for x in row if x != 0]
                
                # 合并相同的数字
                j = 0
                while j < len(row) - 1:
                    if row[j] == row[j + 1]:
                        row[j] *= 2
                        self.score += row[j]
                        row.pop(j + 1)
                        moved = True
                    j += 1
                
                # 填充零
                while len(row) < GRID_SIZE:
                    if direction == 'left':
                        row.append(0)
                    else:
                        row.insert(0, 0)
                
                # 更新网格
                for j in range(GRID_SIZE):
                    if self.grid[i][j] != row[j]:
                        moved = True
                    self.grid[i][j] = row[j]
        
        return moved

    def check_game_over(self):
        """检查游戏是否结束
        
        返回:
            bool: True表示游戏结束，False表示可以继续
        """
        # 检查是否有空格子
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == 0:
                    return False
        
        # 检查是否有相邻的相同数字
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                current = self.grid[i][j]
                # 检查右边
                if j < GRID_SIZE - 1 and current == self.grid[i][j + 1]:
                    return False
                # 检查下边
                if i < GRID_SIZE - 1 and current == self.grid[i + 1][j]:
                    return False
        
        return True
    
    def draw(self):
        """绘制游戏画面
        
        绘制游戏网格、数字和得分信息
        """
        self.window.fill(GRAY)
        
        # 绘制游戏区域背景
        board_rect = pygame.Rect(self.board_start_x, self.board_start_y,
                               self.board_width, self.board_height)
        pygame.draw.rect(self.window, (187, 173, 160), board_rect)
        
        # 绘制每个格子
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.grid[i][j]
                x = self.board_start_x + CELL_MARGIN * (j + 1) + CELL_SIZE * j
                y = self.board_start_y + CELL_MARGIN * (i + 1) + CELL_SIZE * i
                
                # 绘制格子背景
                cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                color = TILE_COLORS.get(value, (237, 194, 46))  # 使用默认颜色
                pygame.draw.rect(self.window, color, cell_rect, border_radius=5)
                
                # 绘制数字
                if value != 0:
                    text_color = WHITE if value > 4 else BLACK
                    text = self.number_font.render(str(value), True, text_color)
                    text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                    self.window.blit(text, text_rect)
        
        # 显示得分
        score_text = self.font.render(f'得分: {self.score}', True, WHITE)
        self.window.blit(score_text, (10, 10))
        
        # 显示游戏结束信息
        if self.game_over:
            game_over_text = self.font.render('游戏结束! 按R重新开始', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, 30))
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
        
        pygame.display.flip()
    
    def handle_input(self):
        """处理用户输入
        
        处理键盘按键和手柄输入
        
        返回:
            bool: True表示要返回主菜单，False表示继续游戏
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.show_pause_menu:
                        self.show_pause_menu = False
                        self.paused = False
                    else:
                        self.show_pause_menu = True
                        self.paused = True
                elif event.key == pygame.K_r and self.game_over:
                    self.__init__()
                elif not self.paused and not self.game_over:
                    moved = False
                    if event.key == pygame.K_UP:
                        moved = self.move('up')
                    elif event.key == pygame.K_DOWN:
                        moved = self.move('down')
                    elif event.key == pygame.K_LEFT:
                        moved = self.move('left')
                    elif event.key == pygame.K_RIGHT:
                        moved = self.move('right')
                    
                    if moved:
                        self.add_new_tile()
                        if self.check_game_over():
                            self.game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN and self.show_pause_menu:
                mouse_pos = pygame.mouse.get_pos()
                if self.continue_button.collidepoint(mouse_pos):
                    self.show_pause_menu = False
                    self.paused = False
                elif self.menu_button.collidepoint(mouse_pos):
                    return True
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
                        self.__init__()
        
        # 处理手柄摇杆和方向键输入
        if not self.game_over and not self.paused:
            for joystick in pygame.joystick.get_count() and [pygame.joystick.Joystick(0)]:
                moved = False
                # 处理左摇杆
                axis_x = joystick.get_axis(0)  # 水平轴
                axis_y = joystick.get_axis(1)  # 垂直轴
                if abs(axis_x) > 0.5 or abs(axis_y) > 0.5:
                    if abs(axis_x) > abs(axis_y):
                        if axis_x < -0.5:
                            moved = self.move('left')
                        elif axis_x > 0.5:
                            moved = self.move('right')
                    else:
                        if axis_y < -0.5:
                            moved = self.move('up')
                        elif axis_y > 0.5:
                            moved = self.move('down')
                
                # 处理方向键
                hat = joystick.get_hat(0)
                if hat[0] != 0 or hat[1] != 0:
                    if hat[0] < 0:
                        moved = self.move('left')
                    elif hat[0] > 0:
                        moved = self.move('right')
                    elif hat[1] > 0:
                        moved = self.move('up')
                    elif hat[1] < 0:
                        moved = self.move('down')
                
                if moved:
                    self.add_new_tile()
                    if self.check_game_over():
                        self.game_over = True
        return False