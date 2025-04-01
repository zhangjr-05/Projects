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

# 定义颜色
BACKGROUND_COLOR = (187, 173, 160)  # 背景色
EMPTY_CELL_COLOR = (204, 192, 179)  # 空格子颜色

# 方块颜色映射
TILE_COLORS = {
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
    2048: (237, 194, 46)
}

# 文字颜色映射
TEXT_COLORS = {
    0: (204, 192, 179),
    2: (119, 110, 101),
    4: (119, 110, 101),
    8: (249, 246, 242),
    16: (249, 246, 242),
    32: (249, 246, 242),
    64: (249, 246, 242),
    128: (249, 246, 242),
    256: (249, 246, 242),
    512: (249, 246, 242),
    1024: (249, 246, 242),
    2048: (249, 246, 242)
}


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
            4096: (60, 58, 50),
            8192: (54, 52, 45)
        }
    },
    "dark": {
        "name": "暗黑",
        "background": (40, 44, 52),
        "empty_cell": (60, 64, 72),
        "text_light": (180, 185, 190),
        "text_dark": (255, 255, 255),
        "overlay": (0, 0, 0, 150),
        "tile_colors": {
            0: (60, 64, 72),
            2: (75, 80, 90),
            4: (85, 90, 100),
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
        "background": (10, 10, 30),
        "empty_cell": (20, 20, 40),
        "text_light": (180, 180, 220),
        "text_dark": (255, 255, 255),
        "overlay": (0, 0, 100, 150),
        "tile_colors": {
            0: (20, 20, 40),
            2: (40, 20, 80),
            4: (60, 20, 110),
            8: (80, 20, 140),
            16: (100, 20, 170),
            32: (120, 20, 200),
            64: (140, 20, 230),
            128: (20, 100, 230),
            256: (20, 140, 200),
            512: (20, 180, 170),
            1024: (20, 210, 140),
            2048: (20, 240, 110),
            4096: (60, 255, 80),
            8192: (120, 255, 40)
        },
        "glow": True  # 特殊效果：发光
    },
    "pastel": {
        "name": "粉彩",
        "background": (245, 240, 225),
        "empty_cell": (235, 225, 210),
        "text_light": (130, 120, 110),
        "text_dark": (75, 65, 55),
        "overlay": (255, 255, 255, 120),
        "tile_colors": {
            0: (235, 225, 210),
            2: (240, 230, 220),
            4: (245, 235, 200),
            8: (250, 220, 190),
            16: (255, 200, 180),
            32: (255, 180, 170),
            64: (255, 160, 150),
            128: (210, 225, 180),
            256: (190, 235, 170),
            512: (170, 245, 160),
            1024: (150, 255, 170),
            2048: (130, 255, 180),
            4096: (120, 235, 190),
            8192: (110, 215, 200)
        },
        "rounded": 10  # 特殊效果：更圆润的方块
    },
    "ocean": {
        "name": "海洋",
        "background": (20, 60, 80),
        "empty_cell": (30, 70, 90),
        "text_light": (150, 200, 220),
        "text_dark": (230, 245, 255),
        "overlay": (0, 50, 80, 150),
        "tile_colors": {
            0: (30, 70, 90),
            2: (40, 90, 110),
            4: (50, 110, 130),
            8: (60, 130, 160),
            16: (70, 150, 180),
            32: (80, 170, 200),
            64: (90, 190, 220),
            128: (100, 160, 210),
            256: (110, 140, 200),
            512: (120, 120, 190),
            1024: (130, 100, 180),
            2048: (140, 80, 170),
            4096: (150, 60, 160),
            8192: (160, 40, 150)
        },
        "gradient": True  # 特殊效果：渐变色
    },
    "forest": {
        "name": "森林",
        "background": (40, 70, 45),
        "empty_cell": (50, 80, 55),
        "text_light": (180, 210, 190),
        "text_dark": (235, 250, 240),
        "overlay": (30, 60, 35, 150),
        "tile_colors": {
            0: (50, 80, 55),
            2: (60, 100, 65),
            4: (70, 120, 75),
            8: (80, 140, 70),
            16: (90, 160, 65),
            32: (100, 180, 60),
            64: (110, 200, 55),
            128: (140, 180, 60),
            256: (160, 170, 65),
            512: (180, 160, 70),
            1024: (200, 150, 75),
            2048: (220, 140, 80),
            4096: (235, 130, 85),
            8192: (250, 120, 90)
        },
        "texture": True  # 特殊效果：纹理
    },
    "candy": {
        "name": "糖果",
        "background": (255, 230, 240),
        "empty_cell": (245, 220, 230),
        "text_light": (150, 100, 120),
        "text_dark": (90, 60, 70),
        "overlay": (255, 200, 220, 150),
        "tile_colors": {
            0: (245, 220, 230),
            2: (255, 215, 225),
            4: (255, 200, 220),
            8: (255, 180, 210),
            16: (255, 160, 200),
            32: (255, 140, 190),
            64: (255, 120, 180),
            128: (250, 170, 210),
            256: (240, 140, 210),
            512: (230, 110, 210),
            1024: (220, 80, 210),
            2048: (210, 50, 210),
            4096: (200, 40, 200),
            8192: (190, 30, 190)
        },
        "animation": "bounce"  # 特殊效果：弹跳动画
    },
    "retro": {
        "name": "复古",
        "background": (60, 60, 60),
        "empty_cell": (80, 80, 80),
        "text_light": (200, 200, 200),
        "text_dark": (255, 255, 255),
        "overlay": (30, 30, 30, 180),
        "tile_colors": {
            0: (80, 80, 80),
            2: (0, 240, 0),
            4: (0, 200, 0),
            8: (0, 180, 0),
            16: (240, 240, 0),
            32: (200, 200, 0),
            64: (180, 180, 0),
            128: (240, 120, 0),
            256: (200, 100, 0),
            512: (180, 80, 0),
            1024: (240, 0, 0),
            2048: (200, 0, 0),
            4096: (160, 0, 0),
            8192: (120, 0, 0)
        },
        "pixelated": True  # 特殊效果：像素化
    }
}

# 当前主题
CURRENT_THEME = "ocean"