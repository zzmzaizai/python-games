import pygame
import sys
import random
import math  # 添加math模块用于三角函数计算

# 初始化 Pygame
pygame.init()

# 定义游戏中使用的颜色（RGB格式）
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)  # 黄色砖块
ORANGE = (255, 165, 0)  # 橙色砖块
GRAY = (128, 128, 128)  # 用于半透明遮罩
GRAY_TRANSPARENT = (128, 128, 128, 128)  # 半透明灰色

# 游戏窗口设置
WINDOW_WIDTH = 800  # 游戏窗口宽度
WINDOW_HEIGHT = 600  # 游戏窗口高度
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # 创建游戏窗口
pygame.display.set_caption('打砖块游戏')  # 设置窗口标题

# 游戏对象类定义
class Paddle:
    """挡板类
    
    玩家控制的挡板，可以左右移动来反弹球。
    属性:
        width: 挡板宽度
        height: 挡板高度
        speed: 移动速度
        rect: 碰撞检测用的矩形对象
    """
    def __init__(self):
        """初始化挡板
        
        设置挡板的初始位置、大小和速度
        """
        self.width = 100
        self.height = 20
        self.x = WINDOW_WIDTH // 2 - self.width // 2  # 初始位置在窗口底部中间
        self.y = WINDOW_HEIGHT - 40
        self.speed = 8  # 移动速度
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, direction):
        """移动挡板
        
        根据输入的方向移动挡板，并确保不会超出屏幕边界
        参数:
            direction: 移动方向，'left'表示左移，'right'表示右移
        """
        if direction == 'left' and self.rect.left > 0:
            self.rect.x -= self.speed
        if direction == 'right' and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.speed

    def draw(self):
        """绘制挡板
        
        在游戏窗口上绘制挡板
        """
        pygame.draw.rect(window, BLUE, self.rect)

class Ball:
    """球类
    
    游戏中的球体，会在屏幕上移动并与其他物体发生碰撞。
    属性:
        radius: 球的半径
        dx, dy: 球的水平和垂直速度
        rect: 用于碰撞检测的矩形对象
    """
    def __init__(self):
        """初始化球
        
        设置球的初始位置、大小和速度
        """
        self.radius = 10
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT - 60
        self.dx = 5  # 水平速度
        self.dy = -5  # 垂直速度，负值表示向上运动
        # 创建一个矩形用于碰撞检测
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                               self.radius * 2, self.radius * 2)

    def move(self):
        """移动球
        
        更新球的位置并处理与墙壁的碰撞
        """
        # 更新球的位置
        self.rect.x += self.dx
        self.rect.y += self.dy

        # 处理与墙壁的碰撞
        # 当球碰到左右墙壁时，水平速度反向
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.dx = -self.dx
        # 当球碰到上边界时，垂直速度反向
        if self.rect.top <= 0:
            self.dy = -self.dy

    def draw(self):
        """绘制球
        
        在游戏窗口上绘制球体
        """
        pygame.draw.circle(window, RED,
                          (self.rect.centerx, self.rect.centery),
                          self.radius)

class Brick:
    """砖块类
    
    游戏中的砖块，可以被球击碎。
    属性:
        rect: 砖块的矩形区域
        color: 砖块的颜色
        hits_required: 需要击中多少次才能消除
        points: 击碎砖块获得的分数
    """
    def __init__(self, x, y, width=60, height=20, color=WHITE):
        """初始化砖块
        
        参数:
            x, y: 砖块的位置
            width, height: 砖块的宽度和高度
            color: 砖块的颜色
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hits_required = 1  # 默认需要击中一次

    def draw(self):
        """绘制砖块
        
        在游戏窗口上绘制砖块
        """
        pygame.draw.rect(window, self.color, self.rect)

class Game:
    """游戏主类
    
    管理游戏的主要逻辑，包括初始化、更新和绘制游戏对象。
    属性:
        paddle: 挡板对象
        ball: 球对象
        bricks: 砖块列表
        level: 当前关卡
        score: 得分
        lives: 生命值
        game_over: 游戏是否结束
        paused: 游戏是否暂停
    """
    def __init__(self):
        """初始化游戏
        
        创建游戏对象并设置初始状态
        """
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = []
        self.level = 1
        self.score = 0
        self.lives = 3  # 初始生命值
        self.game_over = False
        self.paused = False  # 暂停状态
        self.show_pause_menu = False  # 是否显示暂停菜单
        self.setup_level(self.level)
        
        # 初始化暂停菜单按钮
        button_width = 200
        button_height = 50
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        self.continue_button = pygame.Rect(button_x, WINDOW_HEIGHT // 2 - 60, button_width, button_height)
        self.menu_button = pygame.Rect(button_x, WINDOW_HEIGHT // 2 + 10, button_width, button_height)

    def setup_level(self, level):
        """设置关卡
        
        根据当前关卡创建砖块布局。随着关卡提升，砖块数量增加，
        并且出现需要多次击中才能消除的特殊砖块。
        
        参数:
            level: 关卡编号，影响砖块的行数和特殊砖块的出现概率
        """
        self.bricks.clear()  # 清除现有砖块
        
        # 根据关卡增加砖块行数，每过一关增加一行
        rows = 3 + level  # 基础3行，每关增加1行
        cols = 15  # 列数固定为15列
        brick_width = 40  # 砖块宽度
        brick_height = 15  # 砖块高度
        top_offset = 50  # 顶部留空距离

        # 创建砖块阵列，不同位置的砖块具有不同的颜色和分值
        for row in range(rows):
            for col in range(cols):
                # 计算砖块位置，包括间距
                x = col * (brick_width + 5) + 45  # 水平间距5像素
                y = row * (brick_height + 3) + top_offset  # 垂直间距3像素
                
                # 根据行数设置不同颜色和分数的砖块
                if row < 2:
                    color = ORANGE  # 顶部使用橙色
                    points = 30     # 顶部砖块分值高
                elif row < 4:
                    color = YELLOW  # 中部使用黄色
                    points = 20     # 中部砖块分值中等
                else:
                    color = WHITE   # 底部使用白色
                    points = 10     # 底部砖块分值低

                # 在高级关卡中随机添加需要多次击中的特殊砖块
                if level >= 3 and random.random() < 0.2:  # 20%的概率生成特殊砖块
                    color = GREEN   # 特殊砖块使用绿色
                    points = 50     # 特殊砖块分值更高
                    brick = Brick(x, y, brick_width, brick_height, color)
                    brick.hits_required = 2  # 需要击中两次才能消除
                    brick.points = points
                else:
                    brick = Brick(x, y, brick_width, brick_height, color)
                    brick.points = points
                self.bricks.append(brick)

        # 随关卡提高球的速度，增加游戏难度
        self.ball.dx = 5 + level  # 水平速度随关卡提升
        self.ball.dy = -(5 + level)  # 垂直速度随关卡提升

    def handle_collisions(self):
        """处理碰撞
        
        处理球与挡板和砖块的碰撞。对于挡板碰撞，根据击球位置计算反弹角度，
        使游戏更有趣味性。对于砖块碰撞，处理砖块的消除和得分。
        """
        # 处理球与挡板的碰撞，实现智能反弹
        if self.ball.rect.colliderect(self.paddle.rect):
            # 根据击球位置改变反弹角度，使游戏更有趣
            relative_intersect_x = (self.paddle.rect.centerx - self.ball.rect.centerx)
            normalized_intersect = relative_intersect_x / (self.paddle.width / 2)
            bounce_angle = normalized_intersect * 60  # 最大反弹角度为60度
            speed = (self.ball.dx ** 2 + self.ball.dy ** 2) ** 0.5
            # 使用三角函数计算新的速度分量
            self.ball.dx = -speed * math.sin(math.radians(bounce_angle))
            self.ball.dy = -speed * math.cos(math.radians(bounce_angle))

        # 处理球与砖块的碰撞
        for brick in self.bricks[:]:
            if self.ball.rect.colliderect(brick.rect):
                brick.hits_required -= 1  # 砖块被击中次数减1
                if brick.hits_required <= 0:
                    self.bricks.remove(brick)  # 移除被完全击碎的砖块
                    self.score += brick.points  # 增加得分
                self.ball.dy = -self.ball.dy  # 球反弹

        # 检查是否完成关卡
        if not self.bricks:
            if self.level < 5:  # 最多5关
                self.level += 1  # 进入下一关
                self.setup_level(self.level)  # 设置新关卡
                self.ball = Ball()  # 重置球的位置
                self.paddle = Paddle()  # 重置挡板位置
            else:
                self.game_over = True  # 通关结束

    def run(self):
        """运行游戏主循环
        
        控制游戏的主要流程，包括更新游戏状态、处理碰撞、渲染画面等
        """
        clock = pygame.time.Clock()
    
        while not self.game_over:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # ESC键控制暂停菜单
                        if self.show_pause_menu:
                            self.show_pause_menu = False
                            self.paused = False
                        else:
                            self.show_pause_menu = True
                            self.paused = True
                    if event.key == pygame.K_r:  # R键重新开始
                        self.__init__()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.show_pause_menu:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.continue_button.collidepoint(mouse_pos):
                        self.show_pause_menu = False
                        self.paused = False
                    elif self.menu_button.collidepoint(mouse_pos):
                        return True  # 返回主菜单
                # 添加手柄按钮事件处理
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
                        elif event.button == 0:  # A键重新开始
                            self.__init__()
    
            # 如果游戏未暂停，更新游戏状态
            if not self.paused:
                # 处理键盘输入
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.paddle.move('left')
                if keys[pygame.K_RIGHT]:
                    self.paddle.move('right')
    
                # 处理手柄输入
                if pygame.joystick.get_count() > 0:
                    try:
                        joystick = pygame.joystick.Joystick(0)
                        # 处理左摇杆
                        axis_x = joystick.get_axis(0)  # 水平轴
                        if axis_x < -0.5:  # 左
                            self.paddle.move('left')
                        elif axis_x > 0.5:  # 右
                            self.paddle.move('right')
                        
                        # 处理方向键
                        hat = joystick.get_hat(0)
                        if hat[0] < 0:  # 左
                            self.paddle.move('left')
                        elif hat[0] > 0:  # 右
                            self.paddle.move('right')
                    except pygame.error:
                        pass  # 忽略手柄错误
    
                # 更新球的位置和处理碰撞
                self.ball.move()
                self.handle_collisions()
    
                # 检查球是否落到底部
                if self.ball.rect.bottom >= WINDOW_HEIGHT:
                    self.lives -= 1  # 失去一条生命
                    if self.lives <= 0:
                        self.game_over = True
                    else:
                        self.ball = Ball()  # 重置球的位置
    
            # 绘制游戏画面
            window.fill(BLACK)  # 清空屏幕
            self.paddle.draw()
            self.ball.draw()
            for brick in self.bricks:
                brick.draw()

            # 显示得分、关卡和生命值
            font = pygame.font.SysFont('SimHei', 36)  # 使用系统黑体字体
            score_text = font.render(f'得分: {self.score}', True, WHITE)
            level_text = font.render(f'关卡: {self.level}', True, WHITE)
            lives_text = font.render(f'生命: {self.lives}', True, WHITE)
            window.blit(score_text, (10, 10))
            window.blit(level_text, (10, 40))
            window.blit(lives_text, (10, 70))
            
            # 绘制暂停菜单
            if self.show_pause_menu:
                # 创建半透明遮罩层
                overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                overlay.fill(GRAY)
                overlay.set_alpha(128)
                window.blit(overlay, (0, 0))
                
                # 绘制暂停菜单按钮
                pygame.draw.rect(window, BLUE, self.continue_button)
                pygame.draw.rect(window, BLUE, self.menu_button)
                
                # 绘制按钮文本
                font = pygame.font.SysFont('SimHei', 36)  # 使用系统黑体字体
                continue_text = font.render('继续游戏', True, WHITE)
                menu_text = font.render('返回主菜单', True, WHITE)
                
                # 居中显示文本
                continue_text_rect = continue_text.get_rect(center=self.continue_button.center)
                menu_text_rect = menu_text.get_rect(center=self.menu_button.center)
                
                window.blit(continue_text, continue_text_rect)
                window.blit(menu_text, menu_text_rect)
            
            pygame.display.flip()
            clock.tick(60)  # 控制游戏帧率为60FPS

if __name__ == '__main__':
    game = Game()
    game.run()