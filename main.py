import pyautogui
import numpy as np
from PIL import Image
from io import BytesIO
import win32clipboard
import time

QUESTION_STR_LIMIT = 255
QUESTION_LINE_LIMIT = 40

# screen size dependent constants
MAIN_INP_POS = pyautogui.Point(1942, 1376)
MAIN_INP_HIGHER_POS = pyautogui.Point(2010, 1330)
CREATE_A_QUESTION_BTN = pyautogui.Point(2043, 1366)
CREATE_THE_QUESTION_BTN = pyautogui.Point(2043, 1366)
QUESTION_OPTION_HEIGHT = 40
QUESTION_LINE_HEIGHT = 10

SLEEP_DUR = 1
solution_start_height = -1


def get_question_size_offset(question_str):
    s = len(question_str)
    if s > QUESTION_LINE_HEIGHT * 3:
        return QUESTION_LINE_HEIGHT * 2

    return (s // QUESTION_LINE_LIMIT) * QUESTION_LINE_HEIGHT


def add_turkish_chars():
    char_mapping = {'ç': 220, 'Ç': 220, 'ğ': 219,
                    'Ğ': 219, 'ü': 221, 'Ü': 221, 'ı': 73, 'I': 73, 'ş': 186, 'Ş': 186, 'ö': 191, 'Ö': 191}

    for char in char_mapping:
        pyautogui._pyautogui_win.keyboardMapping[char] = char_mapping[char]


def start_quiz(quiz_name, quiz_expo):
    pyautogui.click(MAIN_INP_POS.x, MAIN_INP_POS.y)
    pyautogui.write('/newquiz')
    pyautogui.press('enter')
    pyautogui.write(quiz_name)
    pyautogui.press('enter')
    pyautogui.write(quiz_expo)
    pyautogui.press('enter')
    pyautogui.sleep(SLEEP_DUR)


def add_eba_question(question_str, h):
    if len(question_str) > QUESTION_STR_LIMIT:
        print('question str is more than LIMIT', QUESTION_STR_LIMIT)
        return

    pyautogui.click(CREATE_A_QUESTION_BTN.x, CREATE_A_QUESTION_BTN.y)
    pyautogui.sleep(SLEEP_DUR)
    pyautogui.write(question_str)
    pyautogui.press('enter')

    for ch in ['A', 'B', 'C', 'D', 'E']:
        pyautogui.write(ch)
        pyautogui.press('enter')

    click_2_show_answer()
    x,y,n = find_imgs(h)
    copy_solution_url(x,y)

    add_expo_to_the_question()

    click_2_choice(n)
    generate_the_question()


def set_question_img():
    arr, down = get_question_region(0, True)
    img2 = Image.fromarray(arr)
    img2.save('question.png')
    send_to_clipboard(img2)
    pyautogui.click(MAIN_INP_HIGHER_POS.x, MAIN_INP_HIGHER_POS.y)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.sleep(SLEEP_DUR)
    pyautogui.press('enter')
    pyautogui.sleep(SLEEP_DUR)
    return down


def get_question_region(h=0, is_get_down_idx=False):
    """ returns a np array which contains the bounding box on question screen """
    img = pyautogui.screenshot(region=(4, 170+h, 742, 1166-h))
    return get_bounding_box(img, 3, is_get_down_idx)


def send_to_clipboard(image):
    """ image must be a PIL image """
    output = BytesIO()
    image.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()


def get_bounding_box(img, white_margin=3, is_get_down_idx=False):
    """ img is a PIL image, return a np array which has croppoed all white rows and columns """
    arr = np.array(img)  # im2arr.shape: height x width x channel

    white_pix = np.array([255, 255, 255])
    x, y, _ = arr.shape
    up, down = 0, x

    for i in range(x):
        if np.all(arr[i, :] == white_pix):
            up = up + 1
        else:
            break
    for i in range(x):
        if np.all(arr[x-i-1, :] == white_pix):
            down = down - 1
        else:
            break
    up = up - white_margin
    if up < 0:
        up = 0
    down = down + white_margin
    if down > x-1:
        down = x-1

    left, right = 0, y

    for i in range(y):
        if np.all(arr[:, i] == white_pix):
            left = left + 1
        else:
            break
    for i in range(y):
        if np.all(arr[:, y-i-1] == white_pix):
            right = right - 1
        else:
            break

    left = left - white_margin
    if left < 0:
        left = 0
    right = right + white_margin
    if right > y-1:
        right = y-1

    if is_get_down_idx:
        return arr[up:down, left:right, :], down
    return arr[up:down, left:right, :]


def add_eba_quiz(quiz_name, quiz_expo):
    start_quiz(quiz_name, quiz_expo)
    down = set_question_img()
    add_eba_question('___________________', down)


def click_2_choice(c):
    """ choice c is zero indexed """
    x, y = 1771, 618 + c * 42
    pyautogui.click(x, y)


def add_expo_to_the_question():
    pyautogui.click(1787, 1085)
    pyautogui.hotkey('ctrl', 'v')


def generate_the_question():
    pyautogui.click(2053, 1207)
    pyautogui.sleep(SLEEP_DUR)


def click_2_show_answer():
    pyautogui.click(785, 1367)
    pyautogui.sleep(SLEEP_DUR)


def copy_solution_url(x,y):
    # clear dev tools network tab
    pyautogui.click(1089, 153)
    pyautogui.sleep(SLEEP_DUR)

    # click to "watch solution"
    pyautogui.click(x, y)
    pyautogui.sleep(SLEEP_DUR)

    # click to HTTP request
    pyautogui.click(1079, 400, button='right')
    pyautogui.sleep(SLEEP_DUR)

    # click to HTTP request > copy
    pyautogui.click(1167, 506)
    pyautogui.sleep(SLEEP_DUR)

    # click to HTTP request > copy > link address
    pyautogui.click(1400, 510)
    pyautogui.sleep(SLEEP_DUR)


def template_matching(img:np.array, tmp:Image):
    """ img is the big image, tmp is the template image. Both
    If founded return x,y coordinates of the center of tmp inside img, otherwise return -1,-1"""
    tmp = get_bounding_box(tmp, 0)
    m, n, _ = img.shape
    m2, n2, _ = tmp.shape

    # search from bottom
    for i in reversed(range(m-m2)):
        for j in range(n-n2):
            if np.allclose(img[i:i+m2, j:j+n2], tmp, rtol=0, atol=3):
            # if np.all(img[i:i+m2, j:j+n2] == tmp):
                return (i + m2//2), (j + n2//2)

    return -1, -1


def find_imgs(h):
    """ returns x,y,n. x,y are coordinates of 'watch solution button', n is 0 based index of right choice """
    screen = get_question_region(h)
    Image.fromarray(screen).save('answer.png')
    t1 = time.time()
    n = find_idx_of_right_choice(screen)
    print('finding index of right choice in ', (time.time() - t1))

    tmp = Image.open('img/watch_solution.png').convert('RGB')
    t1 = time.time()
    x,y = template_matching(screen, tmp)
    print('finding solution image in ', (time.time() - t1), ' x,y= ', x,y)
    y = y + h + 170

    return x,y,n


def find_idx_of_right_choice(screen):
    idx = 0
    for ch in ['A', 'B', 'C', 'D', 'E']:
        img = Image.open('img/choice/' + ch + '.png').convert('RGB')
        img.load()
        x, y = template_matching(screen, img)
        if x > -1 and y > -1:
            return idx
        idx = idx + 1
    print('right choice not FOUND')
    return -1


def print_mouse_position():
    prev_pos = pyautogui.Point(0, 0)
    curr_pos = pyautogui.Point(0, 0)
    while True:
        prev_pos = curr_pos
        curr_pos = pyautogui.position()

        if curr_pos != prev_pos:
            print('position: ', curr_pos)


# add_question()

# #ikinci şık doğruysa
# pyautogui.click(1290, 483)

# #üçüncü şık doğruysa
# pyautogui.click(1290, 526)

# #dörcüncü şık doğruysa
# pyautogui.click(1290, 570)
# #beşinci şık doğruysa
# pyautogui.click(1290, 605)

# SORUYU OLUŞTUR
# pyautogui.click(1570, 1000)


# pyautogui.click(1580, 1010)


# print_mouse_position()
add_turkish_chars()
add_eba_quiz('1. TYT Denemesi - Türkçe', 'https://akademikdestek.eba.gov.tr/')

# find_imgs(0,0)
# start_quiz('RG9uJ3QgZm9yZ2V0IHRoYXQgz4AgPSAzLjE0ICYgZG9lc24ndCBlcXVhbCAzLg==', 'expo')
