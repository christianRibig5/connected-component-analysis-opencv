# import the neccessary package
import argparse
import cv2 as cv

# construct the argument parser and the arguments

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True, help="path to input image")
ap.add_argument("-c", "--connectivity",type=int, default=4,help="connectivity for connected component analysis")
args = vars(ap.parse_args())

# load the input image from disk, convert it to grayscale, andd threshhold it

image = cv.imread(args["image"])
gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
thresh = cv.threshold(gray, 0, 225, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]

# apply connected component analysis to the thresholded image

output = cv.connectedComponentsWithStats(
    thresh, args["connectivity"], cv.CV_32S)
(numLabels, labels, stats, centroids)=output

# loop over the number of unique connected components labels

for i in range(0, numLabels):
    # if this is the first component then we examine the
	# *background* (typically we would just ignore this
	# component in our loop)
    if i == 0:
        text = "examining component {}/{} (background)".format(
			i + 1, numLabels)

    # otherwise, we are examing the actual connected component

    else:
        text = "examining component {}/{}".format( i + 1, numLabels)

    # print a status message update for the current connected
	# component
    print("[INFO] {}".format(text))

# extract the connected component statistics and centroid for
# the current label

x = stats[i, cv.CC_STAT_LEFT]
y = stats[i, cv.CC_STAT_TOP]
w = stats[i, cv.CC_STAT_WIDTH]
h = stats[i, cv.CC_STAT_HEIGHT]
area = stats[i, cv.CC_STAT_AREA]
(cX, cY) = centroids[i]

# clone our original image (so we can draw on it) and then draw
# a bounding box surrounding the connected component along with
# a circle corresponding to the centroid

output = image.copy()
cv.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 3)
cv.circle(output, (int(cX), int(cY)), 4, (0, 0, 255), -1)

# construct a mask for the current connected component by
# finding a pixels in the labels array that have the current
# connected component ID

componentMask = (labels == i).astype("uint8") * 255

# show our output image and connected component mask

cv.imshow("Output", output)
cv.imshow("Connected Component", componentMask)
cv.waitKey(0)