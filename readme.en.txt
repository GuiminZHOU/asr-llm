A simple ASR-LLM implementation based on pyaudio + funasr + ollama

[Installation Process]
1. Execute setup.sh
>chmod 755 setup.sh
>./setup.sh

2. Install python virtual environment
>python -m venv ./venv

3. Install requirements.txt, using Aliyun mirror for acceleration
>./venv/bin/python -m pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

4.【optional】if you want to use aliyun-nls, install NLS locally
>git clone https://github.com/aliyun/alibabacloud-nls-python-sdk.git
>cd alibabacloud-nls-python-sdk
>{project_path}/venv/bin/python -m pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
>{project_path}/venv/bin/python -m pip install .

[Execution Process]
1.【optional】if you want to use aliyun-nls, add aliyun configuration to .env
# Access key application portal: https://help.aliyun.com/zh/isi/getting-started/start-here
# NLS app key application portal: https://nls-portal.console.aliyun.com/applist

2. Start Ollama
#By default, the deepseek-r1:7b model is used. If you need to use another model, you can adjust the OLLAMA_MODEL variable in .env and run the corresponding model with Ollama.
>ollama run deepseek-r1:7b

3. Execute main.py
>./venv/bin/python main.py

[tips]
1. funasr: https://github.com/modelscope/FunASR
2. when using funasr for the first time, the model will be downloaded. You can execute the main method in the fun_asr.py file (a wav file needs to be provided).
3. the path to the funasr model folder is generally /Users/xxx/.cache/modelscope/hub/iic/SenseVoiceSmall. You need to assign this path to the FUNASR_MODEL_DIR variable in the .env file.
4. If you want to use aliyun-nls, switch the recognize method used in the recognize_audio method of the pyaudio_main.py file to asr.py. You need to install the nls-sdk and configure the aliyun ak/sk.
