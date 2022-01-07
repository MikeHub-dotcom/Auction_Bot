# IMPORTANT: Wow-client needs to be in a resolution of 1280x800!

import cv2
import numpy as np
import os
from time import time
from window_capture import WindowCapture, debug_capture
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

# initialize the WindowCapture class
wow_client = WindowCapture('World of Warcraft')


# debug_capture(wow_client)

def transform_pixel_coords(fix_point, pos):
    # For the auction house frame the fixpoint is 'ah_upper_left'
    return (pos[0] + fix_point[0], pos[1] + fix_point[1])


def match_template(img, template, debug=False):
    '''methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR,
               cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]'''

    method = cv2.TM_CCOEFF
    img2 = img.copy()

    result = cv2.matchTemplate(img2, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        location = min_loc
    else:
        location = max_loc

    if debug:
        temp_h, temp_w = template.shape
        bottom_right = (location[0] + temp_w, location[1] + temp_h)
        cv2.rectangle(img2, location, bottom_right, 255, 1)

        cv2.imshow('Match', img2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return location


def init_ah_window(window_capture, debug=False):
    # Zur Klasse umwandeln!
    screenshot = cv2.cvtColor(window_capture.get_screenshot(), cv2.COLOR_BGR2GRAY)
    screenshot2 = screenshot.copy()
    screen_h, screen_w = screenshot.shape

    ah_fix_point_location = match_template(screenshot, cv2.imread('Templates/init_ah_window_1280_800.JPG', 0))

    # Defined upper left corner and lower right corner of the auction house frame
    ah_upper_left = (ah_fix_point_location[0] - 285, ah_fix_point_location[1] - 2)
    ah_lower_right = (ah_fix_point_location[0] + 530, ah_fix_point_location[1] + 418)

    # Crop the original screenshot to the size of the auction house frame
    cropped_ah_frame = screenshot[ah_upper_left[1]:ah_lower_right[1], ah_upper_left[0]:ah_lower_right[0]]

    # Get search button coordinats
    search_pos = match_template(cropped_ah_frame, cv2.imread('Templates/suchen_1280_800.JPG', 0))
    search_pos = (search_pos[0] + 40, search_pos[1] + 10)

    # Get reset button coordiantes
    reset_pos = match_template(cropped_ah_frame, cv2.imread('Templates/ruecksetzen_1280_800.JPG', 0))
    reset_pos = (reset_pos[0] + 50, reset_pos[1] + 10)

    # Get "next" button coordinates
    next_pos = match_template(cropped_ah_frame, cv2.imread('Templates/weiter_1280_800.JPG', 0))
    next_pos = (next_pos[0] + 50, next_pos[1] + 15)

    # Get "Handwerkswaren" button coordinates
    handwerkswaren_pos = match_template(cropped_ah_frame, cv2.imread('Templates/handwerkswaren_1280_800.JPG', 0))
    handwerkswaren_pos = (handwerkswaren_pos[0] + 50, handwerkswaren_pos[1] + 5)

    # Crop the auction house frame to the size of the item frame
    cropped_item_frame = cropped_ah_frame[95:385, 220:780]

    if debug:
        # cv2.circle(cropped_ah_frame, (next_pos[0] + 50, next_pos[1] + 15), 1, 255, -1)
        cv2.imshow("cropped", cropped_item_frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        cv2.imshow("cropped", cropped_ah_frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        cv2.rectangle(screenshot2, ah_upper_left, ah_lower_right, 255, 1)
        cv2.imshow('Match', screenshot2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    print("Auctionhouse window initialized.")
    return transform_pixel_coords(ah_upper_left, search_pos), transform_pixel_coords(ah_upper_left,
                                                                                     reset_pos), transform_pixel_coords(
        ah_upper_left, next_pos), transform_pixel_coords(ah_upper_left, handwerkswaren_pos), cropped_item_frame


def get_items(item_frame, debug=True):
    step_size = 37
    for i in range(8):
        single_item_frame = item_frame[0+step_size*i:30+step_size*i, 0:]
        item_name_frame = single_item_frame[:, :180]
        seller_name_frame = single_item_frame[:, 310:385]
        bid_price_frame = single_item_frame[:17, 435:]
        sell_price_frame = single_item_frame[17:, 435:]

        if debug:
            # cv2.circle(cropped_ah_frame, (next_pos[0] + 50, next_pos[1] + 15), 1, 255, -1)
            print(pytesseract.image_to_string(item_name_frame, lang='deu'))
            cv2.imshow("cropped", sell_price_frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()



    return


a, b, c, d, e = init_ah_window(wow_client)
get_items(e)

print('Done.')
