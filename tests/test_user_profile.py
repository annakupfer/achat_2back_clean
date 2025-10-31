import requests
import tests.utils.configuration as configuration
from tests.utils.data import TEST_PHONE, headers_with_token

def test_api_get_user_getData(access_token):
    
    url = configuration.BASE_URL + configuration.USER_GET_DATA_PATH
    headers = headers_with_token(access_token)

    params = {"phone": TEST_PHONE}

    response = requests.get(url, headers=headers, params=params)
    assert response.status_code == 200
    data = response.json()
    assert data["phone"] == TEST_PHONE
