import time
import pyaudio
import wave
from app.asr import single_flash_sr_with_file_name

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
MAX_RECORD_SECONDS = 30
AUDIO_BASE_DIR = './audio'


def recording():
    print('按下【r】开始录音，按下【Ctrl + C】中止录音，按下【q】退出程序，录音最长持续时间30s')
    try:
        while True:
            key = input('>>> ')
            if key.lower() == 'r':
                print('正在录音...')
                break
            elif key.lower() == 'q':
                print('bye~')
                break

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


def play_audio(audio_file_name: str):
    # 只读方式打开wav文件
    wf = wave.open(AUDIO_BASE_DIR + '/' + audio_file_name, 'rb')  # (sys.argv[1], 'rb')
    p = pyaudio.PyAudio()
    # 打开数据流
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # 读取数据
    data = wf.readframes(wf.getnframes())

    # 播放音频
    stream.write(data)

    # 停止数据流
    stream.stop_stream()
    stream.close()

    # 关闭 PyAudio
    p.terminate()


def generate_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    for i in range(0, int(RATE / CHUNK * MAX_RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()

    current_timestamp = int(time.time() * 1e3)
    file_name = 'output' + '_' + str(current_timestamp) + '.wav'
    wf = wave.open(file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def recognize_audio(audio_file_name: str):
    file_path = AUDIO_BASE_DIR + '/' + audio_file_name
    print('录音文件【{}】识别中...' . format(audio_file_name))
    result = single_flash_sr_with_file_name(file_path, 'wav')
    print('录音文件【{}】识别结果：{}' . format(audio_file_name, result))

    return result


if __name__ == '__main__':
    recording()
