'''
В этом задании вам нужно создать интерфейс для работы с файлами. Класс File должен поддерживать несколько необычных операций.

Класс инициализируется полным путем.

obj = File('/tmp/file.txt')

Класс должен поддерживать метод write.

obj.write('line\n')

Объекты типа File должны поддерживать сложение.

first = File('/tmp/first')
second = File('/tmp/second')
new_obj = first + second

В этом случае создается новый файл и файловый объект, в котором содержимое второго файла добавляется к содержимому первого файла. Новый файл должен создаваться в директории, полученной с помощью tempfile.gettempdir. Для получения нового пути можно использовать os.path.join.

Объекты типа File должны поддерживать протокол итерации, причем итерация проходит по строкам файла.

for line in File('/tmp/file.txt'):
    ...

И наконец, при выводе файла с помощью функции print должен печататься его полный путь, переданный при инициализации.

obj = File('/tmp/file.txt')
print(obj)
'/tmp/file.txt'
'''


import os
import uuid


class File:
    def __init__(self, path):
        self.path = path
        self.current_position = 0

        if not os.path.exists(self.path):
            open(self.path, 'w').close()

    def write(self, content):
        with open(self.path, 'w') as f:
            return f.write(content)

    def read(self):
        with open(self.path, 'r') as f:
            return f.read()

    def __add__(self, obj):
        new_path = os.path.join(
            os.path.dirname(self.path),
            str(uuid.uuid4().hex)
        )
        new_file = type(self)(new_path)
        new_file.write(self.read() + obj.read())

        return new_file

    def __str__(self):
        return self.path

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.path, 'r') as f:
            f.seek(self.current_position)

            line = f.readline()
            if not line:
                self.current_position = 0
                raise StopIteration('EOF')

            self.current_position = f.tell()
            return line