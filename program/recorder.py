import sounddevice as sd
import pyautogui
import numpy as np
import wavio as wv
import wave
import win32api
import os
import threading
from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip
import time
import termcolor
try:                     #
    from cv2 import cv2  # fix "cannot find reference" in Pycharm IDE for cv2 module
except ImportError:      #
    pass                 #


class Recorder:
    def __init__(self, checking_input_function, fps):
        self.end_record = False
        self.checking_input_function = checking_input_function
        self.fps = fps
        self.sound_filename = "data\\videos_data\\sound.wav"
        self.video_filename = "data\\videos_data\\video.mp4"
        threading._start_new_thread(self.record_sound, ())
        threading._start_new_thread(self.record_video, ())
        threading._start_new_thread(self.waiting_for_input, ())

    def record_sound(self):
        freq = 44100
        duration = 3
        i = 0
        data = []
        while True:
            if self.end_record:
                break
            recording = sd.rec(int(duration*freq), samplerate=freq, channels=2)
            sd.wait()
            wv.write(f"data\\videos_data\\frame_sound{i}.wav", recording, freq, sampwidth=2)
            w = wave.open(f"data\\videos_data\\frame_sound{i}.wav")
            data.append([w.getparams(), w.readframes(w.getnframes())])
            w.close()
            os.remove(f"data\\videos_data\\frame_sound{i}.wav")
            i += 1
        sound_file = wave.open(self.sound_filename, "wb")
        sound_file.setparams(data[0][0])
        for i in range(len(data)):
            sound_file.writeframes(data[i][1])
        sound_file.close()

    def record_video(self):
        width = win32api.GetSystemMetrics(0)
        height = win32api.GetSystemMetrics(1)
        codec = cv2.VideoWriter_fourcc(*"mp4v")
        video = cv2.VideoWriter(self.video_filename, codec, self.fps, (width, height))
        while True:
            if self.end_record:
                break
            frame = pyautogui.screenshot()
            frame = np.array(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            video.write(frame)
        video.release()

    def add_video_to_sound(self):
        video = VideoFileClip(self.video_filename)
        sound = AudioFileClip(self.sound_filename)
        final_video_with_sound = video.set_audio(sound)
        video_name = input("Write how name this video: ")
        final_video_with_sound.write_videofile(f"videos\\{video_name}.mp4", self.fps)
        sound.close()
        video.close()
        os.remove(self.sound_filename)
        os.remove(self.video_filename)
        abs_video_path = os.path.abspath(f"videos\\{video_name}.mp4")
        print(termcolor.colored(termcolor.colored(f"Recording done. Video saved in {abs_video_path}\n", "green")))
        self.checking_input_function()

    def waiting_for_input(self):
        while not self.end_record:
            print(termcolor.colored("Recording. Write 'q' to stop --> ", "yellow"))
            q = input()
            if q == "q":
                print(termcolor.colored("Saving...", "yellow"))
                self.end_record = True
                time.sleep(6)
                self.add_video_to_sound()
