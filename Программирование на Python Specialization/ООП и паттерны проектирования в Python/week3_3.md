Продолжая работу над игрой, вы добрались до системы достижений. Иногда игре нужно наградить игрока за то, что он достигает определенного результата в игре. Это может быть, например, прохождение всех заданий в игре, достижение определенного уровня, совершение какого-то сложного действия и т.д.

У каждой игры есть движок и интерфейс пользователя. Это два компонента, которые работают параллельно и взаимодействуют друг с другом. Достижения генерируются движком игры, а отображаются пользовательским интерфейсом. Кроме того, на современных игровых площадках, таких как Steam, Google Play, также отображаются достижения, полученные игроком. Для этого применяется как раз паттерн Наблюдатель.

У вас есть движок Engine, который может создавать уведомления о достижениях. Вам необходимо написать обертку над движком, которая будет иметь возможность подписывать наблюдателей и рассылать им уведомления, а также иерархию наблюдателей. В иерархию наблюдателей должны входить абстрактный наблюдатель, `AbstractObserver`, от которого унаследованы 2 наблюдателя `ShortNotificationPrinter` и `FullNotificationPrinter`. Первый из них составляет множество названий полученных достижений, второй составляет список достижений в том порядке, в котором они даны в системе. Имейте в виду, что каждое достижение должно быть учтено только один раз.

Иерархия классов приведена на следующей UML диаграмме:

[observer](observer_scheme.jpg)

Пример достижения, которое генерирует движок:

    {"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"}

Метод `update` не должен возвращать никаких значений, он должен только изменять переменную `achievements`.

Класс `Engine` реализовывать не нужно!

**Решение**:

    from abc import ABC, abstractmethod


    class ObservableEngine(Engine):
        def __init__(self):
            self.__subscribers = set()

        def subscribe(self, subscriber):
            self.__subscribers.add(subscriber)

        def unsubscribe(self, subscriber):
            self.__subscribers.remove(subscriber)

        def notify(self, message):
            for subscriber in self.__subscribers:
                subscriber.update(message)


    class AbstractObserver(ABC):
        @abstractmethod
        def update(self, message):
            pass


    class ShortNotificationPrinter(AbstractObserver):
        def __init__(self):
            self.achievements = set()

        def update(self, message):
            self.achievements.add(message['title'])


    class FullNotificationPrinter(AbstractObserver):
        def __init__(self):
            self.achievements = list()

        def update(self, message):
            if message not in self.achievements:
                self.achievements.append(message)
