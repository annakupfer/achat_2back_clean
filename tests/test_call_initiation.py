
import tests.utils.data as data
from tests.utils.utils import initiate_call, assert_structure

#@pytest.mark.call

def test_call_initiation(access_token):

    ws, response = initiate_call(
    access_token=access_token,
    callee_phone_number=data.CALLEE_PHONE
)


    try:
        assert response.get("type") == "call_started"
        assert response.get("user_phone") == data.CALLER_PHONE
        assert response.get("callee_phone") == data.CALLEE_PHONE
    finally:
        ws.close()

