import websocket
import ssl
import json
import pytest
from tests.utils.configuration import get_ws_url
from tests.utils.utils import assert_structure

# Типизированный шаблон структуры сообщений
EXPECTED_MESSAGE_STRUCTURE = {
    "type": str,
    "messagesList": [
        {
            "date": str,
            "messagesInDate": [
                {
                    "id": int,
                    "message": str,
                    "sender": int,
                    "created": str,
                    "isMyMessage": bool,
                    "isRead": bool,
                    "isForwarded": bool,
                    "type": str,
                    "attachments": [
                        {
                            "id": int,
                            "url": str,
                            "name": str,
                            "type": str,
                            "thumbnail": str,
                            "duration": (str, type(None))  # может быть строкой или None
                        }
                    ]
                }
            ]
        }
    ]
}

def test_get_messages(access_token):
    ws_url = get_ws_url(access_token)
    ws = websocket.create_connection(ws_url, sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.settimeout(5)  # Таймаут 5 секунд на recv()

    try:
        # Получаем список чатов
        response_raw = ws.recv()
        response_data = json.loads(response_raw)
        assert response_data.get("type") == "chat_list"

        # Готовим payload для получения сообщений
        get_messages_payload = {
            "action": "get_messages",
            "chat_id": 117,  # пример корректного chat_id
            "page_number": 0
        }

        print("Sending get_messages payload:", get_messages_payload)
        ws.send(json.dumps(get_messages_payload))

        try:
            response_raw = ws.recv()
        except websocket.WebSocketTimeoutException:
            pytest.fail("Timeout waiting for get_messages response")

        response_messages = json.loads(response_raw)
        print("Received messages response:", json.dumps(response_messages, indent=2))

        # Проверяем тип ответа
        assert response_messages.get("type") == "search_results"

        # Проверяем наличие списка сообщений (может быть пустым)
        messages_list = response_messages.get("messagesList")
        assert messages_list is not None, "messagesList отсутствует в ответе"
        if messages_list:
        # Если есть сообщения, проверяем их структуру
            assert_structure(EXPECTED_MESSAGE_STRUCTURE, response_messages)
        else:
            print("Чат пустой, сообщений нет")
    finally:
        ws.close()