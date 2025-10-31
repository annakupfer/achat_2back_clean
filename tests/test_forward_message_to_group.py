import websocket
import ssl
import json
import copy

from tests.utils.configuration import get_ws_url
import tests.utils.data as data
from tests.utils.utils import (
    assert_structure,
    send_message_to_group,
    wait_for_types_multiple
)

def get_forward_message_payload(original_message_id, chat_id):
    payload = copy.deepcopy(data.WS_FORWARD_MESSAGE_TO_GROUP_TEMPLATE)
    payload["original_message_id"] = original_message_id
    payload["chat_id"] = chat_id
    return payload

def test_forward_message_to_group(access_token):
    ws_url = get_ws_url(access_token)
    ws = websocket.create_connection(ws_url, sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.settimeout(60)

    try:
        # Получаем chat_list
        response_raw = ws.recv()
        response_data = json.loads(response_raw)
        assert response_data.get("type") == "chat_list"

        chat_id = data.TEST_CHAT_ID
        message_text = "Message to be forwarded"

        # Отправляем оригинальное сообщение
        original_msg = send_message_to_group(ws, chat_id, message_text)
        original_message_id = original_msg["messages"]["id"]

        # Проверка структуры оригинального сообщения
        assert_structure(data.EXPECTED_CHAT_MESSAGE_NO_ATTACHMENTS, original_msg)
        assert original_msg["messages"]["message"] == message_text

        # Формируем и отправляем пересылку
        forward_payload = get_forward_message_payload(original_message_id, chat_id)
        ws.send(json.dumps(forward_payload))

        # Ждём 1 confirmation и 2 chat_message (в любом порядке)
        expected_counts = {
            "confirmation": 1,
            "chat_message": 2
        }
        responses = wait_for_types_multiple(ws, expected_counts, timeout=15)

        confirmation = responses["confirmation"][0]
        assert_structure(data.EXPECTED_CONFIRMATION, confirmation)

        forwarded_message = None
        new_message = None

        for msg in responses["chat_message"]:
            if msg["messages"].get("isForwarded"):
                forwarded_message = msg
            else:
                new_message = msg

        assert forwarded_message is not None, "Не получили пересланное сообщение"
        assert new_message is not None, "Не получили новое сообщение"

    finally:
        ws.close()
