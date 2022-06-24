import PySimpleGUI as sg
from windowOne import WinOne
from windowTwo import WinTwo
import datetime
from urls import urls
from requests import get
from requests import post

'''Переменная для Теста удаления объекта БД'''
kod = ['del']
keys = ['kod', 'nameAlloy']

'''Словарь сасусов для Class WinOne'''
status ={'Add': 'add', 'Read':'read'}

''' Функции :'''

'''Функция получает текущую дату'''
def dt():
    now = datetime.datetime.now()  # Получаем текущую дату
    now = now.strftime('%d.%m.%Y')
    return now

'''Функция ничего не делает нужна для теста GitHub'''
def gitTest():
    pass


'''Функция обновления списка марок сплавов'''
def refreshAlloyList(urls):
    try:
        r = get(urls['alloy_read'])
        data = r.json()
        i = data['i']
        listAlloy = i[::3]
    except:
        listAlloy = ['Нет соединения с сервером']
        return listAlloy
    return listAlloy

''' Функция счетчик кол-ва марок'''
def countAlloys(arr):
    #print(arr)
    if arr == ['Нет соединения с сервером']:
        count = '0'
        return count
    else:
        count = str(len(arr))
    return count

'''Цвет темы'''
sg.theme('LightPurple')

'''Основной layout'''
layout = [  [sg.Text('Дата:'), sg.Text(dt())],

            [sg.Frame('', [
                           [sg.Listbox(values=refreshAlloyList(urls), size=(55, len(refreshAlloyList(urls))), key='-alloy-')]
                          ])],
            [sg.Text('Всего в базе ' + countAlloys(refreshAlloyList(urls)) + ' марок сплавов', key='-info-'), sg.Text('', key='-infodel-', size=(24, 1))],
            [sg.Button('Выход', key='-exit-'), sg.Button('Добавить марку', key='-win1-'),
             sg.Button('Параметры марки', key='-win2-'), sg.Button('Удаление марки', key='-del-')]]

'''Запуск основногоо окна'''

'''Провкрка активности сервера'''
if refreshAlloyList(urls) == ['Нет соединения с сервером']:
    serverFlag = False
    #print('Флаг активности сервера в False')
else:
    serverFlag = True
    #print('Флаг активности сервера в True')

windowMain = sg.Window('База данных марок сплавов', layout)

''' Переменные активности окон'''
windowOne_active = False
windowTwo_active = False

'''Основной цикл'''
while True:
    event, values = windowMain.Read()
    if event in (None, '-exit-'):
        break

    '''Удаление марки'''
    if event == '-del-':
       try:
           if refreshAlloyList(urls)==['Нет соединения с сервером']:
                windowMain['-infodel-'].update('Нет соединения с сервером', text_color='red')
                windowMain['-info-'].update('Марки сплавов недоступны')
           else:
                if serverFlag == True:
                    vallog = values['-alloy-']
                    vallog = kod + vallog
                    #print(vallog)
                    data = dict([(keys[0], vallog[0]), (keys[1], vallog[1])])
                    #print(data)
                    r = post(urls['alloy_input'], data)
                    message = r.json()
                    resMessage = message['numRecord']
                    if resMessage == 'del_ok':
                        windowMain.FindElement('-alloy-').Update(refreshAlloyList(urls))
                        windowMain.FindElement('-info-').Update(
                            'Всего в базе ' + str(len(refreshAlloyList(urls))) + ' марок сплавов')
                        windowMain['-infodel-'].update('')
       except:
        #print('Марка не выбрана')
        windowMain['-infodel-'].update('Марка не выбрана', text_color='red')

    '''Окно добавления марок '''
    if event == '-win1-'  and not windowOne_active:
        if serverFlag == True:
            windowOne_active = True
            windowMain.Hide()
            #print('Первое окно Старт!')
            win1 =WinOne(status['Add'])
            win1.openwin(windowMain)
            windowOne_active = False
            windowMain.FindElement('-alloy-').Update(refreshAlloyList(urls))
            windowMain.FindElement('-info-').Update('Всего в базе ' + str(len(refreshAlloyList(urls))) + ' марок сплавов')




    '''Параметры Марки'''
    if event == '-win2-' and not windowTwo_active :

        if serverFlag == True:
            vallog = values['-alloy-']
            #print(vallog)
            if vallog != []:
                windowTwo_active = True
                windowMain.Hide()
                #print('Второе окно Старт!')
                win2 =WinTwo(status['Read'], vallog[0])
                win2.openwin(windowMain)
                windowTwo_active = False
            else:
                #print('Марка не выбрана')
                windowMain['-infodel-'].update('Марка не выбрана', text_color='red')

windowMain.close()
