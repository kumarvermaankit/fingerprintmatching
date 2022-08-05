from http.client import HTTPResponse
import re
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
import cv2

def getMatchedFinderAdhar(image):
    sample = cv2.imread(image)
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

    #result = cv2.drawMatches(sample, kp1, image, kp2, mp, None)
    #result = cv2.resize(result, (0,0), fx=4, fy=4)
    return HttpResponse('aadhar data')
@csrf_exempt

def matching(request):
    file = request.FILES.get('file')
    data = request.POST.get('data')
    print(data)
    print(type(file))
    if file is None:
        return HttpResponse("No file")
    else:
        data = request.FILES['file'] # or self.files['image'] in your form
        path = default_storage.save('tmp/somename.BMP', ContentFile(data.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        return getMatchedFinderAdhar(tmp_file)   