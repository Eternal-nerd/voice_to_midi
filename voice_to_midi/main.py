import sounddevice as sd
import numpy as np
from scipy.fftpack import fft
import math
import mido

outport = mido.open_output('Rev2 1')

def audio_callback(indata, frames, time, status):
    if status:
        print(status)

    audio_data = np.array(indata[:,0], dtype=np.float32)
    fft_data = np.abs(fft(audio_data))

    volume = round(np.average(np.abs(audio_data)) * 127)
    freqency = get_freq(fft_data)
    
    print(f"volume: {volume} | frequency: {freqency}")

    play_note(freq=freqency, vel=volume, time=1)

def get_freq(fft_bin):
    index = np.argmax(fft_bin)
    frequency = index * 44100 / 1024 # sample rate and block size
    return(frequency)

#notes between 0-127
#note 60 is middle C (C4) and is 261.63 hz
# vel: 0-127
def play_note(freq, vel, time):
    global outport

    if (freq == 0) or (vel < 7): #if somehow frequency is 0 or low volume dont play note
        return(0)

    close_note = round(12 * math.log2(freq / 440) + 69) # convert freqeuncy to midi key
    
    message = mido.Message('note_on', note=close_note, velocity=vel, time=time)
    outport.send(message)
    return(0)

def main():
    sr = 44100
    channels = 1 # since I only want the left channel
    duration = 20
    blocksize = 1024

    in_stream = sd.InputStream(
        callback=audio_callback,
        samplerate=sr,
        blocksize=blocksize,
        channels=channels
    )
    with in_stream:
        sd.sleep(duration*1000)

if __name__ == "__main__":
    main()