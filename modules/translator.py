import speech_recognition as sr
from moviepy.editor import VideoFileClip
from googletrans import Translator as GoogleTranslator

class Translator:
    def __init__(self):
        self.translator = GoogleTranslator()
        self.recognizer = sr.Recognizer()

    def translate_text(self, text, dest_lang):
        translation = self.translator.translate(text, dest=dest_lang)
        return translation.text

    def translate_audio(self, audio_file_path, dest_lang):
        with sr.AudioFile(audio_file_path) as source:
            audio_data = self.recognizer.record(source)
            text = self.recognizer.recognize_google(audio_data)
            translation = self.translator.translate(text, dest=dest_lang)
            return translation.text

    def translate_video(self, video_file_path, dest_lang):
        clip = VideoFileClip(video_file_path)
        audio_file_path = video_file_path.replace('.mp4', '.wav')
        clip.audio.write_audiofile(audio_file_path)
        
        return self.translate_audio(audio_file_path, dest_lang)