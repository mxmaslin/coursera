# Реализовать Chain of Responsibility

Вам дан объект класса `SomeObject`, содержащего три поля: `integer_field`, `float_field` и `string_field`:
  
    class SomeObject:
        def __init__(self):
            self.integer_field = 0
            self.float_field = 0.0
            self.string_field = ""  

Необходимо реализовать:
- `EventGet(<type>)` создаёт событие получения данных соответствующего типа
- `EventSet(<value>)` создаёт событие изменения поля типа `type(<value>)`
- классы `NullHandler`, `IntHandler`, `FloatHandler`, `StrHandler` так, чтобы можно было создать цепочку:

`chain = IntHandler(FloatHandler(StrHandler(NullHandler())))`

- `chain.handle(obj, EventGet(int))` — вернуть значение `obj.integer_field`
- `chain.handle(obj, EventGet(str))` — вернуть значение `obj.string_field`
- `chain.handle(obj, EventGet(float))` — вернуть значение `obj.float_field`
- `chain.handle(obj, EventSet(1))` — установить значение `obj.integer_field = 1`
- `chain.handle(obj, EventSet(1.1))` — установить значение `obj.float_field = 1.1`
- `chain.handle(obj, EventSet("str"))` — установить значение `obj.string_field = "str"`

**Решение**:

    E_INT, E_FLOAT, E_STR = "INT", "FLOAT", "STR"


    class EventGet:
        def __init__(self, prop):
            self.kind = {int:E_INT, float:E_FLOAT, str:E_STR}[prop];
            self.prop = None;


    class EventSet:
        def __init__(self, prop):
            self.kind = {int:E_INT, float:E_FLOAT, str:E_STR}[type(prop)];
            self.prop = prop;


    class NullHandler:
        def __init__(self, successor=None):
            self.__successor = successor

        def handle(self, obj, event):
            if self.__successor is not None:
                return self.__successor.handle(obj, event)


    class IntHandler(NullHandler):
        def handle(self, obj, event):
            if event.kind == E_INT:
                if event.prop is None:
                    return obj.integer_field
                else:
                    obj.integer_field = event.prop;
            else:
                return super().handle(obj, event)


    class StrHandler(NullHandler):
        def handle(self, obj, event):
            if event.kind == E_STR:
                if event.prop is None:
                    return obj.string_field
                else:
                    obj.string_field = event.prop;
            else:
                return super().handle(obj, event)


    class FloatHandler(NullHandler):
        def handle(self, obj, event):
            if event.kind == E_FLOAT:
                if event.prop is None:
                    return obj.float_field
                else:
                    obj.float_field = event.prop;
            else:
                return super().handle(obj, event)