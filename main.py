import sounddevice as sd
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from scipy import signal

device_list = sd.query_devices()
print(device_list)

sd.default.device = [1, 6] # type: ignore # Input, Outputデバイス指定

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
    global plotdata, window
    x = plotdata[-N:] * window
    F = np.fft.fft(x) # フーリエ変換
    F = F / (N / 2) # フーリエ変換の結果を正規化
    F = F * (N / sum(window)) # 窓関数による補正
    Amp = np.abs(F) # 振幅スペクトル
    line.set_ydata(Amp[:N // 2])

    return line,

downsample = 1  # FFTするのでダウンサンプリングはしない
length = int(1000 * 48000 / (1000 * downsample))
plotdata = np.zeros((length))
N =2048            # FFT用のサンプル数
fs = 48000            # 音声データのサンプリング周波数
window = signal.hann(N) # 窓関数 # type: ignore
freq = np.fft.fftfreq(N, d=1 / fs) # 周波数スケール

fig, ax = plt.subplots()
line, = ax.plot(freq[:N // 2], np.zeros(N // 2))
ax.set_ylim([0, 0.5]) # type: ignore
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