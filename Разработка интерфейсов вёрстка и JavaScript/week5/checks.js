// Встроенный в Node.JS модуль для проверок
var assert = require('assert');

// Подключаем свою функцию
var emitter = require('./index.js');

// Определим объект для счетчика нотификаций
var notifications = {
    counter: 0,
    count: function () {
        this.counter++;
    }
};

// Определим для хранения логов
var logger = {
    logs: []
};

// Подписываемся на событие new_notification и сразу оповещаем всех подписчиков
emitter
    .on('new_notification', notifications, notifications.count)
    .on('new_notification', logger, function () {
        this.logs.push('Произошло новое событие new_notification');
    })
    .on('new_notification', logger, function () {
        // this указывает на logger
        this.logs.push('Добавлена новая нотификация. Количество - ' + notifications.counter);
    })
    .emit('new_notification');

// Проверяем количество нотификаций
assert.equal(notifications.counter, 1, 'Получена одна нотификация');

// В логе сохранено событие
// Так как обработчик notifications.count отработал первым,
//  в логах сохранено правильное количество нотификаций
assert.deepEqual(logger.logs, [
    'Произошло новое событие new_notification',
    'Добавлена новая нотификация. Количество - 1'
]);

// На время отключаем логгирование, а затем снова включаем
emitter
    .off('new_notification', logger)
    .emit('new_notification')
    .on('new_notification', logger, function () {
        this.logs.push('Новое событие new_notification!');
    })
    .emit('new_notification');

// Проверяем количество нотификаций
assert.equal(notifications.counter, 3, 'Получено три нотификации');
// Проверяем, что логи были отключены, а затем снова подключены
assert.deepEqual(logger.logs, [
    'Произошло новое событие new_notification',
    'Добавлена новая нотификация. Количество - 1',
    'Новое событие new_notification!'
]);

console.info('OK!');
