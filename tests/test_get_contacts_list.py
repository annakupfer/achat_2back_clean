import websocket
import ssl
import json
from tests.utils.configuration import get_ws_url
import tests.utils.data as data
from tests.utils.utils import assert_structure  

def test_add_contact(access_token):
    
    # Получаем url с токеном
    ws_url = get_ws_url(access_token)
    ws = websocket.create_connection(ws_url, sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.settimeout(5)

    try:

        # Получаем стартовое сообщение от сервера
        response_raw = ws.recv()
        response_data = json.loads(response_raw)
        assert response_data.get("type") == "chat_list"

        # Отправляем запрос на получение списка контактов

        payload = data.WS_GET_CONTACTS_PAYLOAD
        ws.send(json.dumps(payload))

         # Получаем ответ
        response_raw = ws.recv()
        response_get_contacts = json.loads(response_raw)

        # Проверка типа
        assert response_get_contacts.get("type") == "contacts_list"

        # Проверка структуры
        assert_structure(data.EXPECTED_CONTACTS_LIST, response_get_contacts)

    finally:
        ws.close()  



