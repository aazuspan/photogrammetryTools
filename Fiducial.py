import cv2
import matplotlib.pyplot as plt
import numpy as np


class Fiducial:
    def __init__(self, img):
        self.img = img
        self._filtered = None
        self._coordinates = None

    def preview(self, size=(4, 4), cmap="gray", filtered=False):
        _, ax = plt.subplots(figsize=size)

        if filtered and self._filtered is not None:
            img = self._filtered
        else:
            img = self.img

        ax.imshow(img, cmap=cmap)

        if self._coordinates:
            ax.plot(self._coordinates[0], self._coordinates[1],
                    marker="+", color="yellow", markersize=20)

    def _filter(self, kernel_size, iterations, threshold, block_size):
        """
        Use morphological opening and adaptive thresholding to filter an image 
        of a fiducial to prepare for corner detection.
        """
        kernel = np.ones((kernel_size, kernel_size), np.uint8)

        img = cv2.normalize(self.img, None, alpha=0, beta=255,
                            norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

        filtered = cv2.morphologyEx(
            img, cv2.MORPH_OPEN, kernel, iterations=iterations)

        if threshold:
            filtered = cv2.adaptiveThreshold(filtered, filtered.max(
            ), cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, 0)

        return filtered

    def _calculate_coordinates(self, kernel_size, iterations, threshold, block_size):
        """
        Perform image filtering and corner finding to locate the fiducial coordinates.
        """
        self._filtered = self._filter(
            kernel_size, iterations, threshold, block_size)

        self._coordinates = self._locate_corner()

        return self.coordinates

    def _locate_corner(self):
        """
        Take a filtered image of a fiducial and find the best corner feature. 
        Return it's pixel coordinates.
        """
        corner = cv2.goodFeaturesToTrack(
            self._filtered, maxCorners=1, qualityLevel=0.1, minDistance=0)

        return (corner[0][0][0], corner[0][0][1])

    @property
    def coordinates(self):
        # TODO: Convert the coordinates from relative coordinates to the global image coordinates
        return self._coordinates
