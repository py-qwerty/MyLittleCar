import cv2
import numpy as np
import glob


# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# 6x9 chess board, prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
object_point = np.zeros((5*8, 3), np.float32)
object_point[:, :2] = np.mgrid[0:8, 0:5].T.reshape(-1, 2)

# 3d point in real world space
object_points = []
# 2d points in image plane
image_points = []
h, w = 0, 0

images = glob.glob('chess_board/*.jpg')

for file_name in images:
    image = cv2.imread(file_name)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape[:2]

    # find chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (8, 5), None)

    # add object points, image points
    if ret:
        object_points.append(object_point)
        cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        image_points.append(corners)

        # draw and display the corners
        cv2.drawChessboardCorners(image, (8, 5), corners, ret)
        cv2.imshow('image', image)
        cv2.waitKey(500)

# calibration
retval, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(object_points, image_points, (w, h), None, None)

np.savez('camera_mtx.npz',mtx=mtx,dist=dist)
print('Matrix saved')

cv2.destroyAllWindows()
