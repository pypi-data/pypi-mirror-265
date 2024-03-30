import numpy as np
from optivision.common import check_image


def gamma_transform(im, c=1, gamma=1):
    """Applies the gamma transformation to the input image. Also known as Power Law Transformation.

    Formula:
        s = c * r^gamma

    Args:
        image (np.ndarray): Input image to be transformed
        c (int, optional): Constant value. Defaults to 1.
        gamma (int, optional): Power value. Defaults to 1.

    Returns:
        np.ndarray: Transformed image
    """
    check_image(im)

    image = im.copy()
    EPSILON = 1e-5
    norm_img = (image / 255.0) + EPSILON  # Adding epsilon to avoid division by zero
    enhanced_img = c * np.power(norm_img, gamma)
    # Need to clip the values to avoid overflow
    enhanced_img = np.clip(enhanced_img, 0, 1)
    enhanced_img = (enhanced_img * 255.0).astype(np.uint8)

    return enhanced_img
