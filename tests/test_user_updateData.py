import requests
import tests.utils.configuration as configuration
from tests.utils.data import TEST_PHONE, headers_with_token, USER_UPDATEDATA_PAYLOAD

def test_api_put_user_updateData(access_token):
    
    url = configuration.BASE_URL + configuration.USER_GET_DATA_PATH
    headers = headers_with_token(access_token)
    params = {"phone": TEST_PHONE}

    # Получаем текущие данные пользователя
    response = requests.get(url, headers=headers, params = params)
    response.raise_for_status()
    old_data = response.json()

    # Обновляем данные пользователя
    url = url = configuration.BASE_URL + configuration.USER_UPDATE_DATA_PATH
    new_data = USER_UPDATEDATA_PAYLOAD
    response = requests.put(url, headers=headers, json = new_data, params=params)

    # Распечатаем ответ

    print("Response status:", response.status_code)
    print("Response text:", response.text)

    assert response.status_code == 200, f"Ошибка обновления: {response.text}"
    assert response.status_code == 200
    data = response.json()
    assert data["phone"] == TEST_PHONE

    # Возвращаем старые данные (чтобы тест не ломал окружение)

    # Поля, которые сервер принимает для обновления
    allowed_fields = ["firstName", "lastName", "nickName", "aboutMe", "birthday"]

    # Формируем данные для восстановления
    restore_data = {k: old_data[k] for k in allowed_fields if k in old_data}

    # Восстанавливаем старые данные
    response = requests.put(url, headers=headers, json=restore_data, params=params)
    assert response.status_code == 200, "Не удалось восстановить исходные данные"

    restored = response.json()
    for key, value in restore_data.items():
        if key in restored:
            assert restored[key] == value, f"Поле {key} не восстановилось"