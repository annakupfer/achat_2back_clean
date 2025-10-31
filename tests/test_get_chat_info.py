import websocket
import ssl
import json
import copy

from tests.utils.configuration import get_ws_url
import tests.utils.data as data
from tests.utils.utils import assert_structure 

def test_get_chat_info(access_token):
    
    ws_url = get_ws_url(access_token)
    ws = websocket.create_connection(ws_url, sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.settimeout(60)
    try:
        # При подключении автоматически приходит chat_list
        response_raw = ws.recv()
        response_data = json.loads(response_raw)
        assert response_data.get("type") == "chat_list"  # автоматическая проверка

        # Явно отправляем get_chats, чтобы получить чаты пользователя
        ws.send(json.dumps(data.WS_GET_CHATS_PAYLOAD))

        # Получаем ответ
        response_raw = ws.recv()
        response_get_chats = json.loads(response_raw)
        assert response_get_chats.get("type") == "chat_list"

        chats = response_get_chats.get("chats", [])
        assert chats, "У пользователя нет чатов"

        # Выбираем первый чат для проверки получения данных чата
        chat_id = chats[0]["id"]

        # Посылаем запрос на получение информации о конкретном чате авторизованного пользователя
        payload = copy.deepcopy(data.WS_GET_CHAT_INFO_TEMPLATE)
        payload["chat_id"] = chat_id

        ws.send(json.dumps(payload))

        # Получаем ответ
        response_raw = ws.recv()
        response_get_chat = json.loads(response_raw)

        # Проверка типа
        assert response_get_chat.get("type") == "chat_list"

        # Проверка, что chat-id совпадает с запрошенным
        assert response_get_chat.get("chats")[0]["id"] == chat_id

        # Проверка структуры ответа
        assert_structure(data.EXPECTED_CHAT_LIST_STRUCTURE,response_get_chat)

    finally:
        ws.close()





