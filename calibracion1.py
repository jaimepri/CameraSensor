import cv2
import glob
import copy

import numpy as np
import cv2
from picamera2 import Picamera2


def get_chessboard_points(chessboard_shape, dx, dy):
    x, y = chessboard_shape
    lista = []

    for j in range(y):
        lista.extend([[i*dx, j*dy, 0] for i in range(x)])
    return np.array(lista)


PICAM = Picamera2()
PICAM.preview_configuration.main.size=(640, 360)
PICAM.preview_configuration.main.format="RGB888"
PICAM.preview_configuration.align()
PICAM.configure("preview")
PICAM.start()

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01)

CHESS_DIM = [7, 7]
DX = 20
DY = 20
MIN_IMAGES = 20

corners_refined = []
tmp_images = []
while len(corners_refined) <= MIN_IMAGES:
    image = PICAM.capture_array()
    ack, tmp_corner = cv2.findChessboardCorners(image, patternSize=CHESS_DIM)
    if ack:
        print(len(corners_refined))
        tmp_images.append(image)
        im_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        corners_refined.append(cv2.cornerSubPix(im_gray, tmp_corner, CHESS_DIM, (-1, -1), criteria))
        patt_image = cv2.drawChessboardCorners(
                                        image, patternSize=CHESS_DIM,
                                        corners=corners_refined[-1], patternWasFound=1
                                        )
        cv2.imwrite(f'imagenes_calibracion/calibracion_numero_{len(corners_refined)}.png', patt_image)
        cv2.imshow("picam", patt_image)

    else:
        cv2.imshow("picam", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



real_points = get_chessboard_points(CHESS_DIM, DX, DY)
object_points = np.asarray([real_points for i in range(len(corners_refined))], dtype=np.float32)
image_points = np.asarray(corners_refined, dtype=np.float32)


rms, intrinsics, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(object_points, image_points, image.shape[:2], None, None)

extrinsics = list(map(lambda rvec, tvec: np.hstack((cv2.Rodrigues(rvec)[0], tvec)), rvecs, tvecs))
# Save the calibration file
np.savez('calibracion', intrinsic=intrinsics, extrinsic=extrinsics)

# Lets print some outputs
print("Corners standard intrinsics:\n",intrinsics)
print("Corners standard dist_coefs:\n", dist_coeffs)
print("root mean square reprojection error:\n", rms)