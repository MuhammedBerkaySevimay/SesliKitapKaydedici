import pyaudio
import wave
import keyboard
import threading
import os

# Ses kaydı ayarları
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 3600  # Maksimum kayıt süresi (örneğin 1 saat)
WAVE_OUTPUT_FILENAME = "output.wav"

# Global değişkenler
frames = []
flag_index = None

# Ses kaydı fonksiyonu
def record_audio():
    global frames
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Recording... Press 'f' to flag, 'r' to reset to last flag, 'q' to quit.")

    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        if keyboard.is_pressed('f'):
            global flag_index
            flag_index = len(frames)
            print(f"Flag added at frame {flag_index}")

        if keyboard.is_pressed('r'):
            if flag_index is not None:
                frames = frames[:flag_index]
                print(f"Recording reset to frame {flag_index}")
            else:
                print("No flag to reset to.")

        if keyboard.is_pressed('q'):
            break

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Kaydı başlatma fonksiyonu
def start_recording():
    record_thread = threading.Thread(target=record_audio)
    record_thread.start()

# Programı çalıştır
if __name__ == "__main__":
    start_recording()
