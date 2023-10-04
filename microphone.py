import sounddevice as sd

# 利用可能なオーディオデバイスのリストを取得
device_list = sd.query_devices()

sd.default.device = [1,6] # type: ignore

# マイクのデバイス情報を特定
microphone_device = None
for device_info in device_list:
    if "Microphone" in device_info["name"]: # type: ignore
        microphone_device = device_info
        break

# マイクのサンプリングレートを表示
if microphone_device:
    print(f"マイクのサンプリングレート: {microphone_device['default_samplerate']} Hz") # type: ignore
else:
    print("マイクが見つかりませんでした。")