import gradio as gr
import os
import shutil
from datetime import datetime
from funasr import AutoModel
import requests
import re

# 创建保存音频文件的文件夹
if not os.path.exists("audio_files"):
    os.makedirs("audio_files")

model_dir = os.getenv("FUNASR_MODEL_DIR")
if model_dir == "":
    model_dir = "iic/SenseVoiceSmall"

def get_available_models():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = [model["name"] for model in response.json()["models"]]
            return models
        else:
            return []
    except Exception as e:
        print(f"获取模型列表失败: {str(e)}")
        return []

def chat_with_llm(model_name, prompt):
    try:
        response = requests.post("http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False
            })
        if response.status_code == 200:
            return response.json()['response']
        else:
            return f"请求失败: {response.status_code}"
    except Exception as e:
        return f"发生错误: {str(e)}"

def clean_asr_text(text):
    """清理 ASR 识别结果中的特殊标记"""
    # 移除所有 <|xxx|> 格式的标记
    cleaned_text = re.sub(r'<\|.*?\|>', '', text)
    # 移除多余的空格
    cleaned_text = ' '.join(cleaned_text.split())
    return cleaned_text

def process_and_chat(audio, model_name, history):
    if audio is None:
        gr.Info("没有检测到音频输入")
        return "", "", history

    # 检查模型是否可用
    if not model_name:
        error_msg = "请先选择一个对话模型"
        gr.Info(f"❌ {error_msg}")
        return error_msg, "", history

    try:
        # 保存音频文件
        audio_path = audio[1] if isinstance(audio, tuple) else audio
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"audio_files/recording_{timestamp}.wav"
        shutil.copy2(audio_path, filename)
        gr.Info(f"✅ 音频已保存: {filename}")
        print(f"[{datetime.now()}] 音频已保存: {filename}")
        
        # ASR 识别
        print(f"[{datetime.now()}] 开始 ASR 识别...")
        gr.Info("🎯 正在进行语音识别...")
        model = AutoModel(model=model_dir, disable_update=True)
        asr_result = model.generate(input=filename)
        recognized_text = clean_asr_text(asr_result[0]['text'])  # 清理识别结果
        print(f"[{datetime.now()}] ASR 识别完成: {recognized_text}")
        gr.Info("✅ 语音识别完成")
        
        # 调用大模型
        print(f"[{datetime.now()}] 开始调用大模型 {model_name}...")
        gr.Info(f"🤖 正在调用 {model_name} 模型...")
        llm_response = chat_with_llm(model_name, recognized_text)
        print(f"[{datetime.now()}] 大模型响应完成")
        gr.Info("✅ 大模型响应完成")
        
        # 添加到历史记录
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_history = f"{history}\n\n===== {timestamp} =====\n问：{recognized_text}\n答：{llm_response}"
        
        return recognized_text, llm_response, new_history
    except Exception as e:
        error_msg = f"处理失败：{str(e)}"
        print(f"[{datetime.now()}] 错误：{error_msg}")
        gr.Info(f"❌ {error_msg}")
        return error_msg, "", history

def clear_audio():
    return None  # 返回 None 会清空 Audio 组件的内容

# 创建 Gradio 界面
with gr.Blocks() as interface:
    gr.Markdown("## 语音对话系统", elem_classes="center-text")
    
    with gr.Row():
        model_selector = gr.Dropdown(
            choices=get_available_models(),
            value=get_available_models()[0],
            label="选择对话模型"
        )
    
    with gr.Row():
        audio_input = gr.Audio(
            sources=["microphone"],
            type="filepath",
            label="录音输入",
            interactive=True
        )
    
    with gr.Row():  
        start_btn = gr.Button("开始录音", elem_id="record-btn")
        send_btn = gr.Button("发送")

    with gr.Row():
        with gr.Column(scale=1):
            asr_output = gr.Textbox(label="当前语音识别结果")
            llm_output = gr.Textbox(label="当前回复", lines=3)
        with gr.Column(scale=1):
            chat_history = gr.Textbox(
                label="对话历史记录", 
                lines=10,
                value="",
                interactive=False
            )
    
    # 设置按钮点击事件
    start_btn.click(
        fn=clear_audio,  # 先清空录音
        inputs=None,
        outputs=audio_input,
    ).then(  # 然后触发录音按钮
        fn=lambda: None,
        inputs=None,
        outputs=None,
        js="() => {document.querySelector('button.record').click()}"
    )
    
    send_btn.click(
        fn=process_and_chat,
        inputs=[
            audio_input,
            model_selector,
            chat_history
        ],
        outputs=[
            asr_output,
            llm_output,
            chat_history
        ]
    )

interface.launch()
