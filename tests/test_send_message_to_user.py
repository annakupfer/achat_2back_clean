import websocket
import ssl
import json
from tests.utils.configuration import get_ws_url
import tests.utils.data as data
from tests.utils.utils import assert_structure, wait_for_types_multiple, send_message_to_user

# Тест для отправки сообщения юзеру

def test_send_message_to_user(access_token):
    ws_url = get_ws_url(access_token)
    ws = websocket.create_connection(ws_url, sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.settimeout(15)

    try:
        # При подключении приходит chat_list
        response_raw = ws.recv()
        response_data = json.loads(response_raw)
        assert response_data.get("type") == "chat_list"

        # Данные для отправки сообщения
        payload = data.WS_SEND_MESSAGE_TO_USER_PAYLOAD

        # Отправляем сообщение и получаем chat_message напрямую
        chat_msg = send_message_to_user(ws, payload["participant_id"], payload["message"])

        # Проверяем структуру и содержимое chat_message
        assert_structure(data.EXPECTED_CHAT_MESSAGE_NO_ATTACHMENTS, chat_msg)
        assert chat_msg["messages"]["message"] == payload["message"]

    finally:
        ws.close()
