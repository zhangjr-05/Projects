import os
import re
import time
import json
import random
import requests
from bs4 import BeautifulSoup

# 豆瓣 Top 250 的 URL
BASE_URL = "https://movie.douban.com/top250"

# 请求头，模拟浏览器访问
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Cookie": "bid=YOUR_BID_HERE; douban-fav-remind=1;",
    "Referer": "https://movie.douban.com/",
}

# 设定要爬取的电影部数
MOVIE_NUMS = 10

def get_json_path():
    '''获取json文件的路径'''
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "douban_movies.json")
json_path = get_json_path()


def get_movie_links():
    """
    获取豆瓣 Top 250 的电影详情页链接
    """
    movie_links = []
    for start in range(0, 250, 25):  # 每页 25 部电影，共 10 页
        url = f"{BASE_URL}?start={start}"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 提取电影详情页链接
        for tag in soup.select(".hd a"):
            movie_links.append(tag["href"])
        
        time.sleep(random.uniform(0.5, 1))  # 随机延时，降低被封风险
    return movie_links

def extract_movie_id(url):
    """
    从电影URL中提取电影ID
    """
    pattern = r"subject/(\d+)/"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_movie_comments(movie_id, comment_count=60):
    """
    获取指定数量的电影短评
    """
    comments = []
    start = 0
    limit = 20  # 豆瓣每页显示20条评论
    
    while len(comments) < comment_count:
        # 构建评论页URL
        comment_url = f"https://movie.douban.com/subject/{movie_id}/comments?start={start}&limit={limit}&sort=new_score&status=P"
        
        response = requests.get(comment_url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        
        comment_items = soup.find_all("div", class_="comment-item")
        
        if not comment_items:
            break  # 没有更多评论了
            
        for comment in comment_items:
            # 提取评论信息
            try:
                comment_info = {
                    "author": comment.find("span", class_="comment-info").a.text.strip(),
                    "time": comment.find("span", class_="comment-time").text.strip(),
                    "content": comment.find("span", class_="short").text.strip(),
                    "rating": "未评分"
                }
                
                # 提取评分
                rating_span = comment.find("span", class_=lambda x: x and x.startswith("allstar"))
                if rating_span:
                    rating_class = rating_span.get("class")[0]
                    rating_value = rating_class.replace("allstar", "")
                    comment_info["rating"] = f"{int(rating_value) // 10}星"
                
                # 提取点赞数
                votes_span = comment.find("span", class_="votes")
                comment_info["useful"] = votes_span.text.strip() if votes_span else "0"
                
                comments.append(comment_info)
            except Exception as e:
                print(f"解析评论时出错: {e}")
        
        # 更新起始位置，获取下一页评论
        start += limit
        
        # 已经获取足够数量的评论或者没有下一页了
        if len(comments) >= comment_count or not soup.find("a", class_="next"):
            break
            
        # 随机延时，降低被封风险
        time.sleep(random.uniform(0.5, 1))
    
    return comments[:comment_count]  # 返回指定数量的评论

def get_movie_details(movie_url):
    """
    获取单部电影的详细信息和短评
    """
    response = requests.get(movie_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 提取电影基本信息
    movie_info = {}
    movie_info["name"] = soup.find("span", property="v:itemreviewed").text.strip()
    movie_info["rating"] = soup.find("strong", class_="ll rating_num").text.strip()
    movie_info["rating_count"] = soup.find("span", property="v:votes").text.strip()
    movie_info["year"] = soup.find("span", class_="year").text.strip("()")
    
    # 提取导演
    try:
        movie_info["director"] = soup.find("a", rel="v:directedBy").text.strip()
    except AttributeError:
        movie_info["director"] = "未知"
    
    # 提取类型
    movie_info["genres"] = [genre.text.strip() for genre in soup.find_all("span", property="v:genre")]
    
    # 提取片长
    try:
        movie_info["duration"] = soup.find("span", property="v:runtime").text.strip()
    except AttributeError:
        movie_info["duration"] = "未知"
    
    # 提取简介
    try:
        movie_info["summary"] = soup.find("span", property="v:summary").text.strip()
    except AttributeError:
        summary_div = soup.find("div", class_="indent", id="link-report")
        if summary_div:
            movie_info["summary"] = summary_div.text.strip()
        else:
            movie_info["summary"] = "无简介"
    
    # 提取电影ID并获取短评
    movie_id = extract_movie_id(movie_url)
    movie_info["short_comments"] = get_movie_comments(movie_id, 60)  # 获取60条短评
    
    return movie_info

def save_to_json(data, filename):
    """
    保存数据到 JSON 文件
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    try:
        # 获取所有电影链接
        print("正在获取电影链接...")
        movie_links = get_movie_links()
        print(f"共获取到 {len(movie_links)} 部电影链接")
        
        # 爬取每部电影的详细信息
        all_movies = []
        for idx, movie_url in enumerate(movie_links[:MOVIE_NUMS]):  # 只爬取前 MOVIE_NUMS 部电影
            print(f"正在爬取第 {idx + 1} 部电影")
            movie_details = get_movie_details(movie_url)
            all_movies.append(movie_details)
            time.sleep(random.uniform(0.5, 1))  # 随机延时，降低被封风险
        
        # 保存到 JSON 文件
        save_to_json(all_movies, json_path)
        print("爬取顺利完成  数据已保存到 douban_movies.json 文件中")
    
    except Exception as e:
        print(f"程序执行过程中出错: {e}")
        # 保存已经爬取的数据
        if all_movies:
            save_to_json(all_movies, json_path)
            print("已保存部分爬取的数据到 douban_movies.json 文件中")

if __name__ == "__main__":
    main()