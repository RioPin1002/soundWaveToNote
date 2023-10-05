import sounddevice as sd

# 利用可能なオーディオデバイスのリストを取得
device_list = sd.query_devices()

print(device_list)