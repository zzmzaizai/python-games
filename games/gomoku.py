import pygame
import sys

# 初始化 Pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)  # 棋盘颜色

# 游戏窗口设置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BOARD_SIZE = 15  # 15x15的棋盘
GRID_SIZE = 30  # 每个格子的大小
PIECE_RADIUS = 13  # 棋子半径

class Game:
    """五子棋游戏类
    
    控制游戏的主要逻辑，包括初始化、更新和渲染
    
    属性:
        window: pygame显示窗口
        board: 棋盘状态数组
        current_player: 当前玩家（1为黑棋，2为白棋）
        game_over: 游戏是否结束
        winner: 获胜者
        paused: 游戏是否暂停
        show_pause_menu: 是否显示暂停菜单
    """
    def __init__(self):
        """初始化游戏
        
        创建游戏窗口，初始化游戏状态
        """
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('五子棋')
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = 1  # 1为黑棋，2为白棋
        self.game_over = False
        self.winner = None
        self.paused = False
        self.show_pause_menu = False
        self.font = pygame.font.SysFont('SimHei', 36)
        
        # 初始化音效
        pygame.mixer.init()
        self.place_sound = pygame.mixer.Sound('resources/place.wav')
        self.win_sound = pygame.mixer.Sound('resources/win.wav')
        
        # 胜利动画相关属性
        self.win_animation_alpha = 0
        self.win_animation_direction = 1
        self.win_animation_speed = 5
        self.win_pieces = []
        
        # 计算棋盘的起始位置（居中显示）
        self.board_start_x = (WINDOW_WIDTH - (BOARD_SIZE - 1) * GRID_SIZE) // 2
        self.board_start_y = (WINDOW_HEIGHT - (BOARD_SIZE - 1) * GRID_SIZE) // 2
        
        # 初始化暂停菜单按钮
        button_width = 200
        button_height = 50
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        self.continue_button = pygame.Rect(button_x, WINDOW_HEIGHT // 2 - 60, button_width, button_height)
        self.menu_button = pygame.Rect(button_x, WINDOW_HEIGHT // 2 + 10, button_width, button_height)
        
        # 添加手柄控制相关的属性
        self.cursor_pos = [BOARD_SIZE // 2, BOARD_SIZE // 2]  # 光标位置
        self.cursor_visible = False  # 光标是否可见
        self.cursor_blink_timer = 0  # 光标闪烁计时器

    def get_grid_position(self, mouse_pos):
        """获取鼠标点击的棋盘格子位置
        
        参数:
            mouse_pos: 鼠标位置坐标
            
        返回:
            tuple: 棋盘格子的(行,列)坐标，如果点击位置无效则返回None
        """
        x, y = mouse_pos
        # 计算相对于棋盘起始位置的偏移
        board_x = x - self.board_start_x
        board_y = y - self.board_start_y
        
        # 检查是否在棋盘范围内
        if 0 <= board_x <= (BOARD_SIZE - 1) * GRID_SIZE and \
           0 <= board_y <= (BOARD_SIZE - 1) * GRID_SIZE:
            # 计算最近的格子交点
            col = round(board_x / GRID_SIZE)
            row = round(board_y / GRID_SIZE)
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                return row, col
        return None
    
    def check_win(self, row, col):
        """检查是否有玩家获胜
        
        检查指定位置的棋子是否形成五子连珠
        
        参数:
            row: 行坐标
            col: 列坐标
            
        返回:
            bool: True表示有玩家获胜，False表示游戏继续
        """
        directions = [(1,0), (0,1), (1,1), (1,-1)]  # 四个方向：横、竖、正斜、反斜
        player = self.board[row][col]
        
        for dx, dy in directions:
            count = 1  # 当前方向的连续棋子数
            win_pieces = [(row, col)]  # 记录获胜的棋子位置
            
            # 正向检查
            for i in range(1, 5):
                new_row = row + dx * i
                new_col = col + dy * i
                if not (0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE):
                    break
                if self.board[new_row][new_col] != player:
                    break
                count += 1
                win_pieces.append((new_row, new_col))
            
            # 反向检查
            for i in range(1, 5):
                new_row = row - dx * i
                new_col = col - dy * i
                if not (0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE):
                    break
                if self.board[new_row][new_col] != player:
                    break
                count += 1
                win_pieces.append((new_row, new_col))
            
            if count >= 5:
                self.win_pieces = win_pieces  # 保存获胜棋子的位置
                return True
        return False

    def draw(self):
        """绘制游戏画面
        
        绘制棋盘、游戏状态信息和暂停菜单
        """
        self.window.fill(GRAY)
        self.draw_board()
        
        # 显示当前玩家
        player_text = self.font.render(
            '当前: ' + ('黑棋' if self.current_player == 1 else '白棋'),
            True, BLACK if self.current_player == 1 else WHITE
        )
        self.window.blit(player_text, (10, 10))
        
        # 显示游戏结束信息和胜利动画
        if self.game_over:
            # 更新胜利动画
            self.win_animation_alpha += self.win_animation_direction * self.win_animation_speed
            if self.win_animation_alpha >= 255:
                self.win_animation_alpha = 255
                self.win_animation_direction = -1
            elif self.win_animation_alpha <= 0:
                self.win_animation_alpha = 0
                self.win_animation_direction = 1
            
            # 绘制获胜棋子的动画效果
            for row, col in self.win_pieces:
                center = (self.board_start_x + col * GRID_SIZE,
                         self.board_start_y + row * GRID_SIZE)
                glow_surface = pygame.Surface((PIECE_RADIUS * 3, PIECE_RADIUS * 3), pygame.SRCALPHA)
                glow_color = (*RED, self.win_animation_alpha)
                pygame.draw.circle(glow_surface, glow_color,
                                 (PIECE_RADIUS * 1.5, PIECE_RADIUS * 1.5),
                                 PIECE_RADIUS * 1.5)
                glow_rect = glow_surface.get_rect(center=center)
                self.window.blit(glow_surface, glow_rect)
            
            winner_text = self.font.render(
                f'游戏结束! {"黑棋" if self.winner == 1 else "白棋"}获胜',
                True, BLACK if self.winner == 1 else WHITE
            )
            text_rect = winner_text.get_rect(
                center=(WINDOW_WIDTH // 2, 30)
            )
            self.window.blit(winner_text, text_rect)
        
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
        
        处理鼠标点击、键盘按键和手柄输入
        
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
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.paused and not self.game_over:
                pos = self.get_grid_position(event.pos)
                if pos:
                    row, col = pos
                    if self.board[row][col] == 0:  # 如果该位置为空
                        self.board[row][col] = self.current_player
                        self.place_sound.play()  # 播放落子音效
                        if self.check_win(row, col):
                            self.game_over = True
                            self.winner = self.current_player
                            self.win_sound.play()  # 播放胜利音效
                        else:
                            self.current_player = 3 - self.current_player  # 切换玩家
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
                    elif event.button == 0:  # A键
                        if self.game_over:
                            self.__init__()
                        elif not self.paused:
                            # 在光标位置落子
                            row, col = self.cursor_pos
                            if self.board[row][col] == 0:
                                self.board[row][col] = self.current_player
                                self.place_sound.play()  # 播放落子音效
                                if self.check_win(row, col):
                                    self.game_over = True
                                    self.winner = self.current_player
                                    self.win_sound.play()  # 播放胜利音效
                                else:
                                    self.current_player = 3 - self.current_player
        
        # 处理手柄摇杆和方向键输入
        if not self.game_over and not self.paused:
            for joystick in pygame.joystick.get_count() and [pygame.joystick.Joystick(0)]:
                # 处理左摇杆
                axis_x = joystick.get_axis(0)  # 水平轴
                axis_y = joystick.get_axis(1)  # 垂直轴
                if abs(axis_x) > 0.5 or abs(axis_y) > 0.5:
                    self.cursor_visible = True
                    if abs(axis_x) > abs(axis_y):
                        if axis_x < -0.5 and self.cursor_pos[1] > 0:
                            self.cursor_pos[1] -= 1
                        elif axis_x > 0.5 and self.cursor_pos[1] < BOARD_SIZE - 1:
                            self.cursor_pos[1] += 1
                    else:
                        if axis_y < -0.5 and self.cursor_pos[0] > 0:
                            self.cursor_pos[0] -= 1
                        elif axis_y > 0.5 and self.cursor_pos[0] < BOARD_SIZE - 1:
                            self.cursor_pos[0] += 1
                
                # 处理方向键
                hat = joystick.get_hat(0)
                if hat[0] != 0 or hat[1] != 0:
                    self.cursor_visible = True
                    if hat[0] < 0 and self.cursor_pos[1] > 0:
                        self.cursor_pos[1] -= 1
                    elif hat[0] > 0 and self.cursor_pos[1] < BOARD_SIZE - 1:
                        self.cursor_pos[1] += 1
                    elif hat[1] > 0 and self.cursor_pos[0] > 0:
                        self.cursor_pos[0] -= 1
                    elif hat[1] < 0 and self.cursor_pos[0] < BOARD_SIZE - 1:
                        self.cursor_pos[0] += 1
        return False
    
    def run(self):
        """运行游戏主循环
        
        控制游戏的主要流程，包括处理输入和更新显示
        """
        clock = pygame.time.Clock()
        
        while True:
            if self.handle_input():  # 如果返回True，表示要返回主菜单
                break
            
            self.draw()
            clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()

