import copy
import random
from utils import *

class AI2048:
    """
    2048游戏的AI类定义 使用贪婪搜索策略
    """
    def __init__(self, game=None):
        # 继承一下当前的game就完事了
        # AI是接盘侠
        self.game = game
    
    def get_move(self) -> int:
        """
        使用有限深度的贪婪搜索确定最佳移动
        """
        if not self.game:
            return None
        
        # 搜索深度 - 可以根据性能需求调整
        depth = 3   # 设置到 4 我电脑崩了
        
        best_move, _ = self._look_ahead(self.game, depth)   # 最佳选择
        
        if best_move is None:
            best_move = random.randint(0, 3)    # 没有就摆烂！
        
        return best_move
    
    def _look_ahead(self, game, depth):
        """
        递归搜索未来几步的最佳移动
        """
        if depth == 0:
            return None, self._evaluate(game)
        
        best_score = -float('inf')
        best_move = None
        
        # 尝试四个方向
        for direction in range(4):
            game_copy = copy.deepcopy(game)
            if game_copy.move(direction):
                # 第一层直接使用当前评估
                if depth == 1:
                    move_score = self._evaluate(game_copy)
                else:
                    # 模拟随机添加一个新方块
                    empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) 
                                  if game_copy.grid[i][j] == 0]
                    if empty_cells:
                        # 考虑2和4这两种可能的新方块
                        scores = []
                        for value in [2, 4]:
                            for cell in empty_cells[:min(3, len(empty_cells))]:  # 限制随机位置样本数量提高效率
                                game_sim = copy.deepcopy(game_copy)
                                game_sim.grid[cell[0]][cell[1]] = value
                                _, score = self._look_ahead(game_sim, depth - 1)
                                scores.append(score)
                        
                        # 取平均值作为期望分数
                        move_score = sum(scores) / len(scores) if scores else 0
                    else:
                        move_score = self._evaluate(game_copy)
                
                if move_score > best_score:
                    best_score = move_score
                    best_move = direction
        
        return best_move, best_score

    def _evaluate(self, game):
        """
        贪婪策略评估函数
        综合考虑多种高级策略因素，动态调整权重
        """
        grid = game.get_grid()
        score = game.get_score()
        max_tile = max(max(row) for row in grid)
        empty_cells = sum(row.count(0) for row in grid)
        
        # 基础分数 - 增加权重
        total_score = score * 1.5
        
        # 空格数量权重
        empty_weight = 20
        if max_tile >= 512:
            empty_weight = 35  # 后期空格更重要
        elif max_tile >= 256:
            empty_weight = 25
        
        total_score += empty_cells * empty_weight
        
        # 合并潜力
        merge_potential = 0
        
        # 水平方向合并潜力
        for i in range(4):
            for j in range(3):
                if grid[i][j] != 0:
                    # 直接相邻相同
                    if grid[i][j] == grid[i][j+1]:
                        merge_potential += grid[i][j] * 2
        
        # 垂直方向合并潜力
        for j in range(4):
            for i in range(3):
                if grid[i][j] != 0:
                    # 直接相邻相同
                    if grid[i][j] == grid[i+1][j]:
                        merge_potential += grid[i][j] * 2
        
        total_score += merge_potential * 1.2
        
        # 多模板蛇形布局评分
        # 定义多种潜在的最优路径模板
        snake_paths = [
            # 经典Z字形蛇形路径
            [
                (0, 0), (0, 1), (0, 2), (0, 3),
                (1, 3), (1, 2), (1, 1), (1, 0),
                (2, 0), (2, 1), (2, 2), (2, 3),
                (3, 3), (3, 2), (3, 1), (3, 0)
            ],
            # 反向Z字形路径
            [
                (0, 3), (0, 2), (0, 1), (0, 0),
                (1, 0), (1, 1), (1, 2), (1, 3),
                (2, 3), (2, 2), (2, 1), (2, 0),
                (3, 0), (3, 1), (3, 2), (3, 3)
            ],
            # 螺旋形路径
            [
                (0, 0), (0, 1), (0, 2), (0, 3),
                (1, 3), (2, 3), (3, 3), (3, 2),
                (3, 1), (3, 0), (2, 0), (1, 0),
                (1, 1), (1, 2), (2, 2), (2, 1)
            ]
        ]
        
        # 计算每个路径的得分，选择最好的那个
        best_snake_score = 0
        for path in snake_paths:
            values = [grid[r][c] for r, c in path]
            path_score = 0
            
            # 计算单调递减得分
            monotonic = True
            for i in range(len(values) - 1):
                if values[i] != 0:
                    if values[i] >= values[i + 1]:
                        # 递减或相等
                        path_score += 2
                        # 额外奖励递减
                        if values[i] > values[i + 1]:
                            if values[i + 1] != 0:
                                path_score += 2
                            else:  # 递减到0也给奖励
                                path_score += 1
                    else:
                        # 不是递减，严重惩罚
                        path_score -= 4
                        monotonic = False
            
            # 如果保持全局单调性，给予额外奖励
            if monotonic and values[0] > 0:
                path_score *= 1.5
            
            # 检查最大值是否在路径起点
            if values[0] == max_tile:
                path_score *= 1.3
            
            best_snake_score = max(best_snake_score, path_score)
        
        # 动态调整蛇形路径权重
        snake_weight = 12
        if max_tile >= 512:
            snake_weight = 18  # 后期单调性更重要
        
        total_score += best_snake_score * snake_weight
        
        # 角落策略评分
        corner_score = 0
        corners = [(0, 0), (0, 3), (3, 0), (3, 3)]
        corner_values = [grid[i][j] for i, j in corners]
        
        # 最大值在角落加分
        if max_tile in corner_values:
            corner_idx = corner_values.index(max_tile)
            corner_pos = corners[corner_idx]
            corner_score += max_tile * 3  # 增加角落权重
            
            # 在最大值周围构建递减序列
            if corner_pos == (0, 0):  # 左上角
                # 检查右侧和下方的数值梯度
                if grid[0][1] != 0 and grid[0][0] >= grid[0][1]:
                    corner_score += grid[0][1] * 0.8
                if grid[1][0] != 0 and grid[0][0] >= grid[1][0]:
                    corner_score += grid[1][0] * 0.8
            elif corner_pos == (0, 3):  # 右上角
                if grid[0][2] != 0 and grid[0][3] >= grid[0][2]:
                    corner_score += grid[0][2] * 0.8
                if grid[1][3] != 0 and grid[0][3] >= grid[1][3]:
                    corner_score += grid[1][3] * 0.8
            elif corner_pos == (3, 0):  # 左下角
                if grid[2][0] != 0 and grid[3][0] >= grid[2][0]:
                    corner_score += grid[2][0] * 0.8
                if grid[3][1] != 0 and grid[3][0] >= grid[3][1]:
                    corner_score += grid[3][1] * 0.8
            elif corner_pos == (3, 3):  # 右下角
                if grid[2][3] != 0 and grid[3][3] >= grid[2][3]:
                    corner_score += grid[2][3] * 0.8
                if grid[3][2] != 0 and grid[3][3] >= grid[3][2]:
                    corner_score += grid[3][2] * 0.8
        
        # 检查次大数在边缘
        second_max = 0
        for i in range(4):
            for j in range(4):
                if grid[i][j] < max_tile and grid[i][j] > second_max:
                    second_max = grid[i][j]
        
        # 边缘大值策略
        edge_positions = [(0, 1), (0, 2), (1, 0), (1, 3), (2, 0), (2, 3), (3, 1), (3, 2)]
        for i, j in edge_positions:
            if grid[i][j] == second_max:
                corner_score += second_max * 0.5
        
        total_score += corner_score
        
        # 平滑度和梯度评分
        smoothness = 0
        gradient = 0
        
        for i in range(4):
            for j in range(4):
                if grid[i][j] != 0:
                    # 计算平滑度 - 相邻格子差值越小越好
                    if j < 3 and grid[i][j+1] != 0:
                        diff = abs(grid[i][j] - grid[i][j+1])
                        smoothness -= diff
                        
                        # 奖励单调递减梯度
                        if grid[i][j] > grid[i][j+1]:
                            gradient += min(4, grid[i][j] / max(1, grid[i][j+1]))
                    
                    if i < 3 and grid[i+1][j] != 0:
                        diff = abs(grid[i][j] - grid[i+1][j])
                        smoothness -= diff
                        
                        # 奖励单调递减梯度
                        if grid[i][j] > grid[i+1][j]:
                            gradient += min(4, grid[i][j] / max(1, grid[i+1][j]))
        
        # 动态调整平滑度权重
        smoothness_weight = 1.5
        if max_tile >= 512:
            smoothness_weight = 2.5  # 后期平滑度更重要
        
        total_score += smoothness * smoothness_weight
        total_score += gradient * 8  # 梯度奖励
        
        # 危险格局惩罚
        danger_score = 0
        
        # 检测危险的填充模式 (例如: 高低高低交替，难以合并)
        for i in range(4):
            alternating = 0
            for j in range(3):
                if grid[i][j] != 0 and grid[i][j+1] != 0:
                    if (grid[i][j] > 2*grid[i][j+1] or grid[i][j+1] > 2*grid[i][j]):
                        alternating += 1
            danger_score -= alternating * 50
        
        for j in range(4):
            alternating = 0
            for i in range(3):
                if grid[i][j] != 0 and grid[i+1][j] != 0:
                    if (grid[i][j] > 2*grid[i+1][j] or grid[i+1][j] > 2*grid[i][j]):
                        alternating += 1
            danger_score -= alternating * 50
        
        # 惩罚大数在中央的情形
        center_positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
        for i, j in center_positions:
            if grid[i][j] >= max_tile / 2:
                danger_score -= grid[i][j] * 0.5
        
        total_score += danger_score
        
        # 空白格分布评分
        # 奖励空格集中分布，而不是散布各处
        if empty_cells > 0:
            empty_clusters = 0
            for i in range(4):
                for j in range(4):
                    if grid[i][j] == 0:
                        # 检查周围的空格
                        neighbors = 0
                        if i > 0 and grid[i-1][j] == 0: neighbors += 1
                        if i < 3 and grid[i+1][j] == 0: neighbors += 1
                        if j > 0 and grid[i][j-1] == 0: neighbors += 1
                        if j < 3 and grid[i][j+1] == 0: neighbors += 1
                        empty_clusters += neighbors
            
            # 空格聚集度评分
            total_score += (empty_clusters / max(1, empty_cells)) * 30
        
        # 游戏状态加成
        game_state = game.get_game_state()
        if game_state == 1:  # 游戏胜利
            total_score += 10000000000  # 成功了疯狂奖励
        elif game_state == 2:  # 游戏失败
            total_score -= 10000000000  # 失败了疯狂惩罚
        
        return total_score