import pygame
from utils import * 
from game import *

class GameRenderer:
    def __init__(self):
        '''初始化'''
        # 初始化字体
        pygame.font.init()

        # 设置主题
        self.theme = THEMES[CURRENT_THEME]

        # 创建游戏窗口
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("2048 Game")

        # 设置字体
        self.font = pygame.font.SysFont('Arial', 30, bold=True)
        self.big_font = pygame.font.SysFont('Arial', 40, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 20)

        # 破纪录？
        self.record_time = 0
        self.show_record = False

    def render(self, game):
        '''渲染游戏'''

        # 清空屏幕
        self.screen.fill(BACKGROUND_COLOR)

        # 绘制网格和方块
        self._draw_grid(game.get_grid())

        # 绘制分数
        self._draw_score(game.get_score(), game.high_score)

        # 检查是否破纪录并显示通知
        if game.new_record and not self.show_record:
            self.show_record = True
            self.record_time = pygame.time.get_ticks()  # 记录当前时间
            game.new_record = False  # 重置标志
        
        # 如果正在显示破纪录通知且未超过1秒
        current_time = pygame.time.get_ticks()
        if self.show_record and current_time - self.record_time < 1000:
            self._draw_new_record()
        elif self.show_record:
            self.show_record = False  # 超过1秒后停止显示

        # 绘制游戏状态
        game_state = game.get_game_state()
        if game_state != 0: # 游戏不在运行状态
            self._draw_game_state(game_state)
        
        # 刷新
        pygame.display.flip()

    def _draw_grid(self, grid: list[list[int]]):
        '''绘制游戏网格和方块'''

        self.screen.fill(self.theme["background"])

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                # 计算格子位置
                x = j * CELL_SIZE + (j + 1) * PADDING
                y = i * CELL_SIZE + (i + 1) * PADDING

                # 获取格子值
                value = grid[i][j]

                # 设置格子颜色
                color = self.theme["tile_colors"].get(value, (0, 0, 0))

                # 绘制格子
                pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE), 0, 5)

                # 如果格子有值，绘制文字
                if value != 0:
                    text_color = self.theme["text_dark"] if value >= 8 else self.theme["text_light"]

                    # 为不同大小的数字选择合适的字体
                    if value < 100:
                        text_surface = self.font.render(str(value), True, text_color)
                    elif value < 1000:
                        text_surface = self.small_font.render(str(value), True, text_color)
                    else:
                        smallest_font = pygame.font.SysFont('Arial', 18)
                        text_surface = smallest_font.render(str(value), True, text_color)

                    # 计算文字位置 (居中)
                    text_rect = text_surface.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))

                    # 绘制文字
                    self.screen.blit(text_surface, text_rect)
    
    def _draw_score(self, score):
        '''绘制分数'''
        score_text = self.font.render(f"Score: {score}", True, (119, 110, 101))
        self.screen.blit(score_text, (10, WINDOW_HEIGHT - 40))

    def _draw_game_state(self, state):
        '''绘制游戏状态消息'''
        # 创建半透明覆盖层
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 150))  # 半透明白色
        self.screen.blit(overlay, (0, 0))

        # 确定要显示的消息
        if state == GAME_WON:
            message = "You Win!"
        else:  # GAME_LOST
            message = "Game Over!"
        
        # 渲染消息
        text_surface = self.big_font.render(message, True, (119, 110, 101))
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
        self.screen.blit(text_surface, text_rect)
        
        # 提示按R键重新开始
        restart_text = self.small_font.render("Press 'R' to Restart", True, (119, 110, 101))
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        self.screen.blit(restart_text, restart_rect)

    def _draw_score(self, score, high_score):
        """绘制分数和最高分"""
        score_text = self.font.render(f"Score: {score}", True, (119, 110, 101))
        self.screen.blit(score_text, (10, 10))
        
        high_score_text = self.font.render(f"Best: {high_score}", True, (119, 110, 101))
        self.screen.blit(high_score_text, (WINDOW_WIDTH - high_score_text.get_width() - 10, 10))

    def _draw_new_record(self):
        """显示破纪录通知"""
        overlay = pygame.Surface((WINDOW_WIDTH, 50), pygame.SRCALPHA)
        overlay.fill((237, 194, 46, 200))  # 黄色半透明背景
        self.screen.blit(overlay, (0, WINDOW_HEIGHT // 2 - 25))
        
        record_text = self.big_font.render("NEW RECORD!", True, (249, 246, 242))
        text_rect = record_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(record_text, text_rect)
    
    