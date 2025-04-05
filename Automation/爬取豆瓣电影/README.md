# 豆瓣电影爬虫

一个用于爬取豆瓣电影 Top 250 信息的 Python 脚本，可获取电影基本信息和短评。

## 功能特点

- 爬取豆瓣 Top 250 电影列表
- 获取电影详细信息（名称、评分、导演、类型、时长等）
- 收集每部电影的短评（默认60条）
- 将所有数据保存为结构化的 JSON 文件 或本地 mysql 数据库

## 环境要求

- Python 3.6+
- 依赖库：
    - requests
    - BeautifulSoup4
    - re
    - json
    - time
    - random
    - os
- 安装mysql

## 使用方法

1. 克隆或下载此项目到本地
2. 安装所需依赖库：
     ```
     pip install requests beautifulsoup4
     ```
3. 根据需要修改 `main.py` 中的配置：
     - `MOVIE_NUMS` - 要爬取的电影数量（默认为10部）
     - `HEADERS` - 请求头信息，可能需要更新 Cookie
4. 点击运行main.py文件或在命令行输入以下命令：
     ```
     python main.py
     ```
5. 爬取结果将保存在同目录下的 `douban_movies.json` 文件中
6. 运行 save_to_sql.py 将数据保存到本地 mysql 数据库

## 数据格式

脚本爬取的 JSON 数据包含以下字段：
- `name`: 电影名称
- `rating`: 评分
- `rating_count`: 评分人数
- `year`: 上映年份
- `director`: 导演
- `genres`: 类型（数组）
- `duration`: 片长
- `summary`: 简介
- `short_comments`: 短评列表（每条包含作者、时间、内容、评分和点赞数）

## 注意事项

- 爬虫设置了随机延时以降低被封禁的风险
- 请遵守豆瓣的使用条款，不要过于频繁地爬取数据
- 可能需要更新 Cookie 信息以确保脚本正常运行

## 免责声明

本项目仅供学习和研究网络爬虫技术使用，请勿用于商业目的或其他可能违反豆瓣服务条款的用途。使用本脚本产生的任何后果由使用者自行承担。

## Tips

有问题可与作者交流~~