import requests
from pathlib import Path
import tests.utils.configuration as configuration


def test_upload_test_image(access_token):
    file_path = Path(__file__).parent /  "assets" / "test_image.jpg"
    assert file_path.exists(), f"Файл не найден: {file_path}"

    url = configuration.BASE_URL + configuration.FILE_UPLOAD_PATH
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    with open(file_path, "rb") as f:
        files = {
            "file": (file_path.name, f, "image/jpeg")
        }
        data = {
            "type": "image/jpg"
        }
        response = requests.post(url, headers=headers, files=files, data=data)

    assert response.status_code == 200, f"Ошибка при загрузке: {response.text}"
    json_data = response.json()
    assert "url" in json_data
    assert json_data["filename"] == file_path.name
