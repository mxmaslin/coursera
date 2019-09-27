// Встроенный в Node.JS модуль для проверок
var assert = require('assert');

// Подключаем свою функцию
var date = require('./index.js');

var time = date('2017-05-16 13:45')
    .add(24, 'hours')
    .subtract(1, 'months')
    .add(3, 'days')
    .add(15, 'minutes');

assert.deepEqual(
    time.value,
    '2017-04-20 14:00',

    'Если к дате "2017-05-16 13:45" ' +
    'прибавить 24 часа, 3 дня и 15 минут, вычесть 1 месяц, ' +
    'то получится "2017-04-20 14:00"'
);

// assert.throws принимает функцию и
// проверяет, что она выбрасывает исключение определенного типа
assert.throws(
    function () {
        date('2017-05-16 13:45').add(2, 'light-years');
    },
    TypeError,

    'Если попытаться прибавить к дате световой год, ' +
    'то выбросится исключение TypeError'
);

assert.throws(
    function () {
        date('2017-05-16 13:45').add(-2, 'years');
    },
    TypeError,

    'Если попытаться передать в функцию add отрицательное число – выбросится исключение TypeError'
);







var time = date('2015-01-01 00:00')
    .add(5, 'minutes')
    .add(1, 'hours')
    .add(2, 'days')
    .add(3, 'months')
    .add(1, 'years');

assert.deepEqual(
    time.value,
    '2016-04-03 01:05',

    'Если к дате "2015-01-01 00:00" ' +
    'прибавить 5 минут, 1 час, 3 месяца, 1 год ' +
    'то получится "2016-04-03 01:05"'
);


var time = date('2016-04-03 01:05')
    .subtract(5, 'minutes')
    .subtract(1, 'hours')
    .subtract(2, 'days')
    .subtract(3, 'months')
    .subtract(1, 'years');

assert.deepEqual(
    time.value,
    '2015-01-01 00:00',

    'Если к дате "2016-04-03 15:00" ' +
    'прибавить 9 часов ' +
    'то получится "2016-04-04 00:00"'
);


var time = date('2016-04-03 15:00')
    .add(9, 'hours');

assert.deepEqual(
    time.value,
    '2016-04-04 00:00',

    'Если к дате "2016-04-03 15:00" ' +
    'прибавить 9 часов ' +
    'то получится "2016-04-04 00:00"'
);



console.info('OK!');
