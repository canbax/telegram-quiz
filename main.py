import pyautogui

# constant related with telegram
QUESTION_STR_LIMIT = 255
QUESTION_LINE_LIMIT = 40

# screen size dependent constants
MAIN_INP_POS = pyautogui.Point(1515, 1018)
CREATE_QUESTION_BTN = pyautogui.Point(1576, 796)
QUESTION_OPTION_HEIGHT = 30
QUESTION_LINE_HEIGHT = 10


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
    pyautogui.sleep(3)


def add_question(question_str):
    if len(question_str):
        print('question str is more than LIMIT', QUESTION_STR_LIMIT)
        return

    # BURADAN İTİBAREN REPEAT ETCEK DÖNGÜYE SOK
    pyautogui.click(MAIN_INP_POS.x, MAIN_INP_POS.y)
    pyautogui.write(question_str)
    pyautogui.press('enter')

    pyautogui.write(' 1 !!!', interval=0.2)
    pyautogui.press('enter')
    pyautogui.write(' 2 !!!', interval=0.2)
    pyautogui.press('enter')
    pyautogui.write(' 3 !!!', interval=0.2)
    pyautogui.press('enter')
    pyautogui.write(' 4 !!!', interval=0.2)
    pyautogui.press('enter')
    pyautogui.write(' 5 !!!', interval=0.2)

    # #birinci şık doğruysa
    pyautogui.click(1290, 440)

    # SORUYU OLUŞTUR
    pyautogui.click(1570, 1000)


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


print_mouse_position()
# add_turkish_chars()
# start_quiz()
