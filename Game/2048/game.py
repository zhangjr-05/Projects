import os
import sys
import random
import pygame
from utils import *
from renderer import GameRenderer

def get_records_path():
    """获取records.txt文件的相对路径"""
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建records.txt文件的路径
    records_path = os.path.join(current_dir, "records.txt")
    return records_path

def load_highscores():
    """读取历史最高分"""
    try:
        records_path = get_records_path()
        if os.path.exists(records_path):
            with open(records_path, "r") as f:
                scores = [int(line.strip()) for line in f if line.strip().isdigit()]
                return scores if scores else [0]
        return [0]  # 如果文件不存在或为空，返回默认值
    except Exception as e:
        print(f"读取分数记录时出错: {e}")
        return [0]  # 出错时返回默认值
    
def save_score(score):
    """保存新的分数记录"""
    if score == 0:
        return
    try:
        scores = load_highscores()
        scores.append(score)
        scores.sort(reverse=True)
        
        records_path = get_records_path()
        with open(records_path, "w") as f:
            for s in scores:
                f.write(f"{s}\n")
    except Exception as e:
        print(f"保存分数记录时出错: {e}")

class Game2048:
    def __init__(self):
        '''初始化游戏'''
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.game_state = GAME_RUNNING
        self.high_score = max(load_highscores())
        self.new_record = False
        self.record_already_shown = False

        # 添加两个初始方块
        self.add_new_tile()
        self.add_new_tile()
    
    
    def add_new_tile(self) -> bool:
        '''在随机空白位置添加一个新的方块(2或4)'''
        # 找出所有空白格子
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == 0]

        if empty_cells: # 如果有空白格子
            # 随机选择一个空白格子
            i, j = random.choice(empty_cells)
            # 生成2或4
            self.grid[i][j] = 2 if random.random() < RANDOM_P_TWO else 4
            return True
        return False
    
    def get_grid(self):
        '''返回当前网格'''
        return self.grid
    
    def get_score(self):
        '''返回当前分数'''
        return self.score
    
    def get_game_state(self):
        '''返回当前游戏状态'''
        return self.game_state
    
    def move(self, direction: int) -> bool:
        """根据方向移动方块
        Args:
            direction (int): 方向: 0 = 上, 1 = 右, 2 = 下, 3 = 左
        Returns:
            bool: 网格是否有变化的bool值
        """
        # 备份当前网格
        memo_grid = [row[:] for row in self.grid]

        # 根据方向执行对应移动
        if direction == 0:
            self._move_up()
        elif direction == 1:
            self._move_right()
        elif direction == 2:
            self._move_down()
        elif direction == 3:
            self._move_left()
        
        # 检查网格是否发生变化
        changed = self.grid != memo_grid

        # 如果有变化，添加新方块并检查游戏状态
        if changed:
            self.add_new_tile()
            self._check_game_state()
        
        return changed
    
    def _move_left(self):
        '''向左移动方块'''
        for i in range(GRID_SIZE):
            # 移动并合并一行
            self._move_row_left(i)

    def _move_right(self):
        '''向右移动方块'''
        for i in range(GRID_SIZE):
            # 反转行，向左移动，再反转回来
            self.grid[i].reverse()
            self._move_row_left(i)
            self.grid[i].reverse()

    def _move_up(self):
        '''向上移动方块'''
        # 转置网格
        self.grid = [list(row) for row in zip(*self.grid)]
        # 向左移动每一行
        for i in range(GRID_SIZE):
            self._move_row_left(i)
        # 再次转置回原始方向
        self.grid = [list(row) for row in zip(*self.grid)]

    def _move_down(self):
        '''向下移动方块'''
        # 转置网格
        self.grid = [list(row) for row in zip(*self.grid)]
        # 向右移动每一行
        for i in range(GRID_SIZE):
            self.grid[i].reverse()
            self._move_row_left(i)
            self.grid[i].reverse()
        # 再次转置回原始方向
        self.grid = [list(row) for row in zip(*self.grid)]
    
    def _move_row_left(self, row_index: int):
        """
        将指定行向左移动并合并
        这是所有移动的基础操作
        Args:
            row_index (int): 移动行的下标
        """
        # 获取当前行并过滤掉0
        row = [tile for tile in self.grid[row_index] if tile != 0]

        # 合并相同的相邻方块
        i = 0
        while i < len(row) - 1:
            if row[i] == row[i + 1]:
                row[i] *= 2
                self.score += row[i]  # 增加分数
                row.pop(i + 1)  # 移除被合并的方块
            i += 1
        
        # 恢复长度
        while len(row) < GRID_SIZE:
            row.append(0)
        
        # 更新网格的行
        self.grid[row_index] = row
    
    def _check_game_state(self):
        '''检查游戏是否结束或者胜利'''

        # 检查是否破纪录
        if self.score > self.high_score and not self.record_already_shown:
            self.high_score = self.score
            self.new_record = True
            self.record_already_shown = True
        elif self.score > self.high_score:
            self.high_score = self.score

        # 检查是否有2048方块
        for row in self.grid:
            if 2048 in row:
                self.game_state = GAME_WON
                return
        
        # 检查是否还有空格
        for row in self.grid:
            if 0 in row:
                return  # 还有空格，游戏继续
            
        # 没有空格了，检查是否有可合并的方块
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE - 1):
                if self.grid[i][j] == self.grid[i][j + 1]:
                    return  # 游戏继续
                
        for i in range(GRID_SIZE - 1):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == self.grid[i + 1][j]:
                    return  # 游戏继续
        
        # 既没有空格也没有可合并的方块，凉了
        self.game_state = GAME_LOST


def run():
        # 初始化pygame
        pygame.init()

        # 创建游戏和渲染器实例
        game = Game2048()
        renderer = GameRenderer()

        # 设置游戏时钟
        clock = pygame.time.Clock()

        # 游戏主循环
        running = True
        while running:

            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if game.get_game_state() == GAME_RUNNING:
                        if event.key == pygame.K_UP:
                            game.move(0)
                        elif event.key == pygame.K_RIGHT:
                            game.move(1)
                        elif event.key == pygame.K_DOWN:
                            game.move(2)
                        elif event.key == pygame.K_LEFT:
                            game.move(3)

                    if event.key == pygame.K_r:  # 按R重开
                        # 保存当前分数
                        save_score(game.get_score())
                        game = Game2048()

            # 渲染
            renderer.render(game)

            # 控制帧率
            clock.tick(30)
        
        # 保存记录并退出游戏
        save_score(game.get_score())
        pygame.quit()
        sys.exit()