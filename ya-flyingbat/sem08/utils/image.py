import numpy
import cv2


def equalize_image_hist(img, bins=256):
    image = img.flatten()
    image_histogram, bins = numpy.histogram(image, bins, normed=True)
    cdf = image_histogram.cumsum()
    cdf = 255 * cdf / cdf[-1]
    image_equalized = numpy.interp(image, bins[:-1], cdf)
    return image_equalized.reshape(img.shape)


# noinspection PyUnresolvedReferences
def draw_rectangle(image, mask, min_radius=10, color=(0, 255, 0), width=2):
    _, contours, _ = cv2.findContours(mask, 1, 2)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > min_radius and h > min_radius:
            image = cv2.rectangle(image, (x, y), (x+w, y+h), color, width)

    return image


# noinspection PyUnresolvedReferences
def draw_circle(image, mask, min_radius=10, color=(0, 255, 0), width=2):
    _, contours, _ = cv2.findContours(mask, 1, 2)

    for contour in contours:
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)
        if radius > min_radius:
            image = cv2.circle(image, center, radius, color, width)

    return image


# noinspection PyUnresolvedReferences
def draw_ellipsis(image, mask, min_radius=10, color=(0, 255, 0), width=2):
    _, contours, _ = cv2.findContours(mask, 1, 2)

    for contour in contours:
        if len(contour) < 5:
            continue
        v_ellipsis = cv2.fitEllipse(contour)
        (xc, yc), (a, b), theta = v_ellipsis
        if a > min_radius and b >= min_radius:
            image = cv2.ellipse(image, v_ellipsis, color, width)

    return image


# noinspection PyUnresolvedReferences
def overlay(image, mask, color, alpha):
    ovl = cv2.merge([mask, mask, mask], 3)
    ones = numpy.ones(mask.shape)
    paint = cv2.merge([
        (ones * color[0]).astype(numpy.uint8),
        (ones * color[1]).astype(numpy.uint8),
        (ones * color[2]).astype(numpy.uint8)], 3)
    pos = ovl == 0
    neg = ovl != 0
    return (pos * image + neg * image * alpha + neg * paint * (1 - alpha)).astype(numpy.uint8)


# noinspection PyUnresolvedReferences
def highlight(
        image,
        heatmap,
        threshold=50,
        blur_kernel_size=(10, 10),
        fig_type="ellipsis",
        fig_min_size=10,
        fig_color=(0, 255, 0),
        fig_line_width=2,
        ovl_color=(255, 0, 0),
        ovl_alpha=0.50):
    draw = {"ellipsis": draw_ellipsis, "rectangle": draw_rectangle, "circle": draw_circle}[fig_type]

    gray_image = cv2.cvtColor(heatmap, cv2.COLOR_RGB2GRAY)

    if blur_kernel_size is not None:
        blurred = cv2.blur(gray_image, blur_kernel_size)
        # blurred = cv2.GaussianBlur(gray_image, blur_kernel_size, 0)
    else:
        blurred = gray_image

    ret, thresh = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)

    result = image

    if ovl_alpha is not None:
        result = overlay(result, thresh, color=ovl_color, alpha=ovl_alpha)

    result = draw(result, thresh, min_radius=fig_min_size, color=fig_color, width=fig_line_width)

    return result
