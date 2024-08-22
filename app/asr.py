import json
import os
import threading
import time
import nls
from dotenv import load_dotenv
from app.get_token import get_aliyun_token
load_dotenv()

URL = "wss://nls-gateway-cn-shanghai.aliyuncs.com/ws/v1"
APP_KEY = os.getenv("APP_KEY")  # 获取AppKey请前往控制台：https://nls-portal.console.aliyun.com/applist


class FlashSr:
    def __init__(self, test_file, ext):
        self.__data = None
        self.__th = threading.Thread(target=self.__test_run)
        self.__id = 'thread0'
        self.__test_file = test_file
        self.__ext = ext
        self.__result = ''

    def loadfile(self, filename):
        with open(filename, "rb") as f:
            self.__data = f.read()

    def start(self):
        self.loadfile(self.__test_file)
        self.__th.start()
        self.__th.join(timeout=20)

    def on_start(self, message, *args):
        pass

    def on_error(self, message, *args):
        pass

    def on_close(self, *args):
        pass

    def on_result_chg(self, message, *args):
        pass

    def on_completed(self, message, *args):
        try:
            message = json.loads(message)
            if message['payload']['result'] != '':
                self.__result = message['payload']['result']
        except Exception as e:
            print('get asr result failed. args=>{}, message=>{}, error=>{}'.format(args, message, e))

    def get_result(self):
        return self.__result

    def __test_run(self):
        token, expire_time = get_aliyun_token()
        sr = nls.NlsSpeechRecognizer(
            url=URL,
            token=token,
            appkey=APP_KEY,
            on_start=self.on_start,
            on_result_changed=self.on_result_chg,
            on_completed=self.on_completed,
            on_error=self.on_error,
            on_close=self.on_close,
            callback_args=[self.__id]
        )

        sr.start(aformat=self.__ext, ex={"hello": 123})
        self.__slices = zip(*(iter(self.__data),) * 640)
        for i in self.__slices:
            sr.send_audio(bytes(i))
            time.sleep(0.01)
        sr.stop()
        time.sleep(1)


def single_flash_sr_with_file_name(file: str, ext: str):
    t = FlashSr(file, ext)
    t.start()
    return t.get_result()


if __name__ == '__main__':
    # 设置打开日志输出
    nls.enableTrace(False)
    result = single_flash_sr_with_file_name('./audio/output_1724058346221.wav', 'wav')
    print(result)
