基于pyaudio + aliyun-nls + ollama实现的简单版asr-llm

【安装过程】
1. 执行setup.sh
chmod 755 setup.sh
./setup.sh

2. 安装虚拟环境
python -m venv ./venv

3. 安装requirements.txt，使用aliyun镜像加速
./venv/bin/python -m pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

4. 本地安装nls
git clone https://github.com/aliyun/alibabacloud-nls-python-sdk.git
cd alibabacloud-nls-python-sdk
{项目路径}/venv/bin/python -m pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
{项目路径}/venv/bin/python -m pip install .

【执行过程】
1. .env添加aliyun配置
access key申请传送门：https://help.aliyun.com/zh/isi/getting-started/start-here
nls app key申请传送门：https://nls-portal.console.aliyun.com/applist

2. 启动ollama
# 默认使用qwen2模型，如需使用其他模型，可以调整llm.py中model变量，并ollama运行对应的模型即可
ollama run qwen2

3. 执行main.py
./venv/bin/python main.py
