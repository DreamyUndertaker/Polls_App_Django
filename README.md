1. Подсистема обновлений:
    Обновлений версий сертификатов безопасности
2. Авторизация\аутентификация:
    Хранение информации о пользователях
3. Лекции:
    Теоритический материал для пользователя
4. Тестирование:
    Тестирование пользователя по заготовленным вопросам
5. Система оценивания:
    ПРоверяет готовность пользователя для работы с СКЗИ (Система криптографичской защиты информации)
6. Криптография:
    Изучить работу с криптографией в спринге
    Хранит данные, необходимые для работы с СКЗИ


Подробное описание модулей:
1. Модуль авторизации:
- Доступ имеют все пользователи
    Две группы пользователй:
        1) Администратор:
            Получаемые данные:
            - ФИО сотрудника прошедшего тестирование
            - Название теста (вопрос масштабируемости)
            - Дата прохождения тестирования
            - Степень прохождения тестирования (оценка пользователя)
            - Затраченное время на прохождение тестирования
            Формат получаемых данных(пример):
             ФИО: Кувшинов Никита Игоревич
                Название теста: Допуск сотрудника к работе с VipNet Client
                Дата прохождения: 24.03.2023
                Степень прохождения: 100
                Затраченное время: 1:35
            Отправляемые данные:
  -    
      2) Тестируемый пользователь:
            Отправляемые данные:
            - Имя
            - Фамилия
            - Отчество
            Получаемые данные:
            - Теоритический материал в формате (Какой формат лекций?)
            - Тестовые вопросы
            - Результаты тестирования
            - (Доступ к допущенным ошибкам, и если да, то в каком формате?)

        Поля для ввода:
            - Имя
            - Пароль (выдается администратором)
            (Все посредством СКЗИ)
    - Результат работы системы: сохранение данных пользователей для дальнейшей связи с результатми тестирования

2. Подсистема обновлений:
    - Должна обновлять версию СКЗИ
    - Проверять актуальность теоритического материала лекций

    - Результат работы системы: поддержание системы в автульном состоянии

3. Модуль лекций:
    - Доступ авторизоанных пользователй
    Формат лекций:
        - Документ pdf

    - Рузельтат работы системы: пользователь получает доступ к лекциям загруженным администратором

4. Модуль тестирования:
    - Доступ имеет авторизованный пользователь
    Возможности пользователя:
        - Выбор правильного по его мнению ответа
        - Переход между вопросами

    Возможности администратора:
        - Тоже что и у пользователя
        - Возможность изменения тестовых вопросов

5. Система оценивания:
- Доступ авторизованных пользотвалей
    Подсистема расчета:
        - Проверяет процентное отношение правильных ответов к неправильным
        - Делает заключение о готовности тестируемого пользователя

    Возможности пользователя:
        - Просмотр своей оценки

    Возможности администратора:
        - Просмотр результатов пользователей

    - Результат работы системы: оценить готовность пользователя к работе с программным комплексом VipNet

6. Модуль криптографии
- Результат работы системы: защита данных посредсовом криптографичских средств защиты






















