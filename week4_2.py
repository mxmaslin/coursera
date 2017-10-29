'''
Часто при зачислении каких-то средств на счет с нас берут комиссию. Давайте реализуем похожий механизм с помощью дескрипторов. Напишите дескриптор Value, который будет использоваться в нашем классе Account.

class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission

У аккаунта будет атрибут commission. Именно эту коммиссию и нужно вычитать при присваивании значений в amount.

new_account = Account(0.1)
new_account.amount = 100
print(new_account.amount)
'''


class Value:
    def __init__(self):
        self.amount = 0

    def __get__(self, obj, obj_type):
        return self.amount

    def __set__(self, obj, value):
        self.amount = value - value * obj.commission