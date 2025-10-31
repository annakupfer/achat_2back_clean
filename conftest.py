import pytest
from tests.utils.sender_stand_requests import request_otp, confirm_otp
from tests.utils.data import TEST_PHONE, OTP_CODE

@pytest.fixture(scope="function")
def access_token():

    request_otp(TEST_PHONE)
    response = confirm_otp(TEST_PHONE, OTP_CODE)
    token = response.json().get("accessToken")
    assert token is not None
    return token

#@pytest.fixture(scope="session")
#def caller_token():
#    """Авторизация основного пользователя (инициатор звонка)"""
#   token = confirm_otp(CALLER_PHONE_NUMBER, OTP_CODE)
#    return token

#@pytest.fixture(scope="session")
#def callee_token():
#    """Авторизация второго пользователя (тот, кто отвечает на звонок)"""
#    token = confirm_otp(CALLEE_PHONE_NUMBER, OTP_CODE )
#    return token

from pathlib import Path

@pytest.fixture
def assets_dir():
    return Path(__file__).parent / "test_file_upload" / "assets"
