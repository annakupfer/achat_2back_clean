from tests.utils.sender_stand_requests import request_otp, confirm_otp
import tests.utils.data as data

def test_api_two_step_auth():
    resp_otp = request_otp(data.TEST_PHONE)
    assert resp_otp.status_code == 200

    resp_confirm = confirm_otp(data.TEST_PHONE, data.OTP_CODE)
    assert resp_confirm.status_code == 200

