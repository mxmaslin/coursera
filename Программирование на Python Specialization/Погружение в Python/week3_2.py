import csv
import sys
import os.path


class CarBase:
    """Базовый класс с общими методами и атрибутами"""

    # индексы полей, которые соответствуют колонкам в исходном csv-файле 
    ix_car_type = 0
    ix_brand = 1
    ix_passenger_seats_count = 2
    ix_photo_file_name = 3
    ix_body_whl = 4
    ix_carrying = 5
    ix_extra = 6

    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        _, ext = os.path.splitext(self.photo_file_name)
        return ext


class Car(CarBase):
    """Класс легковой автомобиль"""
    
    car_type = "car"

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)

    @classmethod
    def from_tuple(cls, row):
        """ Метод для создания экземпляра легкового автомобиля
            из строки csv-файла"""

        return cls(
            row[cls.ix_brand],
            row[cls.ix_photo_file_name],
            row[cls.ix_carrying],
            row[cls.ix_passenger_seats_count],
        )


class Truck(CarBase):
    """Класс грузовой автомобиль"""

    car_type = "truck"

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        # обрабатываем поле body_whl
        try:
            length, width, height = (float(c) for c in body_whl.split("x", 2))
        except ValueError:
            length, width, height = .0, .0, .0

        self.body_length = length
        self.body_width = width
        self.body_height = height

    def get_body_volume(self):
        return self.body_width * self.body_height * self.body_length

    @classmethod
    def from_tuple(cls, row):
        return cls(
            row[cls.ix_brand],
            row[cls.ix_photo_file_name],
            row[cls.ix_carrying],
            row[cls.ix_body_whl],
        )


class SpecMachine(CarBase):
    """Класс спецтехника"""

    car_type = "spec_machine"

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra

    @classmethod
    def from_tuple(cls, row):
        return cls(
            row[cls.ix_brand],
            row[cls.ix_photo_file_name],
            row[cls.ix_carrying],
            row[cls.ix_extra],
        )


def get_car_list(csv_filename):
    with open(csv_filename) as csv_fd:
        # создаем объект csv.reader для чтения csv-файла
        reader = csv.reader(csv_fd, delimiter=';')
        
        # пропускаем заголовок csv
        next(reader)
        
        # это наш список, который будем возвращать
        car_list = []
        
        # объявим словарь, ключи которого - тип автомобиля (car_type),
        # а значения - класс, объект которого будем создавать
        create_strategy = {car_class.car_type: car_class
                           for car_class in (Car, Truck, SpecMachine)}

        # обрабатываем csv-файл построчно
        for row in reader:
            try:
                # определяем тип автомобиля
                car_type = row[CarBase.ix_car_type]
            except IndexError:
                # если не хватает колонок в csv - игнорируем строку
                continue

            try:
                # получаем класс, объект которого нужно создать
                # и добавить в итоговый список car_list
                car_class = create_strategy[car_type]
            except KeyError:
                # если car_type не извесен, просто игнорируем csv-строку
                continue

            try:
                # создаем и добавляем объект в car_list
                car_list.append(car_class.from_tuple(row))
            except (ValueError, IndexError):
                # если данные некорректны, то игнорируем их
                pass

    return car_list


if __name__ == "__main__":
    print(get_car_list(sys.argv[1]))