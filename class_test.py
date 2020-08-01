


class Test(object):

    def __init__(self, status):
        self.status = status

    def main(self):
        if self.status == '1':
            #print('Первый вариант')
            self.printStatus()
        elif self.status == '2':
            #print('Второй вариант')
            self.printStatus()
    def printStatus(self):
        print(self.status + ' Вариант')

class TestNew(Test):
    def __init__(self, status, data):
        super().__init__(status=status)
        self.data = data


win1 = TestNew('2', 20)
win1.main()

# class Breakfast(object):
#     def __init__(self, eggs, spam):
#         self.spam, self.eggs = spam, eggs
#         class HealthyBreakfast(object):
#             def __init__(self, spam):
#                 super(HealthyBreakfast, self).\
#                     __init__(0, spam)