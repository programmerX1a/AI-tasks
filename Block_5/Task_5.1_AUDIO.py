
import matplotlib.pyplot as plt
import numpy as np
import os
import scipy.ndimage as ndimage
from scipy.io import wavfile
import noisereduce as nr

from scipy.signal import  sosfiltfilt,spectrogram,butter, filtfilt,wiener
from IPython.display import Audio,display
fs,data=wavfile.read(os.path.abspath("task5_1.wav"))



if len(data.shape) > 1:
    data = data[:, 0]


#Frequency domain
freq = np.fft.rfftfreq(len(data), d=1/fs)
fft_data = np.fft.rfft(data) 
magnitude = np.abs(fft_data) / len(data)  
phase=np.angle(fft_data)

#Spike Suppression using median filter
window_size=4096
median_magnitude = ndimage.median_filter(magnitude, size=window_size)

clean_magnitude = magnitude.copy()
threshold=3
clean_magnitude[magnitude>median_magnitude*threshold]=median_magnitude[magnitude>median_magnitude*threshold]
clean_fft = clean_magnitude * np.exp(1j * phase) #Polar form
data = np.fft.irfft(clean_fft, n=len(data))

#Allow the human voice band
sos=butter(60,[80,4000],fs=fs,output='sos',btype='bandpass')
data=sosfiltfilt(sos,data)


data=nr.reduce_noise(data,sr=fs)
data=wiener(data,3)
data*=10

wavfile.write("task5_1_clean.wav",fs,data.astype(np.float32))

display(Audio(data,rate=fs))







freq_s,time_s,sxx=spectrogram(data,fs=fs,window='hann',nperseg=1024,scaling='spectrum')

sxx=10*np.log10(sxx+1e-12)
plt.figure()
plt.pcolormesh(time_s, freq_s, sxx, shading='gouraud', cmap='viridis')
plt.colorbar(label='Magnitude')
plt.title('Spectrogram')
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.ylim(0, 10000) 
plt.tight_layout()
plt.show()

plt.figure()
plt.plot(freq, magnitude)
plt.title('Frequency Spectrum (Old)')
plt.xlabel('Frequency ')
plt.ylabel('Magnitude ')
plt.grid(True)
plt.tight_layout()
plt.xlim(0,5000)
plt.show()




plt.figure()
plt.plot(freq, clean_magnitude)
plt.title('Frequency Spectrum (Cleaned)')
plt.xlabel('Frequency ')
plt.ylabel('Magnitude ')
plt.grid(True)
plt.tight_layout()
plt.xlim(0,5000)
plt.show()
plt.figure()
t=np.linspace(0,len(data)/fs,len(data))
plt.plot(t, data)
plt.title('Time Spectrum')
plt.xlabel('Time ')
plt.ylabel('Amplitude ')
plt.grid(True)
plt.tight_layout()
plt.show()
