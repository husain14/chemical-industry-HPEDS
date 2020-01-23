from flask import *
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import os
import cv2
import datetime
import webbrowser 
import time
app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
handle = webbrowser.get()
cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:port"}})

@app.route('/')  
def customer():  
	return render_template('index.html')  
  

def print_data():
	cap=cv2.VideoCapture('templates/box.mp4');
	while(cap.isOpened()):
		ret,img = cap.read()
		if ret == True:
			img=cv2.resize(img, (0,0), fx=0.5, fy=0.5)
			frame = cv2.imencode('.jpg', img)[1].tobytes()
			yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'+ frame +b'\r\n')
			time.sleep(0.025)
		else:
			break
	
	
	
	
@app.route('/survey',methods = ['POST', 'GET'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def data():
	global hathelmet,eyemask,mask,respiratory,vest,gloves,boots,completecoat;
	if request.method == 'POST':
		hathelmet = request.form.get('hathelmet');
		eyemask = request.form.get('eyemask');
		mask = request.form.get('mask');
		respiratory = request.form.get('respiratory');
		vest = request.form.get('vest');
		gloves = request.form.get('gloves');
		boots = request.form.get('boots');
		completecoat = request.form.get('completecoat');
		print(hathelmet,eyemask,mask,respiratory,vest,gloves,boots,completecoat)
		print_data()
	return Response(print_data(),mimetype="multipart/x-mixed-replace;boundary=frame")
	
	
@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

if __name__ == '__main__':  
	app.run(debug = True)  
