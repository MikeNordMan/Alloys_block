from windowOne import WinOne
import PySimpleGUI as sg
from requests import post
from urls import urls

class WinTwo(WinOne):
    def __init__(self, status, data):
        super().__init__(status=status)
        self.data = data

    def layoutTwo(self):
        layout = [[sg.Text('Наименование Марки')],
                  [sg.InputText(default_text=self.inArr(self.findAlloy())[0], disabled=True, key=self.keys[0], size=(50, 1))],
                  [sg.Text('Описание Марки')],
                  [sg.InputText(default_text=self.inArr(self.findAlloy())[1], key=self.keys[1], size=(50, 50))],
                  [sg.Text('Гост или ТУ')],
                  [sg.InputText(default_text=self.inArr(self.findAlloy())[2], key=self.keys[2], size=(50, 1))],
                  [sg.Text('_' * self.lenRasdelLine)],
                  [sg.Text(self.missServer(self.findAlloy()), key='-info-', text_color='red', size=(50, 1))],
                  [sg.Button('Коррекция записи', key='-up-'), sg.Button('Очистить поля', key='-clean-'),
                   sg.Button('Выход', key='-exit-')]
                  ]
        return layout

    '''Функция проверки отключения сервера'''
    def missServer(self, mass):
        if mass ==['-','-','-']:
            a = 'Нет соединения с сервером'
            return a
        else:
            a = ''
            return a
    
    '''Функция заполнения полей при сосоздании Layout'''
    def inArr(self, data):
        a = data
        return a

    '''Функция Очистки полей (переопределение родительской функции)'''
    def cleanFild(self, window):
        window[self.keys[1]].update('')
        window[self.keys[2]].update('')

    ''' Функция запроса данных с сервера'''
    def findAlloy(self):
        self.kod.append(self.data)
        #print('Проверка переменной kod:')
        #print(self.kod[0])
        #print(self.kod[1])
        tt = dict([(self.keysForServer[0], self.kod[0]), (self.keysForServer[1], self.kod[1])])
        #print('Отправка сообщения на сервер:')
        #print(tt)
        try:
            r = post(urls['alloy_read'], tt)
            message = r.json()
            resMessage = message['numRecord']
            #print(resMessage)
            newData = resMessage
            return newData
        except:
            newData = ['-', '-', '-']
            return newData



    ''' Функция коррекции записи'''
    def korect(self, values):
        #print('Режим Коррекции запущен')
        #print(values)
        values.update({self.keysForServer[0]: self.kod1[0]}) # Таким образом можно пополнить словарь
        #print(values)
        for v in values:
            if values[v] == '':
                resMessage = 'Заполните все поля !'
                return resMessage
        try:
            r = post(urls['alloy_read'], values)
            message = r.json()
            resMessage = message['numRecord']
            #print(resMessage)
            return resMessage
        except:
            resMessage = 'Нет соединения с сервером!'
            return resMessage



