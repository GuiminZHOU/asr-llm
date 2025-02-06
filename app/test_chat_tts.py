import ChatTTS
import torch
import torchaudio

input_dir = "../data/"

chat = ChatTTS.Chat()
chat.load(compile=False) # Set to True for better performance

texts = ["不愧是冠军队，等级压制14级又怎样"]

wavs = chat.infer(texts)

torchaudio.save(f"{input_dir}output1.wav", torch.from_numpy(wavs[0]), 16000)