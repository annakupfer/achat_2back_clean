import websocket
import ssl
import json
from tests.utils.configuration import get_ws_url
import tests.utils.data as data
from tests.utils.utils import send_message_to_group

# Тест для отправки сообщения в группу


def test_send_message_to_group(access_token):
    ws_url = get_ws_url(access_token)
    ws = websocket.create_connection(ws_url, sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.settimeout(15)

    try:
        response_data = json.loads(ws.recv())
        assert response_data.get("type") == "chat_list"

        payload = data.WS_SEND_MESSAGE_TO_GROUP_PAYLOAD
        chat_id = payload["chat_id"]
        message_text = payload["message"]

        # Просто вызываем и получаем chat_message
        chat_message = send_message_to_group(ws, chat_id, message_text)

        # Проверки chat_message
        assert chat_message["type"] == "chat_message"
        assert chat_message["chat_id"] == chat_id
        assert chat_message["messages"]["message"] == message_text
        assert chat_message["messages"]["isMyMessage"] is True

    finally:
        ws.close()
