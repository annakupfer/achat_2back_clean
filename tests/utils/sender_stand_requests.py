import requests
import tests.utils.configuration as configuration
import tests.utils.data as data

def request_otp(phone):
    url = configuration.BASE_URL + "api/v1/auth/getOTPCode"
    payload = {"phone": phone}
    response = requests.post(url, json=payload, headers = data.headers)
    return response

def confirm_otp(phone, otp):
    url = configuration.BASE_URL + "api/v1/auth/signIn"
    payload = {"phone": phone, "otpCode": otp}
    response = requests.post(url, json=payload, headers = data.headers)
    return response


def get_user_id_by_token(access_token):
        url = configuration.BASE_URL.rstrip("/") + "/" + configuration.USER_GET_DATA_PATH.lstrip("/")
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        params = {"phone": data.TEST_PHONE}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()["userId"]
   
