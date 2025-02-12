基于pyaudio + funasr + ollama实现的简单版asr-llm

【安装过程】
1. 执行setup.sh
chmod 755 setup.sh
./setup.sh

2. 安装虚拟环境
python -m venv ./venv

3. 安装requirements.txt，使用aliyun镜像加速
./venv/bin/python -m pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

4. 【可选】如果要使用aliyun-nls实现asr，需要本地安装nls
git clone https://github.com/aliyun/alibabacloud-nls-python-sdk.git
cd alibabacloud-nls-python-sdk
{项目路径}/venv/bin/python -m pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
{项目路径}/venv/bin/python -m pip install .

【执行过程】
1.【可选】如果要使用aliyun-nls实现asr，.env添加aliyun配置
access key申请传送门：https://help.aliyun.com/zh/isi/getting-started/start-here
nls app key申请传送门：https://nls-portal.console.aliyun.com/applist

2. 启动ollama + pull模型
# 默认使用deepseek-r1:7b模型，如需使用其他模型，可以调整.env中OLLAMA_MODEL变量，并ollama运行对应的模型即可，默认使用deepseek-r1:7b
ollama run deepseek-r1:7b

3.【命令行启动】执行main.py
./venv/bin/python main.py

4.【界面启动】执行web.py
# 使用gradio构建的交互页面，full developed with cursor:)
# 下拉菜单中展示的模型列表，是当前ollama list的所有模型
# 首次识别，需要加载funasr模型，需要等一会~
./venv/bin/python web.py

【注意事项】
1. funasr传送门：https://github.com/modelscope/FunASR
2. 首次使用funasr时会下载模型，可以先执行fun_asr.py文件中main方法即可(需提供一个wav文件)
3. funasr模型文件夹路径一般为/Users/xxx/.cache/modelscope/hub/iic/SenseVoiceSmall，需要将该路径赋值到.env中的FUNASR_MODEL_DIR变量
4. 如果想使用aliyun-nls，将pyaudio_main.py文件recognize_audio方法中使用的recognize方法切换为asr.py即可，需安装nls-sdk以及配置aliyun ak/sk