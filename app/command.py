import os
import time
import pyaudio
import wave
from app.pyaudio_main import play_audio, recognize_audio
from app.llm import chat

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
MAX_RECORD_SECONDS = 30
AUDIO_BASE_DIR = './audio'


commands = [
    {'c': 'record', 'desc': '录音'},
    {'c': 'play', 'desc': '播放'},
    {'c': 'recognize', 'desc': '识别'},
    {'c': 'chat', 'desc': '聊天'},
    {'c': 'exit', 'desc': '退出'},
]


def desc():
    print("输入以下指令进行交互")
    for i, comm in enumerate(commands):
        print(f"{i + 1}. {comm['c']} - {comm['desc']}")


def is_valid_command(comm: str):
    for c in commands:
        if c['c'] == comm:
            return True
    return False


def command():
    desc()
    while True:
        user_input = input('你的输入> ')
        if user_input == 'exit':
            print("bye~")
            break
        if not is_valid_command(user_input):
            print("输入指令错误，请重新输入！")
            desc()
        if user_input == 'record':
            print('按下【r】开始录音，按下【Ctrl + C】结束录音，输入【exit】退出，录音最长持续时间30s')
            try:
                while True:
                    key = input('>>> ')
                    if key.lower() == 'r':
                        print('正在录音...')
                        break
                    if key.lower() == 'exit':
                        print('bye~')
                        exit()
                    print('指令错误，按下【r】开始录音.')

                p = pyaudio.PyAudio()
                stream = p.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=RATE,
                                input=True,
                                frames_per_buffer=CHUNK)
                frames = []
                try:
                    for i in range(0, int(RATE / CHUNK * MAX_RECORD_SECONDS)):
                        data = stream.read(CHUNK)
                        frames.append(data)
                except KeyboardInterrupt:
                    print('已停止录音，正在生成录音文件...')

                stream.stop_stream()
                stream.close()
                p.terminate()

                current_timestamp = int(time.time() * 1e3)
                file_name = 'output' + '_' + str(current_timestamp) + '.wav'
                wf = wave.open(AUDIO_BASE_DIR + '/' + file_name, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
                wf.close()
                print('录音结束.')
            except Exception as e:
                print(f"录音过程中出现错误：{e}")
            desc()
        if user_input == 'play':
            # 列出目录中的所有文件和目录
            entries = os.listdir(AUDIO_BASE_DIR)
            print('请选择要播放的录音文件：')
            # 打印文件序号和文件名
            for index, entry in enumerate(entries, start=1):
                print(f"{index}. {entry}")
            while True:
                try:
                    play_input = input('请输入序号>>> ')
                    if play_input.lower() == 'exit':
                        print('bye~')
                        exit(0)

                    index_input = int(play_input)
                    i = index_input - 1
                    if i < 0 or i >= len(entries):
                        print('文件不存在！请重新输入指令！')
                        break
                    else:
                        print('开始播放：')
                        play_audio(entries[i])
                        print('播放完毕~')
                        break
                except ValueError:
                    print('输入错误，请重新输入')
            desc()
        if user_input == 'recognize':
            # 列出目录中的所有文件和目录
            entries = os.listdir(AUDIO_BASE_DIR)
            print('请选择要识别的录音文件：')
            # 打印文件序号和文件名
            for index, entry in enumerate(entries, start=1):
                print(f"{index}. {entry}")
            while True:
                try:
                    play_input = input('请输入序号>>> ')
                    if play_input.lower() == 'exit':
                        print('bye~')
                        exit(0)

                    index_input = int(play_input)
                    i = index_input - 1
                    if i < 0 or i >= len(entries):
                        print('文件不存在！请重新输入指令！')
                        break
                    else:
                        recognize_audio(entries[i])
                        break
                except ValueError:
                    print('输入错误，请重新输入')
            desc()
        if user_input == 'chat':
            print('按下【r】开始说话，按下【Ctrl + C】结束，输入【exit】退出，最长持续时间30s')
            try:
                while True:
                    key = input('>>> ')
                    if key.lower() == 'r':
                        print('正在录音...')
                        break
                    if key.lower() == 'exit':
                        print('bye~')
                        exit()
                    print('指令错误，按下【r】开始说话.')

                p = pyaudio.PyAudio()
                stream = p.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=RATE,
                                input=True,
                                frames_per_buffer=CHUNK)
                frames = []
                try:
                    for i in range(0, int(RATE / CHUNK * MAX_RECORD_SECONDS)):
                        data = stream.read(CHUNK)
                        frames.append(data)
                except KeyboardInterrupt:
                    print('正在生成录音文件...')

                stream.stop_stream()
                stream.close()
                p.terminate()

                current_timestamp = int(time.time() * 1e3)
                file_name = 'output' + '_' + str(current_timestamp) + '.wav'
                wf = wave.open(AUDIO_BASE_DIR + '/' + file_name, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
                wf.close()
                print('录音结束.')

                result = recognize_audio(file_name)
                chat(result)
                print('\n')
            except Exception as e:
                print(f"chat过程中出现错误：{e}")
            desc()


if __name__ == '__main__':
    command()
