import sounddevice as sd
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import find_peaks

device_list = sd.query_devices()
print(device_list)

sd.default.device = [1, 6] # type: ignore # Input, Outputデバイス指定
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
    """This is called by matplotlib for each plot update.
    """
    global plotdata, window, peak_freqs, peak_amplitudes
    x = plotdata[-N:]
    F = np.fft.fft(x) # フーリエ変換
    F = F / (N / 2) # フーリエ変換の結果を正規化
    F = F * (N) # 窓関数による補正
    Amp = np.abs(F) # 振幅スペクトル
    line.set_ydata(Amp[:N // 2])

     # ピーク検出
    peaks, _ = find_peaks(Amp[:N // 2], height=7)  # 閾値を調整可能
    peak_freqs = freq[:N // 2][peaks]  # 周波数の配列からピーク周波数を取得
    peak_amplitudes = Amp[:N // 2][peaks]  # 振幅の配列からピーク振幅を取得

    print(peak_freqs)

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