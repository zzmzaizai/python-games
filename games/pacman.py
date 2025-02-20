import pygame
import sys
import random
import math

# 初始化 Pygame 游戏引擎
pygame.init()

# 定义游戏中使用的颜色（RGB格式）
WHITE = (255, 255, 255)   # 白色，用于糖豆
BLACK = (0, 0, 0)        # 黑色，用于背景
YELLOW = (255, 255, 0)   # 黄色，用于玩家
RED = (255, 0, 0)       # 红色，用于敌人1
BLUE = (0, 0, 255)      # 蓝色，用于敌人2
PINK = (255, 192, 203)   # 粉色，用于敌人3

# 游戏窗口和网格设置
WINDOW_WIDTH = 800      # 游戏窗口宽度
WINDOW_HEIGHT = 600     # 游戏窗口高度
GRID_SIZE = 20         # 网格大小（像素）
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE    # 网格宽度数量
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE  # 网格高度数量

class Player:
    """玩家类
    
    控制玩家角色的移动、动画和状态
    
    属性:
        x, y: 玩家位置坐标
        radius: 玩家半径
        speed: 移动速度
        direction: 朝向角度（用于动画）
        score: 得分
        lives: 生命值
    """
    def __init__(self):
        """初始化玩家
        
        设置玩家的初始位置、大小、速度和状态
        """
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.radius = 15
        self.speed = 5
        self.direction = 0  # 角度，用于动画
        self.score = 0
        self.lives = 3

    def move(self, dx, dy):
        """移动玩家
        
        根据输入方向移动玩家，并确保不会移出屏幕
        
        参数:
            dx: x方向的移动量（-1左移，1右移，0不动）
            dy: y方向的移动量（-1上移，1下移，0不动）
        """
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # 确保玩家不会移出屏幕
        if 0 + self.radius <= new_x <= WINDOW_WIDTH - self.radius:
            self.x = new_x
        if 0 + self.radius <= new_y <= WINDOW_HEIGHT - self.radius:
            self.y = new_y

        # 更新朝向角度（用于动画）
        if dx != 0 or dy != 0:
            self.direction = math.degrees(math.atan2(-dy, dx))

    def draw(self, surface):
        """绘制玩家
        
        在游戏窗口上绘制玩家角色，包括圆形身体和三角形嘴巴
        
        参数:
            surface: pygame的显示表面对象
        """
        # 绘制玩家（类似吃豆人的形状）
        pygame.draw.circle(surface, YELLOW, (int(self.x), int(self.y)), self.radius)
        # 绘制嘴巴（简单的三角形）
        mouth_points = [
            (self.x, self.y),
            (self.x + self.radius * math.cos(math.radians(self.direction + 20)),
             self.y - self.radius * math.sin(math.radians(self.direction + 20))),
            (self.x + self.radius * math.cos(math.radians(self.direction - 20)),
             self.y - self.radius * math.sin(math.radians(self.direction - 20)))
        ]
        pygame.draw.polygon(surface, BLACK, mouth_points)

class Enemy:
    """敌人类
    
    控制敌人的移动和行为，会追踪玩家
    
    属性:
        x, y: 敌人位置坐标
        radius: 敌人半径
        color: 敌人颜色
        speed: 移动速度
        direction: 移动方向
    """
    def __init__(self, x, y, color):
        """初始化敌人
        
        参数:
            x, y: 初始位置
            color: 敌人颜色
        """
        self.x = x
        self.y = y
        self.radius = 15
        self.color = color
        self.speed = 3
        self.direction = random.randint(0, 360)

    def move(self, player_x, player_y):
        """移动敌人
        
        根据玩家位置计算移动方向，并加入随机性使移动更有趣
        
        参数:
            player_x: 玩家x坐标
            player_y: 玩家y坐标
        """
        # 计算到玩家的方向向量
        dx = player_x - self.x
        dy = player_y - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist != 0:
            # 标准化方向向量并应用速度
            dx = dx / dist * self.speed
            dy = dy / dist * self.speed
            
            # 加入随机性，使移动更有趣
            if random.random() < 0.02:  # 2%的概率改变方向
                dx += random.uniform(-2, 2)
                dy += random.uniform(-2, 2)
            
            new_x = self.x + dx
            new_y = self.y + dy
            
            # 确保敌人不会移出屏幕
            if 0 + self.radius <= new_x <= WINDOW_WIDTH - self.radius:
                self.x = new_x
            if 0 + self.radius <= new_y <= WINDOW_HEIGHT - self.radius:
                self.y = new_y

    def draw(self, surface):
        """绘制敌人
        
        参数:
            surface: pygame的显示表面对象
        """
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

class Candy:
    """糖豆类
    
    游戏中的收集物，被玩家吃到后增加分数
    
    属性:
        radius: 糖豆半径
        color: 糖豆颜色
        position: 位置坐标
    """
    def __init__(self):
        """初始化糖豆
        
        设置糖豆的大小、颜色，并随机放置位置
        """
        self.radius = 5
        self.color = WHITE
        self.position = self.get_random_position()

    def get_random_position(self):
        """获取随机位置
        
        返回:
            tuple: 随机生成的(x,y)坐标
        """
        x = random.randint(self.radius, WINDOW_WIDTH - self.radius)
        y = random.randint(self.radius, WINDOW_HEIGHT - self.radius)
        return (x, y)

    def draw(self, surface):
        """绘制糖豆
        
        参数:
            surface: pygame的显示表面对象
        """
        pygame.draw.circle(surface, self.color, self.position, self.radius)

class Game:
    """游戏主类
    
    控制游戏的主要逻辑，包括初始化、更新和渲染
    
    属性:
        window: pygame显示窗口
        player: 玩家对象
        enemies: 敌人列表
        candies: 糖豆列表
        font: 字体对象
        game_over: 游戏是否结束
    """
    def __init__(self):
        """初始化游戏
        
        创建游戏窗口，初始化游戏对象
        """
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('吃糖豆')
        self.player = Player()
        # 创建三个不同颜色的敌人，分别在不同位置
        self.enemies = [
            Enemy(100, 100, RED),
            Enemy(WINDOW_WIDTH - 100, 100, PINK),
            Enemy(100, WINDOW_HEIGHT - 100, BLUE)
        ]
        self.candies = [Candy() for _ in range(20)]  # 初始创建20个糖豆
        self.font = pygame.font.SysFont('SimHei', 36)  # 使用系统黑体字体
        self.game_over = False

    def handle_keys(self):
        """处理键盘输入
        
        处理游戏的各种输入事件，包括移动、退出和重启
        
        返回:
            bool: True表示要返回主菜单，False表示继续游戏
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True  # 返回主菜单
                elif event.key == pygame.K_r and self.game_over:
                    self.__init__()
                    self.game_over = False
            # 添加手柄按钮事件处理
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 7:  # Start键
                    return True  # 返回主菜单
                elif event.button == 0 and self.game_over:  # A键重新开始
                    self.__init__()
                    self.game_over = False

        if not self.game_over:
            # 处理方向键移动
            dx = dy = 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                dx = -1
            if keys[pygame.K_RIGHT]:
                dx = 1
            if keys[pygame.K_UP]:
                dy = -1
            if keys[pygame.K_DOWN]:
                dy = 1

            # 处理手柄输入
            for joystick in pygame.joystick.get_count() and [pygame.joystick.Joystick(0)]:
                # 处理左摇杆
                axis_x = joystick.get_axis(0)  # 水平轴
                axis_y = joystick.get_axis(1)  # 垂直轴
                if axis_x < -0.5:  # 左
                    dx = -1
                elif axis_x > 0.5:  # 右
                    dx = 1
                if axis_y < -0.5:  # 上
                    dy = -1
                elif axis_y > 0.5:  # 下
                    dy = 1

                # 处理方向键
                hat = joystick.get_hat(0)
                if hat[0] < 0:  # 左
                    dx = -1
                elif hat[0] > 0:  # 右
                    dx = 1
                if hat[1] > 0:  # 上
                    dy = -1
                elif hat[1] < 0:  # 下
                    dy = 1

            self.player.move(dx, dy)

        return False

    def check_collisions(self):
        """检查碰撞
        
        检查玩家与糖豆和敌人的碰撞，处理得分和生命值
        """
        # 检查与糖豆的碰撞
        for candy in self.candies[:]:
            dx = self.player.x - candy.position[0]
            dy = self.player.y - candy.position[1]
            if math.sqrt(dx * dx + dy * dy) < self.player.radius + candy.radius:
                self.candies.remove(candy)
                self.player.score += 10
                if not self.candies:  # 如果所有糖豆都被吃完
                    self.candies.extend([Candy() for _ in range(20)])

        # 检查与敌人的碰撞
        for enemy in self.enemies:
            dx = self.player.x - enemy.x
            dy = self.player.y - enemy.y
            if math.sqrt(dx * dx + dy * dy) < self.player.radius + enemy.radius:
                self.player.lives -= 1
                if self.player.lives <= 0:
                    self.game_over = True
                else:
                    # 重置玩家位置
                    self.player.x = WINDOW_WIDTH // 2
                    self.player.y = WINDOW_HEIGHT // 2

    def run(self):
        """运行游戏主循环
        
        控制游戏的主要流程，包括更新游戏状态、处理碰撞、渲染画面等
        """
        clock = pygame.time.Clock()

        while True:
            if self.handle_keys():  # 如果返回True，表示要返回主菜单
                break

            if not self.game_over:
                # 更新敌人位置
                for enemy in self.enemies:
                    enemy.move(self.player.x, self.player.y)

                # 检查碰撞
                self.check_collisions()

            # 绘制游戏画面
            self.window.fill(BLACK)
            
            # 绘制所有对象
            for candy in self.candies:
                candy.draw(self.window)
            for enemy in self.enemies:
                enemy.draw(self.window)
            self.player.draw(self.window)

            # 显示分数和生命值
            score_text = self.font.render(f'得分: {self.player.score}', True, WHITE)
            lives_text = self.font.render(f'生命: {self.player.lives}', True, WHITE)
            self.window.blit(score_text, (10, 10))
            self.window.blit(lives_text, (10, 50))

            if self.game_over:
                game_over_text = self.font.render('游戏结束! 按R重新开始', True, WHITE)
                text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                self.window.blit(game_over_text, text_rect)

            pygame.display.flip()
            clock.tick(60)  # 控制游戏速度，60帧每秒

if __name__ == '__main__':
    game = Game()
    game.run()
    game.run()