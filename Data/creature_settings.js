{"Сложность":{
    "1":{
        "Хиты":[5, 12],
        "КЗ":[8, 10],
        "Характеристики":[[-3, 0], [-3, 0], [-3, 0], [-3, 0], [-3, 0], [-3, 0]],
        "Мастерство":2
    },

    "2":{
        "Хиты":[12, 20],
        "КЗ":[10, 13],
        "Характеристики":[[-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1]],
        "Мастерство":2
    },

    "3":{
        "Хиты":[20, 30],
        "КЗ":[12, 16],
        "Характеристики":[[0, 2], [0, 2], [0, 2], [0, 2], [0, 2], [0, 2]],
        "Мастерство":3
    },

    "4":{
        "Хиты":[30, 38],
        "КЗ":[14, 16],
        "Характеристики":[[1, 3], [1, 3], [1, 3], [1, 3], [1, 3], [1, 3]],
        "Мастерство":3
    },

    "5":{
        "Хиты":[38, 60],
        "КЗ":[15, 17],
        "Характеристики":[[2, 5], [2, 5], [2, 5], [2, 5], [2, 5], [2, 5]],
        "Мастерство":4
    },

    "6":{
        "Хиты":[60, 85],
        "КЗ":[17, 18],
        "Характеристики":[[2, 6], [2, 6], [2, 6], [2, 6], [2, 6], [2, 6]],
        "Мастерство":5
    },

    "7":{
        "Хиты":[85, 130],
        "КЗ":[18, 19],
        "Характеристики":[[3, 6], [3, 6], [3, 6], [3, 6], [3, 6], [3, 6]],
        "Мастерство":6
    },

    "8":{
        "Хиты":[130, 220],
        "КЗ":[18, 21],
        "Характеристики":[[4, 7], [4, 7], [4, 7], [4, 7], [4, 7], [4, 7]],
        "Мастерство":7
    },

    "9":{
        "Хиты":[220, 330],
        "КЗ":[20, 23],
        "Характеристики":[[5, 8], [5, 8], [5, 8], [5, 8], [5, 8], [5, 8]],
        "Мастерство":8
    },

    "10":{
        "Хиты":[330, 700],
        "КЗ":[21, 25],
        "Характеристики":[[7, 10], [7, 10], [7, 10], [7, 10], [7, 10], [7, 10]],
        "Мастерство":9
    }

},
"Специализация":{
    "Воин":{
        "Бонусы":[1, -1, 1, -2, -1, -2],
        "Текст атаки":"атакует своим оружнием и наносит",
        "Сложность":0,
        "Архетип":"Ближний бой",
        "Воинское оружие":[["Алебарда", 10], ["Боевой молот", 8], ["Глефа", 10],
                           ["Двуручный меч", 12], ["Длинное копье", 12], ["Длинный меч", 8],
                           ["Короткий меч", 6], ["Молот", 12], ["Моргенштерн", 8],
                           ["Пика", 10], ["Рапира", 8], ["Секира", 12],
                           ["Скимитар", 6], ["Трезубец", 6], ["Цеп", 6]],
        "Простое оружие":[["Палица", 8], ["Булава", 6], ["Кинжал", 4],
                          ["Копье", 6], ["Легкий молот", 4], ["Ручной топор", 6]]
    },

    "Маг":{
        "Бонусы":[-2, 0, -2, 0, 1, 1],
        "Текст атаки":"атакует легким оружием и наносит",
        "Сложность":-2,
        "Архетип":"Заклинания",
        "Простое оружие":[["Кинжал", 4], ["Посох", 6]],
        "Шаблон ступень 1": [["Атака", 2], ["Защита", 1]],
        "Шаблон ступень 2": [["Атака", 3], ["Защита", 2]],
        "Шаблон ступень 3": [["Атака", 5], ["Защита", 2]]
    },

    "Стрелок":{
        "Бонусы":[-1, 2, -2, -1, 0, 0],
        "Текст атаки":"делает выстрел и наносит",
        "Сложность":0,
        "Архетип":"Дальний бой",
        "Воинское оружие":[["Ручной арбалет", 6], ["Тяжелый арбалет", 10], ["Длинный лук", 8]],
        "Простое оружие":[["Легкий арбалет", 8], ["Дротик", 4], ["Короткий лук", 6],
                          ["Праща", 4]]

    },

    "Монстр":{
        "Бонусы":[1, -1, 1, -2, -2, -3],
        "Текст атаки":"совершает атаку и наносит",
        "Сложность":0,
        "Архетип":"Ближний бой",
        "Простое оружие":[["Укус", 6], ["Когти", 6], ["Хвост", 6]]
    },

    "Некромант":{
        "Бонусы":[-2, -1, -1, 0, 1, 0],
        "Текст атаки":"атакует легким оружием и наносит",
        "Сложность":-2,
        "Архетип":"Заклинания",
        "Простое оружие":[["Кинжал", 4], ["Посох", 6]],
        "Шаблон ступень 1": [["Некромантия", 3]],
        "Шаблон ступень 2": [["Некромантия", 5]],
        "Шаблон ступень 3": [["Некромантия", 7]]
    },

    "Целитель":{
        "Бонусы":[-2, -1, -2, 0, 1, 2],
        "Текст атаки":"атакует легким оружием и наносит",
        "Сложность":-2,
        "Архетип":"Заклинания",
        "Простое оружие":[["Кинжал", 4], ["Посох", 6]],
        "Шаблон ступень 1": [["Исцеление", 3]],
        "Шаблон ступень 2": [["Исцеление", 3], ["Защита", 2]],
        "Шаблон ступень 3": [["Исцеление", 5], ["Защита", 2]]
    },

    "Жрец":{
        "Бонусы":[0, -1, 1, 0, 1, 0],
        "Текст атаки":"атакует легким оружием и наносит",
        "Сложность":-1,
        "Архетип":"Заклинания",
        "Воинское оружие":[["Двуручный меч", 12], ["Длинный меч", 8], ["Короткий меч", 6],
                           ["Рапира", 8], ["Скимитар", 6]],
        "Простое оружие":[["Палица", 8], ["Булава", 6], ["Кинжал", 4],
                          ["Ручной топор", 6]],
        "Бонусный урон":[["Излучение", 8]],
        "Шаблон ступень 1": [["Исцеление", 1], ["Атака", 2]],
        "Шаблон ступень 2": [["Исцеление", 2], ["Атака", 3]],
        "Шаблон ступень 3": [["Исцеление", 3], ["Атака", 4]]
    },

    "Паладин":{
        "Бонусы":[1, -1, 1, -2, 0, 0],
        "Текст атаки":"совершает атаку и наносит",
        "Сложность":0,
        "Архетип":"Ближний бой",
        "Воинское оружие":[["Алебарда", 10], ["Боевой молот", 8], ["Глефа", 10],
                           ["Двуручный меч", 12], ["Длинный меч", 8], ["Короткий меч", 6],
                           ["Молот", 12], ["Моргенштерн", 8], ["Рапира", 8],
                           ["Секира", 12], ["Скимитар", 6], ["Цеп", 6]],
        "Простое оружие":[["Палица", 8], ["Булава", 6], ["Кинжал", 4],
                          ["Ручной топор", 6]],
        "Бонусный урон":[["Огонь", 8]],
        "Шаблон ступень 1": [["Защита", 3]],
        "Шаблон ступень 2": [["Исцеление", 2], ["Защита", 3]],
        "Шаблон ступень 3": [["Исцеление", 3], ["Защита", 4]]
    },

    "Богоубийца":{
        "Бонусы":[7, 7, 7, 7, 7, 7],
        "Текст атаки":"совершает атаку и наносит",
        "Сложность":0,
        "Архетип":"Бог",
        "Воинское оружие":[["Двуручный меч", 12]],
        "Бонусный урон":[["Излучение", 12]],
        "Школы":["призыв", "ограждение", "проявление", "прорицание",
                 "очарование", "преобразование", "иллюзия", "некромантия"]
    },

    "Божество":{
        "Бонусы":[25, 25, 25, 25, 25, 25],
        "Текст атаки":"совершает атаку и наносит",
        "Сложность":0,
        "Архетип":"Бог",
        "Воинское оружие":[["Двуручный меч", 12], ["Молот", 12], ["Секира", 12]],
        "Бонусный урон":[["Излучение", 12]],
        "Школы":["призыв", "ограждение", "проявление", "прорицание",
                 "очарование", "преобразование", "иллюзия", "некромантия"]
    },

    "Друид":{
        "Бонусы":[0, -1, 1, -1, 1, -2],
        "Текст атаки":"атакует легким оружием и наносит",
        "Сложность":-1,
        "Архетип":"Заклинания",
        "Воинское оружие":[["Короткий меч", 6], ["Рапира", 8], ["Скимитар", 6]],
        "Простое оружие":[["Кинжал", 4], ["Ручной топор", 6], ["Посох", 6]],
        "Шаблон ступень 1": [["Призыв", 2], ["Атака", 1]],
        "Шаблон ступень 2": [["Призыв", 3], ["Защита", 1], ["Атака", 1]],
        "Шаблон ступень 3": [["Призыв", 4], ["Защита", 2], ["Атака", 1]]
    },

    "Убийца":{
        "Бонусы":[-1, 2, -2, -1, 1, 0],
        "Текст атаки":"совершает атаку и наносит",
        "Сложность":0,
        "Архетип":"Ближний бой",
        "Воинское оружие":[["Короткий меч", 6], ["Рапира", 8], ["Скимитар", 6]],
        "Простое оружие":[["Кинжал", 4]],
        "Бонусный урон":[["Яд", 8]]
    }

},

"Черты":{
    "Силач":{
        "Бонусы":[1, 0, 0, 0, 0, 0]
    },

    "Акробат":{
        "Бонусы":[0, 1, 0, 0, 0, 0]
    },

    "Стойкий":{
        "Бонусы":[0, 0, 1, 0, 0, 0]
    },

    "Академик":{
        "Бонусы":[0, 0, 0, 1, 0, 0]
    },

    "Мудрец":{
        "Бонусы":[0, 0, 0, 0, 1, 0]
    },

    "Оратор":{
        "Бонусы":[0, 0, 0, 0, 0, 1]
    },

    "Дрищ":{
        "Бонусы":[-1, 0, 0, 0, 0, 0]
    },

    "Неуклюжий":{
        "Бонусы":[0, -1, 0, 0, 0, 0]
    },

    "Хрупкий":{
        "Бонусы":[0, 0, -1, 0, 0, 0]
    },

    "Тупой":{
        "Бонусы":[0, 0, 0, -1, 0, 0]
    },

    "Наивный":{
        "Бонусы":[0, 0, 0, 0, -1, 0]
    },

    "Интроверт":{
        "Бонусы":[0, 0, 0, 0, 0, -1]
    }
}
}