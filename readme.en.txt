A simple ASR-LLM implementation based on pyaudio + aliyun-nls + ollama

[Installation Process]
1. Execute setup.sh
>chmod 755 setup.sh
>./setup.sh

2. Install python virtual environment
>python -m venv ./venv

3. Install requirements.txt, using Aliyun mirror for acceleration
>./venv/bin/python -m pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

4. Install NLS locally
>git clone https://github.com/aliyun/alibabacloud-nls-python-sdk.git
>cd alibabacloud-nls-python-sdk
>{project_path}/venv/bin/python -m pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
>{project_path}/venv/bin/python -m pip install .

[Execution Process]
1. Add Aliyun configuration to .env
# Access key application portal: https://help.aliyun.com/zh/isi/getting-started/start-here
# NLS app key application portal: https://nls-portal.console.aliyun.com/applist

2. Start Ollama
#By default, the qwen2.5 model is used. If you need to use another model, you can adjust the OLLAMA_MODEL variable in .env and run the corresponding model with Ollama.
>ollama run qwen2.5

3. Execute main.py
>./venv/bin/python main.py
