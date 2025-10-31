import websocket
import ssl
import pytest
from tests.utils.configuration import get_ws_url

def test_connection_without_token_raises():
    ws_url = get_ws_url(access_token=None)
    
    with pytest.raises(websocket.WebSocketException) as exc_info:
        websocket.create_connection(ws_url, sslopt={"cert_reqs": ssl.CERT_NONE})

    assert "401" in str(exc_info.value), "Ожидается ошибка 401 Unauthorized при отсутствии токена"
