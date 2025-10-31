Автотесты Smoke для ключевых функций backend на Java
Данный проект содержит набор автоматизированных smoke тестов, предназначенных для проверки основных функций backend-сервиса, реализованного на Java. Smoke тестирование помогает быстро убедиться, что ключевые компоненты системы работают корректно после новых изменений или деплоя.

Цели проекта
Быстрая проверка критически важных функций backend.
Обеспечение стабильности основных сервисов.
Раннее выявление серьёзных регрессий.
Автоматизация рутинного тестирования.
В рамках smoke тестирования backend (Java) автоматизированные тесты покрывают следующие ключевые функции:
Аутентификация и подтверждение пользователей (test_auth.py)
Управление соединениями и подключениями WebSocket (test_connection.py, test_connection_without_token.py)
Создание и управление групповыми чатами (test_create_group.py, test_create_group.py)
Получение списка чатов и информации о чатах (test_get_chats.py, test_get_chat_info.py, test_get_chats.py)
Отправка сообщений и работа с сообщениями (включая пересылку и ответы)
(test_send_message.py, test_forward_message_to_user.py, test_reply_message.py, test_response_message.py, test_send_message.py)
Получение списка сообщений и их обработка (test_get_messages.py)
Проверка профиля пользователя (test_user_profile.py, test_api_tests/test_user_profile.py)
Инициация вызовов (test_call_initiation.py)
Работа с WebSocket-соединениями без токена (test_connection_without_token.py)
Общие WebSocket-тесты и сценарии (test_ws_connection.py)
Загрузка файла (test_file_upload.py)
Добавление контакта (test_add_contact.py)
Получение списка контактов (test_get_contacts_list.py)
Структура проекта
api/ — клиентские модули для взаимодействия с backend.
tests/ — директория с тестовыми сценариями.
utils/ — вспомогательные модули и настройки.
venv/ — виртуальное окружение Python (не включается в репозиторий).
Используемые технологии
Python 3.13
Pytest — фреймворк для написания и запуска тестов.
WebSocket — для тестирования реального времени.
Requests — для HTTP-запросов (если используются).
Как запустить тесты
Активировать виртуальное окружение:
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # WindowsКраткое описание проекта.

## Установка

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
