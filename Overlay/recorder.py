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
from cv2 import cv2


class Recorder:
    def __init__(self):
        print(termcolor.colored("\nIf you have noises, turn off microphone", "yellow"))
        while True:
            try:
                self.fps = int(input("Write in how many fps record video: "))
                break
            except ValueError:
                print(termcolor.colored("You have to write number", "red"))
        if self.fps > 75:
            self.fps = 75
            print(termcolor.colored("Max fps is 75", "red"))
        elif self.fps < 5:
            self.fps = 5
            print(termcolor.colored("Minimum fps is 5", "red"))
        i = 5
        for _ in range(5):
            print(f"Time to start: {i}")
            i -= 1
            time.sleep(1)
        self.end_record = False
        self.done_voice_saving = False
        self.sound_filename = "data//videos_data//sound.wav"
        self.video_filename = "data//videos_data//video.mp4"
        threading.Thread(target=self.record_sound, daemon=True).start()
        threading.Thread(target=self.record_video, daemon=True).start()
        self.waiting_for_input()

    def record_sound(self):
        freq = 44100
        duration = 3
        i = 0
        data = []
        while not self.end_record:
            recording = sd.rec(int(duration*freq), samplerate=freq, channels=2)
            sd.wait()
            wv.write(f"data//videos_data//frame_sound{i}.wav", recording, freq, sampwidth=2)
            w = wave.open(f"data//videos_data//frame_sound{i}.wav")
            data.append([w.getparams(), w.readframes(w.getnframes())])
            w.close()
            os.remove(f"data//videos_data//frame_sound{i}.wav")
            i += 1
        sound_file = wave.open(self.sound_filename, "wb")
        sound_file.setparams(data[0][0])
        for i in range(len(data)):
            sound_file.writeframes(data[i][1])
        sound_file.close()
        self.done_voice_saving = True

    def record_video(self):
        width = win32api.GetSystemMetrics(0)
        height = win32api.GetSystemMetrics(1)
        codec = cv2.VideoWriter_fourcc(*"mp4v")
        video = cv2.VideoWriter(self.video_filename, codec, self.fps, (width, height))
        while not self.end_record:
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
        if video_name == "":
            video_name = "video"
        video_path = f"Videos//{video_name}.mp4"
        final_video_with_sound.write_videofile(video_path, self.fps)
        sound.close()
        video.close()
        os.remove(self.sound_filename)
        os.remove(self.video_filename)
        abs_video_path = os.path.abspath(video_path)
        print(termcolor.colored(termcolor.colored(f"Recording done. Video saved in {abs_video_path}\n", "green")))

    def waiting_for_input(self):
        print(termcolor.colored("Recording. Click enter to stop --> ", "yellow"))
        input()
        print(termcolor.colored("Saving...", "yellow"))
        self.end_record = True
        while not self.done_voice_saving:
            time.sleep(1)
        self.add_video_to_sound()
