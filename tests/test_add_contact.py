import websocket
import ssl
import json
from tests.utils.configuration import get_ws_url
import tests.utils.data as data
from tests.utils.utils import assert_structure


def test_add_contact(access_token):
    ws_url = get_ws_url(access_token)
    ws = websocket.create_connection(ws_url, sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.settimeout(5)

    contact_phone = data.WS_ADD_CONTACT_PAYLOAD["contactPhone"]

    try:
        # Получаем стартовое сообщение
        response_data = json.loads(ws.recv())
        assert response_data.get("type") == "chat_list"

        # Добавляем контакт
        ws.send(json.dumps(data.WS_ADD_CONTACT_PAYLOAD))
        response_data = json.loads(ws.recv())

        # Если сервер вернул exception
        if response_data.get("type") == "exception":
            error_msg = response_data.get("message", "")

            # Контакт уже существует — просто фиксируем это и завершаем тест
            if "already exists" in error_msg.lower():
                print(f"Контакт {contact_phone} уже существует")
                return
            else:
                raise Exception(f"Unexpected exception from server: {error_msg}")

        # Проверяем успешный ответ при добавлении
        assert response_data.get("type") == "contact_action"
        assert response_data.get("action") == "added"
        assert_structure(data.EXPECTED_CONFIRMATION_ADD_CONTACT, response_data)

    finally:
        # После теста удаляем контакт(ы) одним запросом
        delete_payload = {
            "action": "delete_contacts",
            "contact_phones": [contact_phone]
        }
        try:
            ws.send(json.dumps(delete_payload))
            ws.recv()  # читаем ответ
        except Exception as e:
            print(f"⚠️ Ошибка при удалении контакта: {e}")
        finally:
            ws.close()
