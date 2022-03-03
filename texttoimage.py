from PIL import Image, ImageDraw
import PySimpleGUI as sg
import random

def key(a):
    sr = 0
    for i in range(len(a)):
        sr += ord(a[i])
    sr = sr // len(a)
    return sr

sg.theme('DarkBlack')

layout = [
    [sg.Text('Фото'), sg.InputText(), sg.FileBrowse("Выбор фото"), sg.Checkbox('Шифрование')],
    [sg.Text('Ключ'), sg.InputText()],
    [sg.Text('Текст')],
    [sg.Multiline(size=(88, 20))],
    [sg.Output(size=(88, 20))],
    [sg.Text('Имя зашифрованного файла'), sg.InputText("result"),sg.FileBrowse("Выбор пути для сохранения")],
    [sg.Button("Текст в фото"), sg.Button("Текст из фото"), sg.Cancel()]
]

window = sg.Window('Текст в фото', layout)

while True:
    event, values = window.read()
    if event in (None, 'Exit', 'Cancel'):
        break
    elif event == "Текст в фото":
        if values[0]:
            file = Image.open(values[0])
            isitago = 1
            if not file and file is not None:
                print('Error: File 1 path not valid.')
                isitago = 0
            elif isitago == 1:
                print("Изображение загружено")
                draw = ImageDraw.Draw(file)
                pix = file.load()
                width = file.size[0]
                height = file.size[1]
                sum = width * height
                text = values[3]
                text_key = [0]
                for i in range(len(text)):
                    text_key.append(ord(text[i]))
                if len(text_key) > sum:
                    print("Изображение слишком маленькое")
                    break
                text_key.append(0)
                print(text_key)
                if values[2]:
                    random.seed(key(values[2]))

                    pix_state = [0]
                    for i in range(sum-1):
                        pix_state.append(0)

                    for i in range(1, len(text_key)):
                        pix_val = random.randint(0, sum)
                        while pix_state[pix_val] == 1:
                            pix_val = random.randint(0, sum)

                        x = pix_val % width
                        y = (pix_val - x) // width
                        if text_key[i] > 1000:
                            text_key[i] -= 890

                        first = text_key[i] >> 5
                        second = (text_key[i] >> 3) & 3
                        th = text_key[i] & 7
                        r = ((pix[x, y][0] >> 3) << 3) | first
                        g = ((pix[x, y][1] >> 2) << 2) | second
                        b = ((pix[x, y][2] >> 3) << 3) | th
                        draw.point((x, y), (r, g, b))
                    print("Image saved with text with key:", values[2])
                    file.save(values[4]+".png")
                    print("Saved")
                else:
                    for i in range(1, len(text_key)):
                        pix_val = i-1
                        x = pix_val % width
                        y = (pix_val - x) % width

                        if text_key[i] > 1000:
                            text_key[i] -= 890
                        first = text_key[i] >> 5
                        second = (text_key[i] >> 3) & 3
                        th = text_key[i] & 7

                        r = ((pix[x, y][0] >> 3) << 3) | first
                        g = ((pix[x, y][1] >> 2) << 2) | second
                        b = ((pix[x, y][2] >> 3) << 3) | th
                        draw.point((x, y), (r, g, b))
                    print("Image saved with text without key")
                    file.save(values[4]+".png")
                    print("Saved")
        else:
            print('Выберите файл')
    elif event == "Текст из фото":
        if values[0]:
            file = Image.open(values[0])
            isitago = 1
            if not file and file is not None:
                print('Error: File 1 path not valid.')
                isitago = 0
            elif isitago == 1:
                alp = "qwertyuiop[]asdfghjklzxcvbnm,./1234567890()-+=_йцукенгшщзхъфывапролджэячсмитьбю"
                print("Изображение загружено")
                draw = ImageDraw.Draw(file)
                pix = file.load()
                width = file.size[0]
                height = file.size[1]
                sum = width*height
                text_sh = ""
                if values[2]:
                    random.seed(key(values[2]))

                    flag = True
                    pix_state = [0]

                    for i in range(sum-1):
                        pix_state.append(0)

                    while flag:
                        pix_val = random.randint(0, sum)

                        while pix_state[pix_val] == 1:
                            pix_val = random.randint(0, sum)

                        x = pix_val % width
                        y = (pix_val - x) // width

                        first = (pix[x, y][0] & 7) << 5
                        sc = (pix[x, y][1] & 3) << 3
                        th = pix[x, y][2] & 7
                        ch = first + sc + th
                        if ch > 130:
                            ch += 890
                        if ch == 0:
                            flag = False
                        else:
                            text_sh += chr(ch)
                    print("Текст из фотографии: ",text_sh)
                else:
                    flag = True
                    i = 0
                    while flag:
                        pix_val = i

                        x = pix_val % width
                        y = (pix_val - x) // width

                        first = (pix[x, y][0] & 7) << 5
                        sc = (pix[x, y][1] & 3) << 3
                        th = pix[x, y][2] & 7
                        ch = first + sc + th
                        if ch > 130:
                            ch += 890
                        if ch == 0:
                            flag = False
                        else:
                            text_sh += chr(ch)
                    print("Текст из фотографии: ",text_sh)
        else:
            print('Выберите файл')
