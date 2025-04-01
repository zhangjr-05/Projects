from game import run

# 主函数就是要简洁明了
def main():
    '''主程序入口'''
    print("欢迎来到2048游戏!")
    print("1. 人类模式")
    print("2. AI贪婪搜索模式")
    print("请选择游戏模式 (1/2):", end=" ")
    choice = input().strip()
    if choice == "2":
        print("AI模式启动!")
        run(ai_mode=True)
    else:
        print("人类模式启动!")
        run(ai_mode=False)

if __name__ == "__main__":
    main()