'''
Первое задание у нас для разогрева. Ваша задача написать Python-модуль solution.py, внутри которого определен класс FileReader.

Инициализатор этого класса принимает аргумент - путь до файла на диске.

У класса должен быть метод read, возвращающий содержимое файла в виде строки.

Еще один момент - внутри метода read вы должны обрабатывать исключение IOError, возникающее, когда файла, с которым был инициализирован класс, на самом деле нет на жестком диске. В случае возникновения такой ошибки метод read должен возвращать пустую строку "".

То есть класс должен работать следующим образом:

reader = FileReader("example.txt")
print(reader.read())
'''



class FileReader:
    """Класс FileReader помогает читать из файла"""

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        try:
            with open(self.file_path) as f:
                return f.read()
        except (IOError, FileNotFoundError):
            return ""
