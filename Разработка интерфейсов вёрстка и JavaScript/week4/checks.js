// Встроенный в Node.JS модуль для проверок
var assert = require('assert');

// Подключаем свою функцию
var lib = require('./index.js');

// Коллекция данных
var friends = [
    {
        name: 'Сэм',
        gender: 'Мужской',
        email: 'luisazamora@example.com',
        favoriteFruit: 'Картофель'
    },
    {
        name: 'Эмили',
        gender: 'Женский',
        email: 'example@example.com',
        favoriteFruit: 'Яблоко'
    },
    {
        name: 'Мэт',
        gender: 'Мужской',
        email: 'danamcgee@example.com',
        favoriteFruit: 'Яблоко'
    },
    {
        name: 'Брэд',
        gender: 'Мужской',
        email: 'newtonwilliams@example.com',
        favoriteFruit: 'Банан'
    },
    {
        name: 'Шерри',
        gender: 'Женский',
        email: 'danamcgee@example.com',
        favoriteFruit: 'Картофель'
    },
    {
        name: 'Керри',
        gender: 'Женский',
        email: 'danamcgee@example.com',
        favoriteFruit: 'Апельсин'
    },
    {
        name: 'Стелла',
        gender: 'Женский',
        email: 'waltersguzman@example.com',
        favoriteFruit: 'Картофель'
    }
];

// Выполняем выборку и фильтрацию с помощью нашего конструктора
var result = lib.query(
    friends,
    lib.select('name', 'gender', 'email'),
    lib.filterIn('favoriteFruit', ['Яблоко', 'Картофель']),
);

// Сравниваем полученный результат с ожидаемым
assert.deepEqual(result, [
    { name: 'Сэм', gender: 'Мужской', email: 'luisazamora@example.com' },
    { name: 'Эмили', gender: 'Женский', email: 'example@example.com' },
    { name: 'Мэт', gender: 'Мужской', email: 'danamcgee@example.com' },
    { name: 'Шерри', gender: 'Женский', email: 'danamcgee@example.com' },
    { name: 'Стелла', gender: 'Женский', email: 'waltersguzman@example.com' }
]);

// Выполняем выборку и фильтрацию с помощью нашего конструктора
var result = lib.query(
    friends,
    lib.select('name', 'gender', 'email'),
    lib.filterIn('favoriteFruit', ['Яблоко', 'Картофель']),
    lib.filterIn('favoriteFruit', ['Яблоко', 'Банан']),
);

// Сравниваем полученный результат с ожидаемым
assert.deepEqual(result, [
    { name: 'Эмили', gender: 'Женский', email: 'example@example.com' },
    { name: 'Мэт', gender: 'Мужской', email: 'danamcgee@example.com' },
]);

// Выполняем выборку и фильтрацию с помощью нашего конструктора
var result = lib.query(
    friends,
    lib.select('name', 'gender', 'email'),
    lib.filterIn('favoriteFruit', ['Яблоко', 'Картофель']),
    lib.filterIn('favoriteFruit', ['Яблоко', 'Банан']),
    lib.select('name'),
);

// Сравниваем полученный результат с ожидаемым
assert.deepEqual(result, [
    { name: 'Эмили'},
    { name: 'Мэт'}
]);

// Выполняем выборку и фильтрацию с помощью нашего конструктора
var result = lib.query(
    friends
);

// Сравниваем полученный результат с ожидаемым
assert.deepEqual(result,
    friends
);

// Выполняем выборку и фильтрацию с помощью нашего конструктора
var result = lib.query(
    friends,
    lib.select('name', 'gender', 'email'),
    lib.filterIn('favoriteFruit', ['Яблоко', 'Картофель']),
    lib.filterIn('favoriteFruit', ['Банан'])
);

// Сравниваем полученный результат с ожидаемым
assert.deepEqual(result, []);

// Выполняем выборку и фильтрацию с помощью нашего конструктора
var result = lib.query(
    friends,
    lib.select('name', 'gender', 'email'),
    lib.filterIn('favoriteFruit', ['Яблоко', 'Картофель']),
    lib.filterIn('favoriteFruit', ['Фейхоа'])
);

// Сравниваем полученный результат с ожидаемым
assert.deepEqual(result, []);

var result = lib.query(
    friends,
    lib.filterIn('favoriteFruit', ['Яблоко', 'Картофель']),
    lib.filterIn('favoriteFruit', ['Картофель'])
);

assert.deepEqual(result, [
  { name: 'Сэм',
    gender: 'Мужской',
    email: 'luisazamora@example.com',
    favoriteFruit: 'Картофель' },
  { name: 'Шерри',
    gender: 'Женский',
    email: 'danamcgee@example.com',
    favoriteFruit: 'Картофель' },
  { name: 'Стелла',
    gender: 'Женский',
    email: 'waltersguzman@example.com',
    favoriteFruit: 'Картофель' }]
);

var result = lib.query(
    friends,
    lib.select('name', 'gender', 'email'),
    lib.select('name')
);

assert.deepEqual(result, [
  { name: 'Сэм' },
  { name: 'Эмили' },
  { name: 'Мэт' },
  { name: 'Брэд' },
  { name: 'Шерри' },
  { name: 'Керри' },
  { name: 'Стелла' }]
);

console.info('OK!');

