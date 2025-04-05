import os
import json
import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='your password',   # 此处填写你的 mysql 密码
)


def get_json_path():
    '''获取json文件的路径'''
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "douban_movies.json")

try:
    with connection.cursor() as cursor:
        # 创建数据库
        cursor.execute("CREATE DATABASE IF NOT EXISTS douban_movies_top250")

        cursor.execute("USE douban_movies_top250")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies(
            id INT AUTO_INCREMENT PRIMARY KEY,
            no INT NOT NULL,
            name VARCHAR(255) NOT NULL,
            rating DECIMAL(3,1) NOT NULL,
            rating_count INT NOT NULL,
            year INT NOT NULL,
            country VARCHAR(255),
            language VARCHAR(255),
            runtime VARCHAR(100),
            IMDb VARCHAR(20),
            intro TEXT,
            directors TEXT,
            scriptwriters TEXT,
            stars TEXT,
            genres TEXT,
            screening_dates TEXT,
            other_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments(
            id INT AUTO_INCREMENT PRIMARY KEY,
            movie_id INT NOT NULL,
            author VARCHAR(100),
            time DATETIME,
            content TEXT,
            rating VARCHAR(10),
            useful INT,
            FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        """)


        # 读取JSON数据
        with open(get_json_path(), 'r', encoding='utf-8') as f:
            movies_data = json.load(f)

        # 插入数据
        for movie in movies_data:
            no = int(movie['no'])
            rating = float(movie['rating'])
            rating_count = int(movie['rating_count'])
            year = int(movie['year'])
            directors = ','.join(movie['directors'])
            scriptwriters = ','.join(movie['scriptwriters'])
            stars = ','.join(movie['stars'])
            genres = ','.join(movie['genres'])
            screening_dates = ','.join(movie['screening_dates'])
            other_name = ','.join(movie['other_name'])

            cursor.execute(
                "INSERT INTO movies (no, name, rating, rating_count, year, country, language, runtime, IMDb, intro, directors, scriptwriters, stars, genres, screening_dates, other_name)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (no, movie['name'], rating, rating_count, year, movie['country'], movie['language'], movie['runtime'], movie['IMDb'], movie['intro'], directors, scriptwriters, stars, genres, screening_dates, other_name)
            )

            for comment in movie['short_comments']:
                useful = int(comment['useful'])
                cursor.execute(
                    "INSERT INTO comments (movie_id, author, time, content, rating, useful)" 
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (no, comment['author'], comment['time'], comment['content'], comment['rating'], useful)
                )
        connection.commit()

except Exception as e:
    print(f'出错了: {e}')
    connection.rollback()
finally:
    connection.close()