## В этом модуле вспомогательные функцмм, не завязанные на конкретные данные

import json 
import ssl
import time
from . import data
import websocket
from tests.utils.configuration import get_ws_url

# Функция проверки структуры сообщения
def assert_structure(expected, actual, path="root"):
    """
    Рекурсивно проверяет, что структура actual соответствует expected.
    Поддерживает шаблоны вида:
      {"key": str}  — ожидается строка
      {"key": (str, type(None))} — допускаются несколько типов
      {"key": {"subkey": int}} — вложенные словари
    """
    for key, expected_value in expected.items():
        assert key in actual, f"{path}: ключ '{key}' отсутствует в actual"
        actual_value = actual[key]

        if isinstance(expected_value, dict):
            assert isinstance(actual_value, dict), f"{path}.{key} должен быть словарём"
            assert_structure(expected_value, actual_value, f"{path}.{key}")

        elif isinstance(expected_value, list):
            assert isinstance(actual_value, list), f"{path}.{key} должен быть списком"
            if expected_value:
                expected_item = expected_value[0]
                for i, item in enumerate(actual_value):
                    if isinstance(expected_item, dict):
                        assert_structure(expected_item, item, f"{path}.{key}[{i}]")
                    else:
                        assert isinstance(item, type(expected_item)), (
                            f"{path}.{key}[{i}]: expected {type(expected_item).__name__}, got {type(item).__name__}"
                        )

        else:
            if actual_value is not None:
                # ✅ поддержка типизированных шаблонов
                if isinstance(expected_value, type):
                    assert isinstance(actual_value, expected_value), (
                        f"{path}.{key}: expected {expected_value.__name__}, got {type(actual_value).__name__}"
                    )
                # ✅ поддержка кортежей типов (например (str, type(None)))
                elif isinstance(expected_value, tuple) and all(isinstance(t, type) for t in expected_value):
                    assert isinstance(actual_value, expected_value), (
                        f"{path}.{key}: expected one of {[t.__name__ for t in expected_value]}, got {type(actual_value).__name__}"
                    )
                else:
                    assert isinstance(actual_value, type(expected_value)), (
                        f"{path}.{key}: expected {type(expected_value).__name__}, got {type(actual_value).__name__}"
                    )

# Функция проверки того, что пользователь находится во всех выданных чатах

def assert_user_in_all_chats(response_data, user_id):
    print("Функция вызвалась")  # отладка
    chats = response_data.get("chats", [])
    missing_in = []

    for chat in chats:
        participant_ids = chat.get("participantId", [])
        if user_id not in participant_ids:
            missing_in.append(chat.get("id"))

    if missing_in:
        print(f"[WARN] Пользователь {user_id} не найден в участниках чатов: {missing_in}")
    else:
        print(f"[INFO] Пользователь {user_id} найден во всех {len(chats)} чатах.")

# Функция ожидания сообщения конкретного типа 


def wait_for_types_multiple(ws, expected_counts, timeout=10):
    """
    Ждём несколько сообщений разных типов.

    :param ws: WebSocket соединение
    :param expected_counts: dict, ключ — тип сообщения, значение — сколько таких ждать
    :param timeout: таймаут
    :return: dict с типами, где значение — список сообщений данного типа
    """
    start = time.time()
    found = {msg_type: [] for msg_type in expected_counts}

    while any(len(found[msg_type]) < count for msg_type, count in expected_counts.items()):
        if time.time() - start > timeout:
            missing = {t: c - len(found[t]) for t, c in expected_counts.items() if len(found[t]) < c}
            raise AssertionError(f"Не получили сообщения: {missing}")

        raw = ws.recv()
        msg = json.loads(raw)
        msg_type = msg.get("type")

        if msg_type in found and len(found[msg_type]) < expected_counts[msg_type]:
            found[msg_type].append(msg)

    return found



# Функция отправки сообщения в группу

def send_message_to_group(ws, chat_id, message_text="", attachments=None):
    """
    Отправляет сообщение через WebSocket.

    :param ws: WebSocket-соединение
    :param chat_id: ID чата
    :param message_text: Текст сообщения
    :param attachments: Список вложений (списки словарей с id и типом)
    :param message_type: Тип сообщения (по умолчанию TEXT)
    :param parent_id: ID родительского сообщения (если это ответ)
    """
    payload = {
        "action": "send_message",
        "chat_id": chat_id,
        "message": message_text,
        "documents": attachments or []
    }
    ws.send(json.dumps(payload))

    responses = wait_for_types_multiple(ws,{"confirmation":1,"chat_message":1})
    return responses["chat_message"][0]  

# Функция отправки сообщения пользователю                            

def send_message_to_user(ws, participant_id, message_text="", attachments=None):
    payload = {
        "action": "send_message",
        "participant_id": participant_id,
        "message": message_text,
        "documents": attachments or []
    }
    ws.send(json.dumps(payload))

    responses = wait_for_types_multiple(ws, {"confirmation": 1, "chat_message": 1})
    return responses["chat_message"][0]

# Функция инициации звонка


def initiate_call(access_token, callee_phone_number):
    """
    Инициирует звонок через WebSocket.
    
    :param access_token: access token вызывающего пользователя
    :param callee_phone_number: номер вызываемого (callee)
    :param user_phone: опционально — телефон инициатора (если сервер ожидает)
    :return: (ws, response_call_started)
    """
    ws_url = get_ws_url(access_token)
    ws = websocket.create_connection(ws_url, sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.settimeout(5)

    # Получаем первое сообщение от сервера — chat_list
    ws.recv()

    # Формируем payload
    payload = {
        "action": "start_call",
        "callee_phone_number": callee_phone_number,
        "sdp": data.WS_CALL_INITIATION_PAYLOAD.get("sdp")  # если sdp есть, иначе None
    }

    
    # Отправляем сообщение
    ws.send(json.dumps(payload))

    # Получаем ответ
    response_raw = ws.recv()
    response_call_started = json.loads(response_raw)

    return ws, response_call_started
