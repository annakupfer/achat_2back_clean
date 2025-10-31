import json
import ssl
import websocket
import tests.utils.data as data
from tests.utils.configuration import get_ws_url
from tests.utils.utils import assert_structure
from tests.utils.data import EXPECTED_CONFIRMATION

def test_create_group(access_token):
    ws_url = get_ws_url(access_token)
    ws = websocket.create_connection(ws_url, sslopt={"cert_reqs": ssl.CERT_NONE})

    group_id = None

    try:
        # Получаем список чатов
        response_raw = ws.recv()
        response_data = json.loads(response_raw)
        assert response_data.get("type") == "chat_list" 
        
        # Создаём группу
        payload = data.WS_CREATE_GROUP_PAYLOAD
        ws.send(json.dumps(payload))

        # Получаем confirmation
        response_raw = ws.recv()
        response_data = json.loads(response_raw)
        assert response_data.get("type") == "confirmation"

        # Проверяем структуру confirmation
        assert_structure(EXPECTED_CONFIRMATION, response_data)

        # Извлекаем ID созданной группы
        group_id = response_data.get("chat_id")
        assert group_id is not None, "chat_id не вернулся в ответе"

    finally:
        # Удаляем группу, если она была создана
        if group_id:
            delete_payload = {
                "action": "delete_group",
                "chat_id": group_id
            }
            ws.send(json.dumps(delete_payload))
            ws.recv()  # читаем подтверждение (если сервер что-то возвращает)
        ws.close()
