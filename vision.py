import tensorflow
import tensorflow_hub as hub
import numpy as np
import cv2 as cv

module = hub.load("https://tfhub.dev/google/movenet/singlepose/lightning/4")

keypointDict = {
	'nose': 0,
	'left_eye': 1,
	'right_eye': 2,
	'left_ear': 3,
	'right_ear': 4,
	'left_shoulder': 5,
	'right_shoulder': 6,
	'left_elbow': 7,
	'right_elbow': 8,
	'left_wrist': 9,
	'right_wrist': 10,
	'left_hip': 11,
	'right_hip': 12,
	'left_knee': 13,
	'right_knee': 14,
	'left_ankle': 15,
	'right_ankle': 16
}

def getKeypointsForDisplay(keypointScores, height, width, keypointThreshold=0.11):
    keypointsAll = []
    keypointEdgesAll = []
    numInstances, _, _, _ = keypointScores.shape
    for idx in range(numInstances):
        keypointsX = keypointScores[0, idx, :, 1]
        keypointsY = keypointScores[0, idx, :, 0]
        keypointScores = keypointScores[0, idx, :, 2]
        keypointsAbsXY = np.stack([width * np.array(keypointsX), height * np.array(keypointsY)], axis=-1)
        keypointsAboveThreshold = keypointsAbsXY[keypointScores > keypointThreshold, :]
        keypointsAll.append(keypointsAboveThreshold)

    if keypointsAll:
        keypointsXY = np.concatenate(keypointsAll, axis=0)
    else:
        keypointsXY = np.zeros((0, 17, 2))

    return keypointsXY

def movenet(inputImage):
    model = module.signatures['serving_default']
    inputImage = tensorflow.cast(inputImage, dtype=tensorflow.int32)
    outputs = model(inputImage)
    keypointScores = outputs['output_0'].numpy()
    return keypointScores

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Can't open camera")
    exit()

def displayVideo(screen):
    _, frame = cap.read()

    frame = cv.resize(frame, (0, 0), fx=0.2, fy=0.2)
    tensorflowImage = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    inputImage = tensorflow.expand_dims(tensorflowImage, axis=0)
    input_image = tensorflow.image.resize_with_pad(inputImage, 192, 192)
    displayImage = tensorflow.expand_dims(tensorflowImage, axis=0)

    keypointScores = movenet(input_image)
    height, width, _ = np.squeeze(displayImage.numpy(), axis=0).shape

    keypointLocations = getKeypointsForDisplay(keypointScores, height, width)
    
    bodyPoints = {}
    for key in keypointDict:
        if len(keypointLocations) > keypointDict[key]:
            bodyPoints[key] = keypointLocations[keypointDict[key]]
    return bodyPoints