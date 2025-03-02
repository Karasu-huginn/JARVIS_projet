import re
import configparser
from PIL import Image

class SizeError(Exception):
    pass

def check_for_word(text, word):
    text = text.split()
    for element in text:
        if element.lower() == word:
            return True
    return False

def treat_ai_text(answer):
    answer["talk"] = re.sub('[*]','',answer["talk"])
    return answer

def change_voice():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    param = config['VOICE']['selected_voice']
    if param == '1':
        config['VOICE'] = {'selected_voice':'0'}
    if param == '0':
        config['VOICE'] = {'selected_voice':'1'}
    with open('settings.ini','w') as file:
        config.write(file)

def convert_list_to_str(elements):
    string = ""
    for element in elements:
        string += element + ","
    string = string[:-1]
    return string

def convert_time(time):
    seconds = time//1000
    minutes = seconds//60
    seconds = seconds%60
    hours = minutes//60
    minutes = minutes%60
    return f"{hours}h {minutes}min {seconds}s"

def convert_to_jpeg(img_name):
    img = Image.open(f"img/{img_name}")
    rgb_im = img.convert('RGB')
    img_name = img_name.split(".")[0]
    rgb_im.save(f'img/{img_name}.jpeg')