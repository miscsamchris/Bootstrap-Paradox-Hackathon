import pafy
import cv2
import numpy as np
from DLmodel import DeepLabModel
from PIL import Image
MODEL = DeepLabModel("mobile_net_model")
from flask import Flask, render_template, Response
app = Flask(__name__)
url = "https://www.youtube.com/watch?v=arhjhHeuRUc"
video = pafy.new(url)
best = video.getbest(preftype="mp4")
cap = cv2.VideoCapture(best.url)
@app.route('/')
def index():
    return render_template('index.html')
def gen():
    """Video streaming generator function."""
    while True:
        ret, img = cap.read()
        img=run_visualization(Image.fromarray(img))
        cv2.imwrite('t.jpg', img)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
@app.route('/video_feed')
def video_feed():
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

def run_visualization(img):
    resized_im, seg_map = MODEL.run(img)
    return display(resized_im, seg_map)
def display(baseImg, matImg):
  width, height = baseImg.size
  dummyImg = np.zeros([height, width, 4], dtype=np.uint8)
  for x in range(width):
            for y in range(height):
                color = matImg[y,x]
                (r,g,b) = baseImg.getpixel((x,y))
                if color == 0:
                    dummyImg[y,x,3] = 0
                else :
                    dummyImg[y,x] = [r,g,b,255]
  return dummyImg
# =============================================================================
# while (True):
#     ret,img = cap.read()
#     img=run_visualization(Image.fromarray(img))
#     cv2.imshow("Video",img)
#     if cv2.waitKey(20) & 0xFF == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()
# =============================================================================

if __name__ == '__main__':
    app.run(host='localhost', debug=True, threaded=True)