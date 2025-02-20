import pygame
import random
import sys

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# 游戏配置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 25
GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_X = (WINDOW_WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2
GRID_Y = (WINDOW_HEIGHT - GRID_HEIGHT * BLOCK_SIZE) // 2

# 全局变量
window = None

# 方块形状定义
TETROMINOS = {
    'I': [
        [[0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        CYAN
    ],
    'O': [
        [[1, 1],
         [1, 1]],
        YELLOW
    ],
    'T': [
        [[0, 1, 0],
         [1, 1, 1],
         [0, 0, 0]],
        MAGENTA
    ],
    'S': [
        [[0, 1, 1],
         [1, 1, 0],
         [0, 0, 0]],
        GREEN
    ],
    'Z': [
        [[1, 1, 0],
         [0, 1, 1],
         [0, 0, 0]],
        RED
    ],
    'J': [
        [[1, 0, 0],
         [1, 1, 1],
         [0, 0, 0]],
        BLUE
    ],
    'L': [
        [[0, 0, 1],
         [1, 1, 1],
         [0, 0, 0]],
        ORANGE
    ]
}

class Tetromino:
    """俄罗斯方块类
    
    表示一个正在下落的方块。包含方块的形状、位置和旋转状态。
    
    属性:
        shape: 方块形状
        color: 方块颜色
        x: 方块在网格中的x坐标
        y: 方块在网格中的y坐标
        rotation: 当前旋转状态
    """
    def __init__(self):
        """初始化方块
        
        随机选择一个方块形状并设置初始位置
        """
        self.shape = random.choice(list(TETROMINOS.keys()))
        self.blocks = TETROMINOS[self.shape][0]
        self.color = TETROMINOS[self.shape][1]
        self.x = GRID_WIDTH // 2 - len(self.blocks[0]) // 2
        self.y = 0
        self.rotation = 0
    
    def rotate(self):
        """旋转方块
        
        将方块顺时针旋转90度
        """
        # 创建新的旋转后的方块数组
        rotated = [[0 for _ in range(len(self.blocks))] for _ in range(len(self.blocks[0]))]
        for i in range(len(self.blocks)):
            for j in range(len(self.blocks[0])):
                rotated[j][len(self.blocks) - 1 - i] = self.blocks[i][j]
        return rotated

class Game:
    """游戏主类
    
    控制游戏的主要逻辑，包括初始化、更新和渲染
    
    属性:
        grid: 游戏网格
        current_piece: 当前下落的方块
        next_piece: 下一个方块
        score: 得分
        level: 当前等级
        game_over: 游戏是否结束
        paused: 游戏是否暂停
    """
    def __init__(self):
        """初始化游戏
        
        创建游戏窗口，初始化游戏状态
        """
        global window
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('俄罗斯方块')
        
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.score = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self.fall_time = 0
        self.fall_speed = 1000  # 初始下落速度（毫秒）
        self.font = pygame.font.SysFont('SimHei', 36)
    
    def handle_input(self):
        """处理用户输入
        
        处理键盘和手柄的输入事件
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                elif not self.paused and not self.game_over:
                    if event.key == pygame.K_LEFT:
                        self.move_piece(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.move_piece(1)
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
                    elif event.key == pygame.K_DOWN:
                        self.move_piece_down()
                    elif event.key == pygame.K_SPACE:
                        self.drop_piece()
                elif event.key == pygame.K_r and self.game_over:
                    self.__init__()
            
            # 手柄控制
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 7:  # Start键
                    self.paused = not self.paused
                elif not self.paused and not self.game_over:
                    if event.button == 0:  # A键
                        self.rotate_piece()
                    elif event.button == 1:  # B键
                        self.drop_piece()
                elif event.button == 0 and self.game_over:  # A键重新开始
                    self.__init__()
        
        # 手柄摇杆和方向键
        if pygame.joystick.get_count() > 0:
            try:
                joystick = pygame.joystick.Joystick(0)
                if not self.paused and not self.game_over:
                    # 左摇杆
                    axis_x = joystick.get_axis(0)
                    if axis_x < -0.5:
                        self.move_piece(-1)
                    elif axis_x > 0.5:
                        self.move_piece(1)
                    
                    # 方向键
                    hat = joystick.get_hat(0)
                    if hat[0] < 0:
                        self.move_piece(-1)
                    elif hat[0] > 0:
                        self.move_piece(1)
                    if hat[1] < 0:
                        self.move_piece_down()
            except pygame.error:
                pass
    
    def move_piece(self, dx):
        """移动方块
        
        水平移动当前方块
        
        参数:
            dx: 移动的方向（-1为左，1为右）
        """
        self.current_piece.x += dx
        if not self.is_valid_move():
            self.current_piece.x -= dx
    
    def rotate_piece(self):
        """旋转方块
        
        尝试旋转当前方块，如果旋转后位置无效则取消旋转
        """
        old_blocks = self.current_piece.blocks
        self.current_piece.blocks = self.current_piece.rotate()
        if not self.is_valid_move():
            self.current_piece.blocks = old_blocks
    
    def move_piece_down(self):
        """向下移动方块
        
        将当前方块向下移动一格
        """
        self.current_piece.y += 1
        if not self.is_valid_move():
            self.current_piece.y -= 1
            self.place_piece()
    
    def drop_piece(self):
        """快速下落
        
        将当前方块直接下落到底部
        """
        while self.is_valid_move():
            self.current_piece.y += 1
        self.current_piece.y -= 1
        self.place_piece()
    
    def is_valid_move(self):
        """检查移动是否有效
        
        检查当前方块的位置是否合法
        
        返回:
            bool: 如果移动有效返回True，否则返回False
        """
        for y, row in enumerate(self.current_piece.blocks):
            for x, cell in enumerate(row):
                if cell:
                    if (self.current_piece.x + x < 0 or
                        self.current_piece.x + x >= GRID_WIDTH or
                        self.current_piece.y + y >= GRID_HEIGHT or
                        (self.current_piece.y + y >= 0 and
                         self.grid[self.current_piece.y + y][self.current_piece.x + x])):
                        return False
        return True
    
    def place_piece(self):
        """放置方块
        
        将当前方块固定到网格中，检查是否有可以消除的行
        """
        for y, row in enumerate(self.current_piece.blocks):
            for x, cell in enumerate(row):
                if cell:
                    if self.current_piece.y + y < 0:
                        self.game_over = True
                        return
                    self.grid[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color
        
        # 检查是否有完整的行
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(cell is not None for cell in self.grid[y]):
                lines_cleared += 1
                for y2 in range(y, 0, -1):
                    self.grid[y2] = self.grid[y2 - 1][:]
                self.grid[0] = [None] * GRID_WIDTH
            else:
                y -= 1
        
        # 更新分数
        if lines_cleared > 0:
            self.score += [100, 300, 500, 800][lines_cleared - 1] * self.level
            self.level = self.score // 5000 + 1
            self.fall_speed = max(100, 1000 - (self.level - 1) * 100)
        
        # 生成新方块
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()
    
    def draw(self):
        """绘制游戏画面
        
        绘制游戏网格、当前方块、下一个方块和游戏信息
        """
        window.fill(BLACK)
        
        # 绘制网格
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(window, WHITE,
                               (GRID_X + x * BLOCK_SIZE,
                                GRID_Y + y * BLOCK_SIZE,
                                BLOCK_SIZE, BLOCK_SIZE), 1)
                if self.grid[y][x]:
                    pygame.draw.rect(window, self.grid[y][x],
                                   (GRID_X + x * BLOCK_SIZE + 1,
                                    GRID_Y + y * BLOCK_SIZE + 1,
                                    BLOCK_SIZE - 2, BLOCK_SIZE - 2))
        
        # 绘制当前方块
        if not self.game_over:
            for y, row in enumerate(self.current_piece.blocks):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(window, self.current_piece.color,
                                       (GRID_X + (self.current_piece.x + x) * BLOCK_SIZE + 1,
                                        GRID_Y + (self.current_piece.y + y) * BLOCK_SIZE + 1,
                                        BLOCK_SIZE - 2, BLOCK_SIZE - 2))
        
        # 绘制下一个方块预览
        preview_x = GRID_X + GRID_WIDTH * BLOCK_SIZE + 50
        preview_y = GRID_Y
        pygame.draw.rect(window, WHITE, (preview_x, preview_y, 100, 100), 1)
        for y, row in enumerate(self.next_piece.blocks):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(window, self.next_piece.color,
                                   (preview_x + x * BLOCK_SIZE + 10,
                                    preview_y + y * BLOCK_SIZE + 10,
                                    BLOCK_SIZE - 2, BLOCK_SIZE - 2))
        
        # 显示分数