import pygame
import sys
import random
import math

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# 游戏配置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 15
PADDLE_SPEED = 5
BALL_SPEED = 7

# 全局变量
window = None

class Paddle:
    """挡板类
    
    玩家控制的挡板，可以上下移动来击球
    
    属性:
        rect: 挡板的矩形区域
        speed: 移动速度
        score: 得分
    """
    def __init__(self, x, color):
        """初始化挡板
        
        参数:
            x: 挡板的水平位置
            color: 挡板的颜色
        """
        self.rect = pygame.Rect(x, WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2,
                              PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED
        self.score = 0
        self.color = color
    
    def move(self, up=True):
        """移动挡板
        
        参数:
            up: True表示向上移动，False表示向下移动
        """
        if up and self.rect.top > 0:
            self.rect.y -= self.speed
        if not up and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.speed
    
    def draw(self):
        """绘制挡板"""
        pygame.draw.rect(window, self.color, self.rect)

class Ball:
    """球类
    
    游戏中的球，在场地中移动并与挡板碰撞
    
    属性:
        rect: 球的矩形区域
        dx: 水平速度
        dy: 垂直速度
        speed: 移动速度
    """
    def __init__(self):
        """初始化球"""
        self.rect = pygame.Rect(WINDOW_WIDTH//2 - BALL_SIZE//2,
                              WINDOW_HEIGHT//2 - BALL_SIZE//2,
                              BALL_SIZE, BALL_SIZE)
        self.speed = BALL_SPEED
        self.reset()
    
    def reset(self):
        """重置球的位置和速度"""
        self.rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        angle = random.uniform(-math.pi/4, math.pi/4)
        if random.choice([True, False]):
            angle += math.pi
        self.dx = self.speed * math.cos(angle)
        self.dy = self.speed * math.sin(angle)
    
    def move(self):
        """移动球"""
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        # 检查上下边界碰撞
        if self.rect.top <= 0 or self.rect.bottom >= WINDOW_HEIGHT:
            self.dy *= -1
    
    def draw(self):
        """绘制球"""
        pygame.draw.ellipse(window, WHITE, self.rect)

class Game:
    """游戏主类
    
    控制游戏的主要逻辑，包括初始化、更新和渲染
    
    属性:
        player1: 左侧玩家
        player2: 右侧玩家
        ball: 球
        game_over: 游戏是否结束
        paused: 游戏是否暂停
    """
    def __init__(self):
        """初始化游戏"""
        global window
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('弹球')
        
        self.player1 = Paddle(50, BLUE)
        self.player2 = Paddle(WINDOW_WIDTH - 50 - PADDLE_WIDTH, RED)
        self.ball = Ball()
        self.game_over = False
        self.paused = False
        self.font = pygame.font.SysFont('SimHei', 36)
        self.win_score = 5  # 获胜所需分数
    
    def handle_input(self):
        """处理用户输入"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r and self.game_over:
                    self.__init__()
            # 手柄控制
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 7:  # Start键
                    self.paused = not self.paused
                elif event.button == 0 and self.game_over:  # A键重新开始
                    self.__init__()
        
        if not self.paused and not self.game_over:
            keys = pygame.key.get_pressed()
            # 玩家1控制（W/S键）
            if keys[pygame.K_w]:
                self.player1.move(True)
            if keys[pygame.K_s]:
                self.player1.move(False)
            # 玩家2控制（上/下方向键）
            if keys[pygame.K_UP]:
                self.player2.move(True)
            if keys[pygame.K_DOWN]:
                self.player2.move(False)
            
            # 手柄控制
            if pygame.joystick.get_count() > 0:
                try:
                    # 第一个手柄控制玩家1
                    joystick1 = pygame.joystick.Joystick(0)
                    axis_y1 = joystick1.get_axis(1)  # 左摇杆垂直轴
                    if axis_y1 < -0.5:
                        self.player1.move(True)
                    elif axis_y1 > 0.5:
                        self.player1.move(False)
                    
                    # 如果有第二个手柄，用于控制玩家2
                    if pygame.joystick.get_count() > 1:
                        joystick2 = pygame.joystick.Joystick(1)
                        axis_y2 = joystick2.get_axis(1)  # 左摇杆垂直轴
                        if axis_y2 < -0.5:
                            self.player2.move(True)
                        elif axis_y2 > 0.5:
                            self.player2.move(False)
                except pygame.error:
                    pass
    
    def update(self):
        """更新游戏状态"""
        if not self.paused and not self.game_over:
            self.ball.move()
            
            # 检查球与挡板的碰撞
            if self.ball.rect.colliderect(self.player1.rect):
                self.ball.dx = abs(self.ball.dx)  # 确保球向右移动
                # 根据击球位置改变反弹角度
                relative_intersect_y = (self.player1.rect.centery - self.ball.rect.centery)
                normalized_intersect = relative_intersect_y / (PADDLE_HEIGHT/2)
                bounce_angle = normalized_intersect * math.pi/3  # 最大反弹角度为60度
                self.ball.dy = -self.ball.speed * math.sin(bounce_angle)
            
            elif self.ball.rect.colliderect(self.player2.rect):
                self.ball.dx = -abs(self.ball.dx)  # 确保球向左移动
                # 根据击球位置改变反弹角度
                relative_intersect_y = (self.player2.rect.centery - self.ball.rect.centery)
                normalized_intersect = relative_intersect_y / (PADDLE_HEIGHT/2)
                bounce_angle = normalized_intersect * math.pi/3  # 最大反弹角度为60度
                self.ball.dy = -self.ball.speed * math.sin(bounce_angle)
            
            # 检查得分
            if self.ball.rect.left <= 0:
                self.player2.score += 1
                self.ball.reset()
            elif self.ball.rect.right >= WINDOW_WIDTH:
                self.player1.score += 1
                self.ball.reset()
            
            # 检查游戏是否结束
            if self.player1.score >= self.win_score or self.player2.score >= self.win_score:
                self.game_over = True
    
    def draw(self):
        """绘制游戏画面"""
        window.fill(BLACK)
        
        # 绘制中间分隔线
        for y in range(0, WINDOW_HEIGHT, 20):
            pygame.draw.rect(window, WHITE,
                           (WINDOW_WIDTH//2 - 5, y, 10, 10))
        
        # 绘制玩家和球
        self.player1.draw()
        self.player2.draw()
        self.ball.draw()
        
        # 显示分数
        score1_text = self.font.render(str(self.player1.score), True, BLUE)
        score2_text = self.font.render(str(self.player2.score), True, RED)
        window.blit(score1_text, (WINDOW_WIDTH//4, 20))
        window.blit(score2_text, (3*WINDOW_WIDTH//4, 20))
        
        # 显示游戏结束信息
        if self.game_over:
            winner = "蓝方" if self.player1.score > self.player2.score else "红方"
            game_over_text = self.font.render(f'{winner}获胜! 按R键重新开始', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            window.blit(game_over_text, text_rect)
        
        # 显示暂停信息
        elif self.paused:
            pause_text = self.font.render('游戏暂停', True, WHITE)
            text_rect = pause_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            window.blit(pause_text, text_rect)
        
        pygame.display.flip()
    
    def run(self):
        """运行游戏主循环"""
        clock = pygame.time.Clock()
        
        while True:
            self.handle_input()
            self.update()
            self.draw()
            clock.tick(60)