from flask import Flask, render_template, Response,url_for,redirect,jsonify
from pdetect import out
from cv2 import VideoCapture
import time
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Index.html')

def gen():
    cap = VideoCapture(-1)
    heartbeat_count = 128
    heartbeat_values = [0]*heartbeat_count
    heartbeat_times = [time.time()]*heartbeat_count
    while True:
        frame= out(cap,heartbeat_values,heartbeat_times)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        # yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n\r\n')
# def gen1():
#     cap = VideoCapture(-1)
#     while True:
#         frame,frame1= out(cap)
#         yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n\r\n')


@app.route('/monitor')
def monitor():
    return render_template('monitor.html')
            
        
@app.route('/video_feed')
def video_feed():
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/graph_feed')
# def graph_feed():
#     return Response(gen1(),mimetype='multipart/x-mixed-replace; boundary=frame1')


if __name__ == '__main__':
    app.run(debug=True)