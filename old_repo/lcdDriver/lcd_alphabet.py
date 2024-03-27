# lib: adafruit-blinka, adafruit-circuitpython-charlcd
from subprocess import Popen, PIPE
from time import sleep, perf_counter
from datetime import datetime
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

def init(sensibilità = 4):
    lcd_columns = 16
    lcd_rows = 2
    lcd_rs = digitalio.DigitalInOut(board.D25)
    lcd_en = digitalio.DigitalInOut(board.D24)
    lcd_d4 = digitalio.DigitalInOut(board.D23)
    lcd_d5 = digitalio.DigitalInOut(board.D17)
    lcd_d6 = digitalio.DigitalInOut(board.D18)
    lcd_d7 = digitalio.DigitalInOut(board.D22)
    global lcd, buffer_line_1, charCount, prevChar, sens
    lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                        lcd_d7, lcd_columns, lcd_rows)
    lcd.clear()
    lcd.cursor = False
    buffer_line_1 = ""
    charCount = 0
    prevChar = ""
    # sensibilità: ogni quanti caratteri consecutivi ricevuti lo considero come confermato; 1 sensibilità massima - 10 sensibilità minima
    sens = sensibilità



def __UpdateTopScreen():
    global lcd_line_1
    lcd.cursor_position(0,0)
    lcd.message = lcd_line_1[:15] + " " * 16

def __UpdateStarsScreen(numStars):
    if 0 <= numStars <= sens:
        lcd.cursor_position(0,1)
        lcd.message = '*' * numStars + '-' * (sens - numStars)

def __UpdateLetterScreen(char):
    lcd.cursor_position(15,1)
    if char == "space":
        lcd.message = "S"
    elif len(char) == 1:
        lcd.message = char
    elif char == "del":
        lcd.message = "<"
    elif char == "reset":
        lcd.message = "X"
    elif char == "NOINPUT":
        lcd.message = " "


def __NewChar(input_str):
    global buffer_line_1, lcd_line_1
    if input_str == "reset":
        buffer_line_1 = ""
    elif input_str == "del":
        buffer_line_1 = buffer_line_1[:-1]  
    elif len(input_str) == 1 and (input_str.isalpha()):
        buffer_line_1 += input_str
    elif input_str == "space":
        buffer_line_1 += " "
    lcd_line_1 = buffer_line_1[-15:] + "_"
    __UpdateTopScreen()


def CharRaised(char):
    global charCount, prevChar, lcd_line_2, sens
    if char == "NOINPUT":
        charCount = 0
        __UpdateLetterScreen(char)
    elif prevChar != char:
        charCount = 0
        __UpdateLetterScreen(char)
    else:
        charCount+=1
        if charCount == sens + 1:
            charCount = 0
            print("DEBUG: new char: '" + char + "'")
            __NewChar(char)
            __UpdateLetterScreen("NOINPUT")
    prevChar = char
    __UpdateStarsScreen(charCount)

def SetDisplay(line_1, line_2):
    lcd.clear()
    lcd.cursor_position(0,0)
    if len(line_1) < 16 and len(line_2) < 16:
        lcd.message = line_1 + "\n" + line_2


# DEBUG CODE
# dict = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm','n','o','p','q','r','s','t','u','v','w','x','y','z', 'space', 'del', 'reset']
# charCount = 0
# prevChar = ""
# lcd_line_1 = ""
# lcd_line_2 = ""
# for x in "ciao come va":
#     for _ in range(9):
#         charRaised(x)
#         sleep(0.2)
#     for _ in range(random.randint(0,3)):
#             charRaised(dict[random.randint(0,27)])
#             sleep(0.2)
#     sleep(0.2)
# charRaised("NOINPUT")
