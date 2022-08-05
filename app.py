import http
from flask import Flask, request, Response
from werkzeug.utils import secure_filename
import os
import cv2

# from db import db_init, db
# from models import Img




app = Flask(__name__)


def getMatchedFinderAdhar(image):
    sample = cv2.imread('8__M_Left_thumb_finger_sample.BMP')
    best_score = 0
    filename = None
    image = None
    kp1, kp2, mp = None, None, None


    counter =0
    for folder in os.listdir("/home/sourav/projects/python/fingerprint/archive/SOCOFing/Altered"):
        for file in [file for file in os.listdir("/home/sourav/projects/python/fingerprint/archive/SOCOFing/Altered/" + folder)]:
            print(counter)
            counter+=1
            fingerprint_image = cv2.imread('/home/sourav/projects/python/fingerprint/archive/SOCOFing/Altered/' + folder + '/' +file)
            sift = cv2.SIFT_create()

            keypoint_1, desriptors_1 = sift.detectAndCompute(sample, None)
            keypoint_2, desriptors_2 = sift.detectAndCompute(fingerprint_image, None)

            matches = cv2.FlannBasedMatcher({'algorithm': 0, 'trees': 10},
                    {}).knnMatch(desriptors_1, desriptors_2, k=2)

            match_points = []

            for p, q in matches:
                if p.distance < 0.1 * q.distance:
                    match_points.append(p)

            keypoints =0
            if len(keypoint_1) < len(keypoint_2):
                keypoints = len(keypoint_2)

            else:
                keypoints = len(keypoint_1)

            if len(match_points)/keypoints * 100 > best_score:
                best_score = len(match_points)/keypoints * 100
                filename = file
                image = fingerprint_image
                kp1 = keypoint_1
                kp2 = keypoint_2
                mp = match_points

    print("best match: " + filename)
    print("score: " + str(best_score))

    result = cv2.drawMatches(sample, kp1, image, kp2, mp, None)
    result = cv2.resize(result, (0,0), fx=4, fy=4)
    data = {}
    return http(data)



@app.route('/upload', methods=['POST'])
def upload():
    pic = request.files['pic']
    if not pic:
        return 'No pic uploaded!', 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400

    img = Img(img=pic.read(), name=filename, mimetype=mimetype)

    return type(img)


appFlask = Flask(__name__)
@appFlask.route('/home')
def home():
    result = 10/0
    return 'We are learning HTTPS @ EduCBA'
if __name__ == "__main__":
    appFlask.run(debug=True)