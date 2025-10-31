import websocket
import ssl
import json
import pytest
from tests.utils.configuration import get_ws_url
import tests.utils.data as data
import copy
from tests.utils.utils import assert_structure


def test_reply_message(access_token):
    
    ws_url = get_ws_url(access_token)
    ws = websocket.create_connection(ws_url, sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.settimeout(5)  # Таймаут 5 секунд на recv()

    try:
        # Получаем список чатов
        response_raw = ws.recv()
        response_data = json.loads(response_raw)
        assert response_data.get("type") == "chat_list"

        message_payload = data.WS_SEND_MESSAGE_TO_USER_PAYLOAD

        # Отправляем обычное сообщение
        print("Sending message payload:", message_payload)
        ws.send(json.dumps(message_payload))

        # Получаем ответ chat_message на отправку
        response_raw = ws.recv()
        response_send = json.loads(response_raw)
        assert response_send.get("type") == "chat_message"

        chat_id_sent = response_send.get("chat_id")
        message_id_sent = response_send["messages"]["id"]

        # Проверяем текст сообщения
        assert response_send["messages"]["message"] == message_payload["message"]

        # Получаем confirmation на отправку сообщения
        response_raw = ws.recv()
        response_confirmation = json.loads(response_raw)
        assert response_confirmation.get("type") == "confirmation"
        assert str(response_confirmation.get("chat_id")) == str(chat_id_sent)

        reply_payload = copy.deepcopy(data.WS_REPLY_PAYLOAD_TEMPLATE)
        reply_payload["chat_id"] = chat_id_sent
        reply_payload["original_message_id"] = message_id_sent


        # Теперь отправляем reply
        print("Sending reply payload:", reply_payload)
        ws.send(json.dumps(reply_payload))

        try:
            response_raw = ws.recv()
        except websocket.WebSocketTimeoutException:
            pytest.fail("Timeout waiting for reply message response")

        response_reply = json.loads(response_raw)
        print("Reply response:", response_reply)

        # Проверяем тип сообщения
        assert response_reply.get("type") == "chat_message"

        # Проверяем совпадение chat_id
        assert str(response_reply.get("chat_id")) == str(chat_id_sent)

    
        # Можно добавить проверку структуры, если есть шаблон для reply
        assert_structure(data.EXPECTED_REPLY_MESSAGE, response_reply)

    finally:
        ws.close()