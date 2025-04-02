# 定义游戏常量
GRID_SIZE = 4  # 游戏网格大小 4x4
CELL_SIZE = 100  # 每个格子的像素大小
PADDING = 10  # 格子间距
WINDOW_WIDTH = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * PADDING
WINDOW_HEIGHT = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * PADDING + 50  # 额外的50像素用于显示分数

# 游戏状态
GAME_RUNNING = 0
GAME_WON = 1
GAME_LOST = 2

# 随机生成2的概率
RANDOM_P_TWO = 0.8

# AI移动延迟 (ms)
AI_DELAY = 100

# 主题定义
THEMES = {
    "classic": {
        "name": "经典",
        "background": (187, 173, 160),
        "empty_cell": (204, 192, 179),
        "text_light": (119, 110, 101),
        "text_dark": (249, 246, 242),
        "overlay": (255, 255, 255, 150),
        "tile_colors": {
            0: (204, 192, 179),
            2: (238, 228, 218),
            4: (237, 224, 200),
            8: (242, 177, 121),
            16: (245, 149, 99),
            32: (246, 124, 95),
            64: (246, 94, 59),
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46),
            4096: (237, 190, 30),
            8192: (237, 185, 15)
        }
    },
    "dark": {
        "name": "暗黑",
        "background": (30, 32, 38),
        "empty_cell": (50, 53, 60),
        "text_light": (190, 195, 200),
        "text_dark": (255, 255, 255),
        "overlay": (0, 0, 0, 150),
        "tile_colors": {
            0: (50, 53, 60),
            2: (70, 73, 80),
            4: (85, 88, 95),
            8: (100, 90, 140),
            16: (120, 80, 170),
            32: (140, 70, 190),
            64: (160, 60, 210),
            128: (90, 140, 220),
            256: (70, 160, 200),
            512: (50, 180, 180),
            1024: (45, 190, 160),
            2048: (40, 200, 140),
            4096: (35, 210, 120),
            8192: (30, 220, 100)
        }
    },
    "neon": {
        "name": "霓虹",
        "background": (5, 5, 20),
        "empty_cell": (15, 15, 35),
        "text_light": (200, 200, 240),
        "text_dark": (255, 255, 255),
        "overlay": (0, 0, 100, 150),
        "tile_colors": {
            0: (15, 15, 35),
            2: (40, 20, 80),
            4: (60, 20, 120),
            8: (255, 50, 120),  # 粉红霓虹
            16: (255, 100, 50),  # 橙色霓虹
            32: (255, 220, 50),  # 黄色霓虹
            64: (50, 255, 120),  # 绿色霓虹
            128: (50, 200, 255),  # 蓝色霓虹
            256: (150, 50, 255),  # 紫色霓虹
            512: (255, 100, 200),  # 粉红霓虹
            1024: (100, 255, 200),  # 青色霓虹
            2048: (255, 255, 100),  # 黄色霓虹
            4096: (60, 255, 80),
            8192: (120, 255, 40)
        },
        "glow": True
    },
    "ocean": {
        "name": "海洋",
        "background": (10, 45, 70),
        "empty_cell": (20, 60, 85),
        "text_light": (150, 210, 230),
        "text_dark": (230, 250, 255),
        "overlay": (0, 50, 80, 150),
        "tile_colors": {
            0: (20, 60, 85),
            2: (40, 90, 120),
            4: (50, 110, 140),
            8: (60, 140, 170),
            16: (70, 160, 190),
            32: (80, 180, 210),
            64: (90, 200, 230),
            128: (100, 170, 220),
            256: (75, 145, 210),
            512: (50, 120, 200),
            1024: (25, 95, 190),
            2048: (10, 70, 180),
            4096: (5, 50, 170),
            8192: (0, 30, 160)
        },
        "gradient": True
    },
    "forest": {
        "name": "森林",
        "background": (30, 60, 35),
        "empty_cell": (40, 70, 45),
        "text_light": (190, 220, 200),
        "text_dark": (235, 250, 240),
        "overlay": (30, 60, 35, 150),
        "tile_colors": {
            0: (40, 70, 45),
            2: (60, 100, 65),
            4: (80, 120, 75),
            8: (100, 140, 70),  # 浅草绿
            16: (120, 160, 60),  # 黄绿
            32: (140, 180, 50),  # 青橄榄
            64: (110, 130, 50),  # 深橄榄
            128: (90, 110, 50),  # 苔藓
            256: (70, 90, 40),   # 深林绿
            512: (120, 100, 60),  # 树皮棕
            1024: (140, 110, 70), # 浅木色
            2048: (160, 120, 80),  # 木纹色
            4096: (90, 70, 40),   # 深木色
            8192: (70, 50, 30)    # 古木色
        },
        "texture": True
    },
    "candy": {
        "name": "糖果",
        "background": (255, 240, 245),
        "empty_cell": (250, 235, 240),
        "text_light": (150, 100, 120),
        "text_dark": (90, 60, 70),
        "overlay": (255, 220, 230, 150),
        "tile_colors": {
            0: (250, 235, 240),
            2: (255, 200, 220),  # 粉红色
            4: (255, 180, 210),  # 桃红色
            8: (255, 230, 150),  # 淡黄色
            16: (180, 230, 255),  # 淡蓝色
            32: (200, 255, 200),  # 薄荷绿
            64: (255, 190, 170),  # 淡橙色
            128: (220, 170, 255), # 淡紫色
            256: (255, 150, 180), # 草莓色
            512: (150, 220, 255), # 蓝莓色
            1024: (255, 220, 120), # 香草色
            2048: (200, 255, 160), # 青苹果色
            4096: (255, 160, 140), # 水蜜桃色
            8192: (190, 180, 255)  # 蓝紫糖
        },
        "animation": "bounce"
    },
}

# 当前主题
CURRENT_THEME = "candy"

# 背景和空格子颜色直接使用主题中的定义
BACKGROUND_COLOR = THEMES[CURRENT_THEME]["background"]
EMPTY_CELL_COLOR = THEMES[CURRENT_THEME]["empty_cell"]

# 根据当前主题生成方块颜色映射
TILE_COLORS = THEMES[CURRENT_THEME]["tile_colors"]

# 生成文字颜色映射
TEXT_COLORS = {}
for value in TILE_COLORS.keys():
    # 对于较小的数值使用深色文字，较大数值使用浅色文字
    if value <= 4:
        TEXT_COLORS[value] = THEMES[CURRENT_THEME]["text_light"]
    else:
        TEXT_COLORS[value] = THEMES[CURRENT_THEME]["text_dark"]


# 获取历史记录
import os
import json

def get_records_path():
    """获取records.json文件的路径"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "records.json")

def load_highscores():
    """读取历史最高分"""
    try:
        records_path = get_records_path()
        if os.path.exists(records_path):
            with open(records_path, "r") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, dict) and "scores" in data and isinstance(data["scores"], list):
                        return sorted(data["scores"], reverse=True)
                except json.JSONDecodeError:
                    pass
        return [0]
    except Exception as e:
        print(f"读取分数记录时出错: {e}")
        return [0]
    
def save_score(score):
    """保存新的分数记录"""
    if score <= 0:
        return
        
    try:
        scores = load_highscores()
        if score not in scores:  # 避免重复分数
            scores.append(score)
        
        scores = sorted(scores, reverse=True)[:10]  # 只保留前10个最高分
        
        records_path = get_records_path()
        with open(records_path, "w") as f:
            json.dump({"scores": scores}, f)
    except Exception as e:
        print(f"保存分数记录时出错: {e}")
