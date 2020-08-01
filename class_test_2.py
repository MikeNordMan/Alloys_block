from class_test import Test


class TestNew(Test):
    def __init__(self, status, data):
        super().__init__(status=status)
        self.data = data


win1 = TestNew('2', 20)
win1.main()