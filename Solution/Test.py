import cv2
import numpy as np
from DLmodel import DeepLabModel
from PIL import Image
cap = cv2.VideoCapture("../small.mp4")
MODEL = DeepLabModel("mobile_net_model")
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
while (True):
    ret,img = cap.read()
    img=run_visualization(Image.fromarray(img))
    cv2.imshow("Video",img)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()