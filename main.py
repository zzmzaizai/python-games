import pygame
import sys
import math  # 添加math模块导入
import importlib


# 初始化 Pygame
pygame.init()
pygame.joystick.init()  # 初始化手柄支持

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# 游戏窗口设置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((int(WINDOW_WIDTH), int(WINDOW_HEIGHT)))
pygame.display.set_caption('小游戏集合')

# 延迟加载游戏类
def load_game_class(game_name):
    """动态加载游戏类
    
    根据游戏名称动态导入对应的游戏模块，并返回其Game类。
    这种延迟加载的方式可以提高程序启动速度，减少内存占用。
    
    参数:
        game_name: 游戏模块名称
        
    返回:
        Game类对象，如果加载失败则返回None
    """
    try:
        # 动态导入模块
        module = importlib.import_module(game_name.lower())
        # 获取模块中的Game类
        return getattr(module, 'Game')
    except ImportError:
        print(f'无法加载游戏模块: {game_name}')
        return None

from games.breakout import Game as BreakoutGame
from games.snake import Game as SnakeGame
from games.pacman import Game as PacmanGame



class Menu:
    """游戏菜单类
    
    管理游戏菜单界面，包括游戏选择、切换和说明显示等功能
    
    属性:
        font: pygame字体对象，用于渲染文本
        games: 游戏列表，包含每个游戏的名称、类和说明
        selected: 当前选中的游戏索引
        transition_alpha: 切换动画的透明度值
        show_instructions: 是否显示游戏说明
    """
    def __init__(self):
        """初始化菜单
        
        创建字体对象，设置游戏列表和初始状态
        """
        """初始化菜单
        
        创建字体对象，设置游戏列表和初始状态
        """
        self.font = pygame.font.SysFont('SimHei', 48)  # 使用系统黑体字体
        # 初始化手柄
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for joystick in self.joysticks:
            joystick.init()
        
        self.games = []
        self.selected = 0
        self.transition_alpha = 0
        self.show_instructions = False
        self.show_tutorial = False
        self.tutorial_page = 0
        self.scroll_offset = 0  # 添加滚动偏移量
        self.visible_items = 5  # 一次显示的游戏数量
        self.item_height = 70  # 每个游戏选项的高度
        self.scroll_speed = 20  # 滚动速度
        self.target_scroll = 0  # 目标滚动位置
        self.scroll_smoothness = 0.2  # 滚动平滑度
        
        # 添加新手引导按钮
        button_width = 200
        button_height = 50
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        self.tutorial_button = pygame.Rect(button_x, WINDOW_HEIGHT - 100, button_width, button_height)
        
        # 初始化游戏列表
        self.init_games()
    
    def init_games(self):
        """初始化游戏列表"""
        self.games = [
            {
                'name': '打砖块',
                'module': 'breakout',
                'class': None,
                'instructions': '使用方向键或手柄左右移动挡板，反弹球击碎砖块。按ESC/手柄Start键暂停，R键/手柄A键重新开始。',
                'tutorial': [
                    '欢迎来到打砖块游戏！',
                    '使用←→方向键或手柄左摇杆控制挡板左右移动',
                    '反弹小球击碎上方的砖块',
                    '不同颜色的砖块有不同的分值',
                    '注意不要让球落到底部',
                    '按ESC/手柄Start键暂停游戏，按R键/手柄A键重新开始'
                ]
            },
            {
                'name': '贪吃蛇',
                'module': 'snake',
                'class': None,  # 延迟加载
                'instructions': '使用方向键或手柄控制蛇的移动方向，吃到食物长大。按ESC/手柄Start键暂停，R键/手柄A键重新开始。',
                'tutorial': [
                    '欢迎来到贪吃蛇游戏！',
                    '使用↑↓←→方向键或手柄左摇杆/方向键控制蛇的移动',
                    '吃到红色食物可以让蛇变长',
                    '注意不要撞到自己的身体',
                    '按ESC/手柄Start键暂停游戏，按R键/手柄A键重新开始'
                ]
            },
            {
                'name': '吃糖豆',
                'module': 'pacman',
                'class': None,  # 延迟加载
                'instructions': '使用方向键或手柄控制角色移动，吃掉糖豆，躲避敌人。按ESC/手柄Start键暂停，R键/手柄A键重新开始。',
                'tutorial': [
                    '欢迎来到吃糖豆游戏！',
                    '使用↑↓←→方向键或手柄左摇杆/方向键控制角色移动',
                    '收集白色糖豆来得分',
                    '躲避彩色的敌人',
                    '按ESC/手柄Start键暂停游戏，按R键/手柄A键重新开始'
                ]
            },
            {
                'name': '俄罗斯方块',
                'module': 'tetris',
                'class': None,  # 延迟加载
                'instructions': '使用方向键或手柄控制方块移动和旋转，空格键/B键快速下落。按ESC/手柄Start键暂停，R键/手柄A键重新开始。',
                'tutorial': [
                    '欢迎来到俄罗斯方块！',
                    '使用←→方向键或手柄左摇杆/方向键控制方块左右移动',
                    '使用↑键或手柄A键旋转方块',
                    '使用↓键加速下落，空格键或手柄B键直接到底',
                    '消除完整的行来得分',
                    '按ESC/手柄Start键暂停游戏，按R键/手柄A键重新开始'
                ]
            },
            {
                'name': '弹球',
                'module': 'pong',
                'class': None,  # 延迟加载
                'instructions': '双人对战，左侧玩家使用W/S键，右侧玩家使用上下方向键，或使用两个手柄控制。按ESC/手柄Start键暂停，R键/手柄A键重新开始。',
                'tutorial': [
                    '欢迎来到弹球游戏！',
                    '左侧玩家使用W/S键或第一个手柄控制蓝色挡板',
                    '右侧玩家使用↑↓键或第二个手柄控制红色挡板',
                    '击球时根据击中位置改变反弹角度',
                    '先得到5分的玩家获胜',
                    '按ESC/手柄Start键暂停游戏，按R键/手柄A键重新开始'
                ]
            },
            {
                'name': '五子棋',
                'module': 'gomoku',
                'class': None,  # 延迟加载
                'instructions': '双人对战，使用鼠标点击落子，黑白双方轮流下棋。按ESC/手柄Start键暂停，R键/手柄A键重新开始。',
                'tutorial': [
                    '欢迎来到五子棋游戏！',
                    '黑白双方轮流下棋',
                    '使用鼠标点击棋盘落子',
                    '先连成五子的一方获胜',
                    '按ESC/手柄Start键暂停游戏，按R键/手柄A键重新开始'
                ]
            },
            {
                'name': '2048',
                'module': 'game2048',
                'class': None,  # 延迟加载
                'instructions': '使用方向键或手柄控制方块移动和合并，相同数字的方块会合并并翻倍。按ESC/手柄Start键暂停，R键/手柄A键重新开始。',
                'tutorial': [
                    '欢迎来到2048游戏！',
                    '使用↑↓←→方向键或手柄左摇杆/方向键控制方块移动',
                    '相同数字的方块相撞会合并并翻倍',
                    '尽可能获得更高的分数',
                    '当无法移动时游戏结束',
                    '按ESC/手柄Start键暂停游戏，按R键/手柄A键重新开始'
                ]
            },
            {
                'name': '退出',
                'module': None,
                'class': None,
                'instructions': '',
                'tutorial': []
            }
        ]
        self.selected = 0
        self.transition_alpha = 0
        self.show_instructions = False
        self.show_tutorial = False
        self.tutorial_page = 0
        
        # 添加新手引导按钮
        button_width = 200
        button_height = 50
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        self.tutorial_button = pygame.Rect(button_x, WINDOW_HEIGHT - 100, button_width, button_height)

    def draw(self):
        """绘制菜单界面
        
        绘制标题、游戏列表和游戏说明（如果启用）
        """
        # 简化背景绘制
        window.fill(BLACK)
        
        # 绘制标题
        title = self.font.render('小游戏集合', True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        window.blit(title, title_rect)
        
        # 平滑滚动动画
        self.scroll_offset += (self.target_scroll - self.scroll_offset) * self.scroll_smoothness
        
        # 计算可见游戏的范围
        start_idx = max(0, self.selected - self.visible_items // 2)
        end_idx = min(len(self.games), start_idx + self.visible_items)
        
        # 调整起始索引确保显示足够的项目
        if end_idx - start_idx < self.visible_items and len(self.games) > self.visible_items:
            if start_idx == 0:
                end_idx = self.visible_items
            else:
                start_idx = len(self.games) - self.visible_items
        
        # 绘制游戏列表
        list_center_y = WINDOW_HEIGHT // 2
        for i in range(start_idx, end_idx):
            # 计算每个选项的位置
            offset = (i - self.selected) * self.item_height
            y_pos = list_center_y + offset - self.scroll_offset
            
            # 根据距离中心的远近设置缩放和透明度
            distance = abs(y_pos - list_center_y)
            scale = 1 - (distance / (WINDOW_HEIGHT / 2)) * 0.3  # 最多缩小到70%
            alpha = 255 - (distance / (WINDOW_HEIGHT / 2)) * 155  # 最低透明度100
            
            # 绘制游戏选项
            color = RED if i == self.selected else WHITE
            text = self.font.render(self.games[i]['name'], True, color)
            # 缩放文本
            scaled_size = (int(text.get_width() * scale), int(text.get_height() * scale))
            if scaled_size[0] > 0 and scaled_size[1] > 0:  # 确保尺寸大于0
                scaled_text = pygame.transform.smoothscale(text, scaled_size)
                # 设置透明度
                scaled_text.set_alpha(alpha)
                text_rect = scaled_text.get_rect(center=(WINDOW_WIDTH // 2, y_pos))
                window.blit(scaled_text, text_rect)
        
        # 显示游戏说明
        if self.show_instructions and self.games[self.selected]['instructions']:
            instructions_font = pygame.font.SysFont('SimHei', 24)
            instructions = instructions_font.render(
                self.games[self.selected]['instructions'],
                True, WHITE
            )
            instructions_rect = instructions.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)
            )
            window.blit(instructions, instructions_rect)
        
        # 绘制新手引导按钮和界面（保持不变）
        if not self.show_tutorial:
            pygame.draw.rect(window, BLUE, self.tutorial_button)
            tutorial_text = self.font.render('新手引导', True, WHITE)
            tutorial_text_rect = tutorial_text.get_rect(center=self.tutorial_button.center)
            window.blit(tutorial_text, tutorial_text_rect)
        
        if self.show_tutorial and self.games[self.selected]['tutorial']:
            self.draw_tutorial()
        
        pygame.display.flip()
    
    def draw_tutorial(self):
        """绘制新手引导界面"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        window.blit(overlay, (0, 0))

        tutorial_font = pygame.font.SysFont('SimHei', 36)
        current_tutorial = self.games[self.selected]['tutorial'][self.tutorial_page]
        tutorial_text = tutorial_font.render(current_tutorial, True, WHITE)
        tutorial_rect = tutorial_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        window.blit(tutorial_text, tutorial_rect)

        total_pages = len(self.games[self.selected]['tutorial'])
        page_text = tutorial_font.render(f'{self.tutorial_page + 1}/{total_pages}', True, WHITE)
        page_rect = page_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        window.blit(page_text, page_rect)

        nav_font = pygame.font.SysFont('SimHei', 24)
        nav_text = nav_font.render('使用←→切换页面，按ESC关闭引导', True, WHITE)
        nav_rect = nav_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
        window.blit(nav_text, nav_rect)

        pygame.display.flip()

    def run(self):
        """运行菜单主循环
        
        处理用户输入，更新菜单状态，实现游戏切换
        """
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self.show_tutorial:
                        if event.key == pygame.K_ESCAPE:
                            self.show_tutorial = False
                        elif event.key == pygame.K_LEFT:
                            self.tutorial_page = max(0, self.tutorial_page - 1)
                        elif event.key == pygame.K_RIGHT:
                            max_page = len(self.games[self.selected]['tutorial']) - 1
                            self.tutorial_page = min(max_page, self.tutorial_page + 1)
                    else:
                        if event.key == pygame.K_UP:
                            self.selected = (self.selected - 1) % len(self.games)
                            # 更新目标滚动位置
                            self.target_scroll = (self.selected - self.visible_items // 2) * self.item_height
                        elif event.key == pygame.K_DOWN:
                            self.selected = (self.selected + 1) % len(self.games)
                            # 更新目标滚动位置
                            self.target_scroll = (self.selected - self.visible_items // 2) * self.item_height
                        elif event.key == pygame.K_RETURN:
                            self.handle_game_selection()
                        elif event.key == pygame.K_i:
                            self.show_instructions = not self.show_instructions
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if not self.show_tutorial:
                        # 检查新手引导按钮点击
                        if self.tutorial_button.collidepoint(mouse_pos):
                            self.show_tutorial = True
                            self.tutorial_page = 0
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 4:  # 鼠标滚轮向上
                        if self.selected > 0:
                            self.selected -= 1
                            self.target_scroll = (self.selected - self.visible_items // 2) * self.item_height
                    elif event.button == 5:  # 鼠标滚轮向下
                        if self.selected < len(self.games) - 1:
                            self.selected += 1
                            self.target_scroll = (self.selected - self.visible_items // 2) * self.item_height
                # 处理手柄按钮事件
                elif event.type == pygame.JOYBUTTONDOWN:
                    if self.show_tutorial:
                        if event.button == 7:  # Start键
                            self.show_tutorial = False
                        elif event.button == 2:  # X键
                            self.tutorial_page = max(0, self.tutorial_page - 1)
                        elif event.button == 1:  # B键
                            max_page = len(self.games[self.selected]['tutorial']) - 1
                            self.tutorial_page = min(max_page, self.tutorial_page + 1)
                    else:
                        if event.button == 0:  # A键
                            self.handle_game_selection()
                        elif event.button == 7:  # Start键
                            self.show_instructions = not self.show_instructions

            # 处理手柄摇杆和方向键输入（移到事件循环外部）
            if self.joysticks and not self.show_tutorial:
                try:
                    joystick = self.joysticks[0]  # 使用第一个手柄
                    # 处理左摇杆
                    axis_y = joystick.get_axis(1)  # 垂直轴
                    if axis_y < -0.5:  # 上
                        self.selected = (self.selected - 1) % len(self.games)
                        self.target_scroll = (self.selected - self.visible_items // 2) * self.item_height
                    elif axis_y > 0.5:  # 下
                        self.selected = (self.selected + 1) % len(self.games)
                        self.target_scroll = (self.selected - self.visible_items // 2) * self.item_height
                    # 处理方向键
                    hat = joystick.get_hat(0)
                    if hat[1] == 1:  # 上
                        self.selected = (self.selected - 1) % len(self.games)
                        self.target_scroll = (self.selected - self.visible_items // 2) * self.item_height
                    elif hat[1] == -1:  # 下
                        self.selected = (self.selected + 1) % len(self.games)
                        self.target_scroll = (self.selected - self.visible_items // 2) * self.item_height
                except pygame.error:
                    pass  # 忽略手柄错误

            self.draw()
            clock.tick(60)

    def handle_game_selection(self):
        """处理游戏选择
        
        当玩家选择一个游戏时，处理游戏的启动和切换
        """
        if self.selected == len(self.games) - 1:  # 退出选项
            pygame.quit()
            sys.exit()
        else:
            # 显示简单的加载提示
            loading_font = pygame.font.SysFont('SimHei', 36)
            loading_text = loading_font.render('正在加载游戏...', True, WHITE)
            loading_rect = loading_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            
            # 显示加载界面
            window.fill(BLACK)
            window.blit(loading_text, loading_rect)
            pygame.display.flip()
            
            # 延迟加载游戏类
            if self.games[self.selected]['class'] is None:
                self.games[self.selected]['class'] = load_game_class(self.games[self.selected]['module'])
            
            # 启动选中的游戏
            game = self.games[self.selected]['class']()
            game.run()

            # 游戏结束后重新设置窗口和标题
            window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            pygame.display.set_caption('小游戏集合')

            # 播放返回动画
            for alpha in range(255, 0, -25):
                self.transition_alpha = alpha
                self.draw()
                pygame.time.delay(5)

if __name__ == '__main__':
    menu = Menu()
    menu.run()