import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment #remove later
import math
import librosa.core as lc
import queue
import time
import mido
import random as rd
import sys
import threading


#notes between 0-127
#note 60 is middle C (C4) and is 261.63 hz
def get_close_note(freq):
    note = round(12 * math.log2(freq / 440) + 69)
    return(note)

def play_note(note, vel, time):
    return()

def get_pitch(frame, sr):
    cents = lc.estimate_tuning(y=frame, sr=sr)
    pitch = 2 ** (cents/1200) * 440
    return pitch

def main():
    filename = 'sample.wav'
    global current_frame
    current_frame = 0
    global blocksize
    blocksize = 1024
    buffersize = 20
    duration = 12 
    channels = [2]
    downsample = 10
    interval = 30 # in ms
    mapping = [c - 1 for c in channels]  # Channel numbers start with 1
    global q
    q = queue.Queue()
    #frame_list = []

    def callback(outdata, frames, time, status):
        global current_frame
        global blocksize
        global q
        if status:
            print(status)
        try:
            data = q.get_nowait()
        except queue.Empty:
            print("Error: Queue Empty")
            return(-1)

        if len(data) < len(outdata):
            outdata[:len(data)] = data
            outdata[len(data):].fill(0)
        else:
            outdata[:] = data


    #fill queue
    with sf.SoundFile(filename) as file:
        for i in range(buffersize):
            data = file.read(blocksize)
            if len(data) == 0:
                break
            q.put_nowait(data)

        outstream = sd.OutputStream(
            samplerate=file.samplerate,
            blocksize=blocksize,
            device=sd.default.device, #FIXME?
            channels=file.channels,
            callback=callback
            )
        with outstream:
            timeout = blocksize*buffersize/file.samplerate
            while (len(data)):
                data = file.read(blocksize)
                q.put(data, timeout=timeout)
            sd.sleep(duration*1000)










    #outport = mido.open_output('Rev2 1')
    #message = mido.Message('note_on', note=50, velocity=100, time=1)
    #outport.send(message)
    '''for i in range(127):
        ran = rd.randint(1, 127)
        message = mido.Message('note_on', note=i, velocity=100, time=1)
        outport.send(message)
        message = mido.Message('note_on', note=ran, velocity=100, time=1)
        outport.send(message)
        time.sleep(0.1)'''


if __name__ == "__main__":
    main()
    quit()