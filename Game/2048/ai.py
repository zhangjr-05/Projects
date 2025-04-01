import copy
import random
from utils import GRID_SIZE, GAME_RUNNING

class AI2048:
    """
    2048游戏的AI 使用贪婪搜索策略
    """
    def __init__(self, game=None):
        self.game = game
    
    def get_next_move(self):
        """
        确定下一步移动的方向
        返回值: 0(上), 1(右), 2(下), 3(左)
        """
        if not self.game:
            return None
        
        # 尝试所有方向，选择得分最高的一个
        best_score = -1
        best_move = None
        
        # 对每个可能的移动方向进行评估
        for direction in range(4):
            # 创建游戏状态的深拷贝
            game_copy = copy.deepcopy(self.game)
            
            # 尝试移动
            if game_copy.move(direction):
                # 评估移动后的状态
                move_score = self._evaluate_board(game_copy)
                
                # 如果这个移动比当前最佳移动更好，则更新
                if move_score > best_score:
                    best_score = move_score
                    best_move = direction
        
        # 如果没有有效移动，随机选择一个方向
        if best_move is None:
            best_move = random.randint(0, 3)
        
        return best_move
    
    def _evaluate_board(self, game):
        """
        评估游戏状态的分数
        这是一个简单的贪婪评估函数
        """
        grid = game.get_grid()
        score = game.get_score()
        
        # 基础评分 = 当前得分
        total_score = score
        
        # 加分项1: 空格数量
        empty_cells = sum(row.count(0) for row in grid)
        total_score += empty_cells * 10
        
        # 加分项2: 大数值方块位于边角
        # 我们希望最大的数在角落
        max_tile = max(max(row) for row in grid)
        corner_values = [grid[0][0], grid[0][3], grid[3][0], grid[3][3]]
        if max_tile in corner_values:
            total_score += max_tile * 0.5
        
        # 加分项3: 相邻相似值的单调性
        monotonicity_score = 0
        
        # 行单调性
        for i in range(4):
            for j in range(3):
                if grid[i][j] != 0 and grid[i][j+1] != 0:
                    if grid[i][j] >= grid[i][j+1]:
                        monotonicity_score += 1
        
        # 列单调性
        for j in range(4):
            for i in range(3):
                if grid[i][j] != 0 and grid[i+1][j] != 0:
                    if grid[i][j] >= grid[i+1][j]:
                        monotonicity_score += 1
        
        total_score += monotonicity_score * 5
        
        return total_score
    
    
    def get_advanced_move(self):
        """
        使用进阶策略确定下一步移动
        """
        if not self.game:
            return None
        
        best_score = -float('inf')
        best_move = None
        
        for direction in range(4):
            game_copy = copy.deepcopy(self.game)
            if game_copy.move(direction):
                # 使用更高级的评估函数
                move_score = self._evaluate_advanced(game_copy)
                if move_score > best_score:
                    best_score = move_score
                    best_move = direction
        
        if best_move is None:
            best_move = random.randint(0, 3)
        
        return best_move

    def _evaluate_advanced(self, game):
        """
        更高级的评估函数
        综合考虑多种策略因素
        """
        grid = game.get_grid()
        score = game.get_score()
        
        # 基础分数
        total_score = score
        
        # 1. 空格数量权重
        empty_cells = sum(row.count(0) for row in grid)
        total_score += empty_cells * 20  # 空格非常重要
        
        # 2. 合并潜力 - 检查相邻相同数字
        merge_potential = 0
        for i in range(4):
            for j in range(3):
                if grid[i][j] != 0 and grid[i][j] == grid[i][j+1]:
                    merge_potential += grid[i][j]
        
        for j in range(4):
            for i in range(3):
                if grid[i][j] != 0 and grid[i][j] == grid[i+1][j]:
                    merge_potential += grid[i][j]
                    
        total_score += merge_potential
        
        # 3. 蛇形布局评分 (像蛇一样的数值递减序列)
        snake_score = 0
        # 从左上到右下的蛇形路径
        snake_path = [
            (0, 0), (0, 1), (0, 2), (0, 3),
            (1, 3), (1, 2), (1, 1), (1, 0),
            (2, 0), (2, 1), (2, 2), (2, 3),
            (3, 3), (3, 2), (3, 1), (3, 0)
        ]
        
        values = [grid[r][c] for r, c in snake_path]
        for i in range(len(values) - 1):
            if values[i] >= values[i+1] and values[i] != 0:
                snake_score += 1
                # 如果是递减序列，给予更高奖励
                if values[i] > values[i+1] and values[i+1] != 0:
                    snake_score += 1
        
        total_score += snake_score * 10
        
        # 4. 大数字在角落的奖励
        max_tile = max(max(row) for row in grid)
        corner_values = [grid[0][0], grid[0][3], grid[3][0], grid[3][3]]
        if max_tile in corner_values:
            total_score += max_tile * 2
        
        # 5. 平滑度 - 相邻格子的数值差异
        smoothness = 0
        for i in range(4):
            for j in range(4):
                if grid[i][j] != 0:
                    # 计算与右侧格子的差异
                    if j < 3 and grid[i][j+1] != 0:
                        smoothness -= abs(grid[i][j] - grid[i][j+1])
                    # 计算与下方格子的差异
                    if i < 3 and grid[i+1][j] != 0:
                        smoothness -= abs(grid[i][j] - grid[i+1][j])
        
        total_score += smoothness * 1.5
        
        return total_score