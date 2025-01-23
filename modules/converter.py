from moviepy.editor import VideoFileClip
from fpdf import FPDF
from PIL import Image
import speech_recognition as sr
import qrcode

class Con:
    def __init__(self):
        print("Con Initialized")

    def video_to_audio(self, video_path):
        clip = VideoFileClip(video_path)
        audio_path = video_path.replace('.mp4', '.mp3')
        clip.audio.write_audiofile(audio_path)
        return audio_path

    def video_to_voice(self, video_path):
        clip = VideoFileClip(video_path)
        voice_path = video_path.replace('.mp4', '.ogg')
        clip.audio.write_audiofile(voice_path, codec='libvorbis')
        return voice_path

    def image_to_pdf(self, image_path):
        image = Image.open(image_path)
        pdf_path = image_path.replace('.jpg', '.pdf').replace('.jpeg', '.pdf').replace('.png', '.pdf')

        pdf = FPDF()
        pdf.add_page()
        pdf.image(image_path, x=10, y=8, w=190)
        pdf.output(pdf_path)

        return pdf_path

    def video_to_text(self, video_path):
        audio_path = self.video_to_audio(video_path)
        recognizer = sr.Recognizer()

        with sr.AudioFile(audio_path) as source:
            audio_data = source.read()
            text = recognizer.recognize_google(audio_data)

        return text

    def video_to_gif(self, video_path):
        clip = VideoFileClip(video_path)
        gif_path = video_path.replace('.mp4', '.gif')
        clip.write_gif(gif_path)
        return gif_path

    def generate_qr_code(self, text):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        qr_code_path = 'qr_code.png'
        img.save(qr_code_path)

        return qr_code_path