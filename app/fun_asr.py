import os

from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
from dotenv import load_dotenv
load_dotenv()
model_dir = os.getenv("FUNASR_MODEL_DIR")
if model_dir == "":
    model_dir = "iic/SenseVoiceSmall"


def recognize(file_name: str):
    model = AutoModel(
        model=model_dir,
        disable_update=True,
    )

    # en
    res = model.generate(
        input=file_name,
        language="auto",  # "zn", "en", "yue", "ja", "ko", "nospeech"
    )
    return rich_transcription_postprocess(res[0]["text"])


if __name__ == '__main__':
    res = recognize("../data/237628379833701364.wav")
    print(res)