import websocket
import ssl
import json
from tests.utils.sender_stand_requests import get_user_id_by_token
from tests.utils.configuration import get_ws_url
import tests.utils.data as data
from tests.utils.utils import assert_structure, assert_user_in_all_chats 

def test_get_chats(access_token):
    user_id = get_user_id_by_token(access_token)
    ws_url = get_ws_url(access_token)
    ws = websocket.create_connection(ws_url, sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.settimeout(5)

    try:
        # При подключении автоматически приходит chat_list
        response_raw = ws.recv()
        response_data = json.loads(response_raw)
        assert response_data.get("type") == "chat_list"  # автоматическая проверка

        # Явно отправляем get_chats
        ws.send(json.dumps(data.WS_GET_CHATS_PAYLOAD))

        # Получаем ответ
        response_raw = ws.recv()
        response_get_chats = json.loads(response_raw)

        # Проверка типа
        assert response_get_chats.get("type") == "chat_list"

        # Проверка структуры
        assert_structure(data.EXPECTED_CHAT_LIST_STRUCTURE, response_get_chats)

        # Проверка наличия хотя бы одного чата
        assert isinstance(response_get_chats.get("chats"), list), "Поле 'chats' должно быть списком"
        # assert len(response_get_chats.get("chats")) >= 1

        # Проверка наличия пользователя в списках участников

        assert_user_in_all_chats(response_get_chats, user_id)

        #for chat in response_get_chats["chats"]:
        #   participant_ids = chat.get("participantId", [])
        #   assert user_id in participant_ids, f"Пользователь {user_id} не найден в участниках чата {chat['id']}"

    finally:
        ws.close()