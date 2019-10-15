/**
 * @param {Array} collection
 * @params {Function[]} – Функции для запроса
 * @returns {Array}
 */
function query(collection) {
    var friends = JSON.parse(JSON.stringify(collection));

	if (arguments.length === 1) return friends;

    // filterIn
    for (var i = 1; i < arguments.length; i++){
        if (arguments[i].name == 'filterIn') {
            var f = arguments[i];
            var filtered = f(friends);
            friends = intersect(friends, filtered);
        }     
    }

    // select
    var selectArgs = [];
    for (var i = 1; i < arguments.length; i++){
        if (arguments[i].name == 'select') {
            var f = arguments[i];
            selectArgs.push(f(collection));
        }
    }
    var intersectedSelectArgs = getIntersectedSelectArgs(selectArgs);
    friends = selectIntersected(friends, intersectedSelectArgs);

    return friends;
}

function intersect(array1, array2) {
    return array1.filter(function(element){
        return array2.indexOf(element) != -1;
    });
}

function getIntersectedSelectArgs(args){
    if (args.length === 0) return [];
    return args.reduce(function(a, b){
        return a.filter(function(element){
            return b.indexOf(element) != -1;
        });
    });
}

/**
 * @params {String[]}
 */
function select() {
    var args = [].slice.call(arguments);
    return function select(collection) {
        return args;
    }
}

function selectIntersected(collection, fields) {
    if (fields.length === 0) return collection;
    collectionFields = Object.keys(collection[0]);
    var friends = [];
    for (var item in collection){
        var friend = {};
        for (let field of fields){
            if (collectionFields.indexOf(field) > -1) {
                friend[field] = collection[item][field];
            }
        }
        if (Object.keys(friend).length > 0) friends.push(friend);
    }
    return friends;
}

/**
 * @param {String} property – Свойство для фильтрации
 * @param {Array} values – Массив разрешённых значений
 */
function filterIn(property, values) {
    return function filterIn(collection){
        return collection.filter(function(n){
            return values.indexOf(n[property]) != -1;
        });
    }
}

module.exports = {
    query: query,
    select: select,
    filterIn: filterIn
};

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
// var result = query(
//     friends,
//     select('name', 'gender', 'email', 'szuko'),
//     // select('name')
//     // filterIn('favoriteFruit', ['Яблоко', 'Картофель']),
//     // filterIn('favoriteFruit', ['Картофель']),
//     // select('name', 'gender'),
//     // filterIn('favoriteFruit', ['Ананас', 'Картофель']),
//     // filterIn('favoriteFruit', ['Ананас']),
//     // select()
// );
// console.log(result);
