from dotenv import load_dotenv
from app.command import command
load_dotenv()

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    command()
