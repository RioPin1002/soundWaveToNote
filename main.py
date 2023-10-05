import sounddevice as sd
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import find_peaks


device_list = sd.query_devices()
print(device_list)


# 音階と対応する周波数の辞書を定義
note_to_frequency = {
    'A0': 27.50, 'A#0/Bb0': 29.14, 'B0': 30.87,
    'C1': 32.70, 'C#1/Db1': 34.65, 'D1': 36.71, 'D#1/Eb1': 38.89, 'E1': 41.20, 'F1': 43.65, 'F#1/Gb1': 46.25, 'G1': 49.00, 'G#1/Ab1': 51.91, 'A1': 55.00, 'A#1/Bb1': 58.27, 'B1': 61.74,
    'C2': 65.41, 'C#2/Db2': 69.30, 'D2': 73.42, 'D#2/Eb2': 77.78, 'E2': 82.41, 'F2': 87.31, 'F#2/Gb2': 92.50, 'G2': 98.00, 'G#2/Ab2': 103.83, 'A2': 110.00, 'A#2/Bb2': 116.54, 'B2': 123.47,
    'C3': 130.81, 'C#3/Db3': 138.59, 'D3': 146.83, 'D#3/Eb3': 155.56, 'E3': 164.81, 'F3': 174.61, 'F#3/Gb3': 185.00, 'G3': 196.00, 'G#3/Ab3': 207.65, 'A3': 220.00, 'A#3/Bb3': 233.08, 'B3': 246.94,
    'C4': 261.63, 'C#4/Db4': 277.18, 'D4': 293.66, 'D#4/Eb4': 311.13, 'E4': 329.63, 'F4': 349.23, 'F#4/Gb4': 369.99, 'G4': 392.00, 'G#4/Ab4': 415.30, 'A4': 440.00, 'A#4/Bb4': 466.16, 'B4': 493.88,
    'C5': 523.25, 'C#5/Db5': 554.37, 'D5': 587.33, 'D#5/Eb5': 622.25, 'E5': 659.26, 'F5': 698.46, 'F#5/Gb5': 739.99, 'G5': 783.99, 'G#5/Ab5': 830.61, 'A5': 880.00, 'A#5/Bb5': 932.33, 'B5': 987.77,
    'C6': 1046.50, 'C#6/Db6': 1108.73, 'D6': 1174.66, 'D#6/Eb6': 1244.51, 'E6': 1318.51, 'F6': 1396.91, 'F#6/Gb6': 1479.98, 'G6': 1567.98, 'G#6/Ab6': 1661.22, 'A6': 1760.00, 'A#6/Bb6': 1864.66, 'B6': 1975.53,
    'C7': 2093.00, 'C#7/Db7': 2217.46, 'D7': 2349.32, 'D#7/Eb7': 2489.02, 'E7': 2637.02, 'F7': 2793.83, 'F#7/Gb7': 2959.96, 'G7': 3135.96, 'G#7/Ab7': 3322.44, 'A7': 3520.00, 'A#7/Bb7': 3729.31, 'B7': 3951.07,
    'C8': 4186.01
}


sd.default.device = [0, 6] # type: ignore # Input, Outputデバイス指定
peak_freqs = []  # ピークの周波数を格納
peak_amplitudes = []  # ピークの振幅を格納

def callback(indata, frames, time, status):
    # indata.shape=(n_samples, n_channels)
    global plotdata
    data = indata[::downsample, 0]
    shift = len(data)
    plotdata = np.roll(plotdata, -shift, axis=0)
    plotdata[-shift:] = data



def update_plot(frame):
    global plotdata, window, peak_freqs, peak_amplitudes
    x = plotdata[-N:]
    F = np.fft.fft(x) # フーリエ変換
    F = F / (N / 2) # フーリエ変換の結果を正規化
    F = F * (N) # 窓関数による補正
    Amp = np.abs(F) # 振幅スペクトル
    line.set_ydata(Amp[:N // 2])

     # ピーク検出
    peaks, _ = find_peaks(Amp[:N // 2], height=80)  # 閾値を調整可能
    peak_freqs = freq[:N // 2][peaks]  # 周波数の配列からピーク周波数を取得
    peak_amplitudes = Amp[:N // 2][peaks]  # 振幅の配列からピーク振幅を取得

    


    print(peaks)

    if len(peak_freqs) >= 2:
        frequency = max(peak_amplitudes)
    else:
        # 入力として周波数を受け取る
        frequency = peak_freqs

    # 周波数をもとに最も近い音階を見つける
    closest_note = None
    closest_difference = float('inf')
    for note, frequ in note_to_frequency.items():
        difference = abs(frequency - frequ)
        if difference < closest_difference:
            closest_difference = difference
            closest_note = note

    # 結果を表示
    print(f"入力された周波数 {frequency} Hz に最も近い音階は {closest_note} です。")






    return line,

downsample = 1  # FFTするのでダウンサンプリングはしない
length = int(1000 * 48000 / (1000 * downsample))
plotdata = np.zeros((length))
N =4096            # FFT用のサンプル数
fs = 48000            # 音声データのサンプリング周波数
window = signal.hann(N) # 窓関数 # type: ignore
freq = np.fft.fftfreq(N, d=1 / fs) # 周波数スケール

fig, ax = plt.subplots()
line, = ax.plot(freq[:N // 2], np.zeros(N // 2))
# ピークをプロットに追加
ax.plot(peak_freqs, peak_amplitudes, 'ro', markersize=5)  # ピークを赤い点でプロット
ax.set_ylim([0, 100]) # type: ignore
ax.set_xlim([0, 1000]) # type: ignore
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Amplitude spectrum')
fig.tight_layout()

stream = sd.InputStream(
        channels=1,
        dtype='float32',
        callback=callback
    )
ani = FuncAnimation(fig, update_plot, interval=30, blit=True)
with stream:
    plt.show()