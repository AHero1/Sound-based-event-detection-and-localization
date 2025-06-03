import threading
import signal
import numpy as np
import pyaudio
import scipy
import matplotlib.pyplot as plt

BUFFER_SIZE = 2**11
SAMPLING_RATE = 44100

# Instantiate the microphones
mic_right = pyaudio.PyAudio()
mic_center = pyaudio.PyAudio()
mic_left = pyaudio.PyAudio()

class FFTVisualizer:
    def __init__(self, buffer_size, sampling_rate):
        self.fig, self.ax = plt.subplots()

        # Get frequencies for x-axis in Hz
        coefficients = np.fft.fftfreq(buffer_size)
        x_freq = [np.abs(c * sampling_rate) for c in coefficients]

        # Initialize y-axis with random values
        highest_random_number = np.iinfo(np.int16).max * 10
        y_random = np.random.randint(low=0, high=highest_random_number, size=buffer_size)

        # Plot and get line object
        self.line, = self.ax.plot(x_freq, y_random)

        # Style plot
        self.ax.set_xlim(0, sampling_rate / 4)
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("Amplitude / FFT Magnitude")
        plt.show(block=False)

        # Assign class variables
        self.fig = self.fig
        self.line = self.line

    # Plot y-values for the graph (must have length of buffer_size)
    # y should be result of FFT
    def plot(self, y):
        self.line.set_ydata(y)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def close(self):
        plt.close(self.fig)

class FFTNormalizedDBVisualizer:
    def __init__(self, buffer_size, sampling_rate):
        self.fig, self.ax = plt.subplots()

        # Get frequencies for x-axis in Hz
        coefficients = np.fft.fftfreq(buffer_size)
        x_freq = [np.abs(c * sampling_rate) for c in coefficients]

        # Initialize y-axis with random values in the range -240 to 0 dB
        y_random = np.random.randint(low=240 * -1, high=0, size=buffer_size)

        # Plot and get line object
        self.line, = self.ax.plot(x_freq, y_random)

        # Style plot
        self.ax.set_xlim(0, sampling_rate / 4)
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("Normalized Sound Pressure Level [dB]")
        plt.show(block=False)

        # Assign class variables
        self.fig = self.fig
        self.line = self.line

    # y should be result of normalizedDb(FFT)
    def plot(self, y):
        self.line.set_ydata(y)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def close(self):
        plt.close(self.fig)

def normalized_db(sound_data, buffer_size):
    sound_data_fft = np.abs(np.fft.fft(sound_data) / 2).astype(int)
    
    # Calculate normalized db level
    for i in range(len(sound_data_fft)):
        if sound_data_fft[i] > 0:
            sound_data_fft[i] = 20 * (np.log10(sound_data_fft[i]) - np.log10(buffer_size * 32768))
        else:
            sound_data_fft[i] = -200
            
    return sound_data_fft

def delay(signal1, signal2, sampling_rate):
    n = len(signal1)
    similarity = np.correlate(signal2, signal1, mode='full') 
    lag = np.arange(-len(signal2) + 1, len(signal1))
    index = np.argmax(abs(similarity))
    delay = lag[index] / sampling_rate
    return delay

stream_right = mic_right.open(format=pyaudio.paInt16,
                              input_device_index=2,
                              channels=1,
                              rate=SAMPLING_RATE,
                              input=True,
                              frames_per_buffer=BUFFER_SIZE)

stream_center = mic_center.open(format=pyaudio.paInt16,
                                input_device_index=3,
                                channels=1,
                                rate=SAMPLING_RATE,
                                input=True,
                                frames_per_buffer=BUFFER_SIZE)

stream_left = mic_left.open(format=pyaudio.paInt16,
                            input_device_index=4,
                            channels=1,
                            rate=SAMPLING_RATE,
                            input=True,
                            frames_per_buffer=BUFFER_SIZE)

sound_data_right = [0] * BUFFER_SIZE
sound_data_center = [0] * BUFFER_SIZE
sound_data_left = [0] * BUFFER_SIZE

whistle_flag_right = False
whistle_flag_center = False
whistle_flag_left = False

# Initialize shutdown process on Ctrl+C
print("Starting... use Ctrl+C to stop")
def handle_close(signum, frame):
    print("\nStopping")
    stream_right.close()
    stream_center.close()
    stream_left.close()
    mic_right.terminate()
    mic_center.terminate()
    mic_left.terminate()
    exit(1)
signal.signal(signal.SIGINT, handle_close)

# Thread for MIC-1 
def mic_thread_right():
    global whistle_flag_right
    global sound_data_right
    i = 0
    while True:
        data_buffer = stream_right.read(BUFFER_SIZE, exception_on_overflow=False)
        sound_data_right = np.frombuffer(data_buffer, dtype=np.int16)
        y_fft = np.fft.fft(sound_data_right)
        y_fft = np.abs(y_fft).astype(int)
        if any(value > 8000000 for value in y_fft[1900:2000]):
            print("Whistle detected in MIC-1 ", i)
            i += 1
            whistle_flag_right = True

# Thread for MIC-2
def mic_thread_center():
    global whistle_flag_center
    global sound_data_center
    i = 0
    while True:
        data_buffer = stream_center.read(BUFFER_SIZE, exception_on_overflow=False)
        sound_data_center = np.frombuffer(data_buffer, dtype=np.int16)
        y_fft = np.fft.fft(sound_data_center)
        y_fft = np.abs(y_fft).astype(int)
        if any(value > 8000000 for value in y_fft[1900:2000]):
            print("Whistle detected in MIC-2", i)
            i += 1
            whistle_flag_center = True

# Thread for MIC-3
def mic_thread_left():
    global whistle_flag_left
    global sound_data_left
    k = 0
    while True:
        data_buffer = stream_left.read(BUFFER_SIZE, exception_on_overflow=False)
        sound_data_left = np.frombuffer(data_buffer, dtype=np.int16)
        y_fft = np.fft.fft(sound_data_left)
        y_fft = np.abs(y_fft).astype(int)
        if any(value > 8000000 for value in y_fft[1900:2000]):
            print("Whistle detected in MIC-3 ", k)
            k += 1
            whistle_flag_left = True

def main_thread():
    global whistle_flag_right
    global whistle_flag_center
    global whistle_flag_left
    global sound_data_right
    global sound_data_center
    global sound_data_left
    global SAMPLING_RATE
    while True:
        if whistle_flag_right or whistle_flag_center or whistle_flag_left:
            delay_right_center = delay(sound_data_right, sound_data_center, SAMPLING_RATE)
            delay_left_center = delay(sound_data_center, sound_data_left, SAMPLING_RATE)
            delay_right_left = delay(sound_data_right, sound_data_left, SAMPLING_RATE)
            print('Time delay between right and center: ', delay_right_center)
            print('Time delay center and left: ', delay_left_center)
            print('Time delay right and left: ', delay_right_left)
            delay_right_center = delay(sound_data_right, sound_data_center, SAMPLING_RATE)
            delay_left_center = delay(sound_data_center, sound_data_left, SAMPLING_RATE)
            delay_right_left = delay(sound_data_right, sound_data_left, SAMPLING_RATE)
            if whistle_flag_right:
                print('Sound from the right')
                
            elif whistle_flag_center:
                print('Sound from the center')
                
            elif whistle_flag_left:
                print('Sound from the left')
            whistle_flag_right = whistle_flag_center = whistle_flag_left = False    

thrd1 = threading.Thread(target=mic_thread_right)
thrd2 = threading.Thread(target=mic_thread_center)
thrd3 = threading.Thread(target=mic_thread_left)
thrd4 = threading.Thread(target=main_thread)

thrd1.start()
thrd2.start()
thrd3.start()
thrd4.start()

thrd1.join()
thrd2.join()
thrd3.join()
thrd4.join()

print("Main thread exiting...")
