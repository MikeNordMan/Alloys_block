import PySimpleGUI as sg
from requests import post
from urls import urls


class WinOne():
    '''Конструктор Class'''
    def __init__(self, status):
        self.status = status

    '''Переменные класса'''
    kod = ['find']
    kod1 = ['update']
    keys = ['nameAlloy', 'discript', 'tu_Gost']
    keysForServer = ['kod', 'nameAlloy']
    lenRasdelLine = 50  # Кол-во символов

    '''Основная функция класса'''
    def openwin(self, wind):

        if self.status == 'add':
            '''Цвет темы'''
            sg.theme('LightPurple')
            '''Запуск основногоо окна'''
            window = sg.Window('Первое окно', self.layout())
            self.controlAdd(window, wind)

        if self.status == 'read':
           #print('Второе окно')
           '''Цвет темы'''
           sg.theme('LightPurple')
           '''Запуск основногоо окна'''
           window = sg.Window('Первое окно', self.layoutTwo())
           self.controlAdd(window, wind)

    '''Функция закрытия текущего окна и открытия главного'''
    def colseWin(self, wind,window):
        window.close()
        wind.UnHide()
        #print('Работает Закрытие Первого окна')

    '''Функция Очистки полей'''
    def cleanFild(self, window):
        for key in self.keys:
            window[key].update('')

    '''Функция проверяет заполнение всех полей и ставит название марки в заглавный вид'''
    def dataUp(self, window, values):
        flag = 1
        for key in self.keys:
            if values[key] == '':
                window['-info-'].update('Заполните все поля!!!', text_color='red')
                flag = 0

        if flag == 1:
            textUp = values[self.keys[0]]
            textUp = textUp.upper()
            values.update({self.keys[0]: textUp})
            #print(values)
            return values

    '''Функция записывает данные в БД'''
    def sendData(self, url, data, window):
        try:
            r = post(url, data)
            message = r.json()
            resMessage = message['numRecord']
            if resMessage != '':
                if resMessage == 'Есть такой элемент':
                    window['-info-'].update('Есть такой элемент', text_color='red')
                else:
                    window['-info-'].update('Запись успешно занесена в БД', text_color='green')
                    self.cleanFild(window)
            return resMessage
        except:
            window['-info-'].update('Нет соединения с БД')


    def layout(self):
        layout = [[sg.Text('Наименование Марки')],
                  [sg.InputText(key=self.keys[0], size=(50, 1))],
                  [sg.Text('Описание Марки')],
                  [sg.InputText(key=self.keys[1], size=(50, 50))],
                  [sg.Text('Гост или ТУ')],
                  [sg.InputText(key=self.keys[2], size=(50, 1))],
                  [sg.Text('_' * self.lenRasdelLine)],
                  [sg.Text('', key='-info-', text_color='red', size=(50, 1))],
                  [sg.Button('Добавить запись', key='-add-'), sg.Button('Очистить поля', key='-clean-'),
                   sg.Button('Выход', key='-exit-')]
                  ]
        return layout






    '''Функция управления окном в статусе Add'''

    def controlAdd(self, window, wind):
        while True:
            event, values = window.Read()
            if event in (None, '-exit-'):
                if wind != 'test':
                    self.colseWin(wind, window)
                break

            ''' Очисщаем поля'''
            if event == '-clean-':
                self.cleanFild(window)
                #print('Очистка Полей')

            ''' Добавляем запись'''
            if event == '-add-':
                values['kod'] = 'add'
                #print(values)
                newData = self.dataUp(window, values)
                # print(newData)
                if newData != None:
                    self.sendData(urls['alloy_input'], newData, window)

            ''' Корекция записи'''
            if event == '-up-':
                res = self.korect(values)
                if res=='ok update':
                    window['-info-'].update('Корекция прошла успешно ', text_color='green')
                elif res == 'Нет соединения с сервером!':
                    window['-info-'].update(res, text_color='red')
                elif res == 'Заполните все поля !':
                    window['-info-'].update(res, text_color='red')
                else:
                    window['-info-'].update('Корекция не прошла !', text_color='red')


