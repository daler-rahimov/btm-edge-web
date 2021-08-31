import app.ball_thrower_cotroller as ball_thrower_api
from app.ball_thrower_cotroller.ball_thrower_core import BallThrower
import logging 
import pytest
logger = logging.getLogger(__name__)

from app.ball_thrower_cotroller.ball_thrower_core import ERROR_EXPLANATION
pars = [(k, v) for k, v in ERROR_EXPLANATION.items()]

from app.ball_thrower_cotroller.btm_serial_clint import ArduinoBtmClintMock

@pytest.mark.parametrize("test_input,expected", pars)
def test_bt_exceptions(client, superuser_token_headers, monkeypatch, test_input, expected):
    class ArduinoBtmClintStub(ArduinoBtmClintMock):
        def send_cmd(self, spin: int): return test_input; 
    btm_serial_api_stub = ArduinoBtmClintStub("COM4")  
    ball_thrower_stub = BallThrower(btm_serial_api_stub)
    monkeypatch.setattr(ball_thrower_api, "ball_thrower", ball_thrower_stub, raising=True)

    # get spin 
    response = client.get("/api/v1/ball_thrower/spin", headers=superuser_token_headers)
    assert response.status_code == 333 
    assert response.json().get("serial_message") == expected 
    # get power
    response = client.get("/api/v1/ball_thrower/power", headers=superuser_token_headers)
    assert response.status_code == 333 
    assert response.json().get("serial_message") == expected 
    # put spin 
    spin = {'spin': 10}
    response = client.put( "/api/v1/ball_thrower/spin", json=spin, headers=superuser_token_headers)
    assert response.status_code == 333 
    assert response.json().get("serial_message") == expected 
    # put power
    power = {'shot_power': 10}
    response = client.put( "/api/v1/ball_thrower/power", json=power, headers=superuser_token_headers)
    assert response.status_code == 333 
    assert response.json().get("serial_message") == expected 


def test_get_spin(client, superuser_token_headers, monkeypatch):
    VAL = 10
    class ArduinoBtmClintStub(ArduinoBtmClintMock):
        def send_cmd(self, spin: int): return VAL; 
    btm_serial_api_stub = ArduinoBtmClintStub("COM4")  
    ball_thrower_stub = BallThrower(btm_serial_api_stub)
    monkeypatch.setattr(ball_thrower_api, "ball_thrower", ball_thrower_stub, raising=True)

    spin = {'spin': VAL}
    response = client.get("/api/v1/ball_thrower/spin", headers=superuser_token_headers)
    assert response.status_code == 200
    assert response.json() == spin


def test_get_power(client, superuser_token_headers, monkeypatch):
    VAL = 10
    class ArduinoBtmClintStub(ArduinoBtmClintMock):
        def send_cmd(self, spin: int): return VAL; 
    btm_serial_api_stub = ArduinoBtmClintStub("COM4")  
    ball_thrower_stub = BallThrower(btm_serial_api_stub)
    monkeypatch.setattr(ball_thrower_api, "ball_thrower", ball_thrower_stub, raising=True)

    power = {'shot_power': VAL}
    response = client.get("/api/v1/ball_thrower/power", headers=superuser_token_headers)
    assert response.status_code == 200
    assert response.json() == power


def test_put_spin(client, superuser_token_headers, monkeypatch):
    VAL = 10
    class ArduinoBtmClintStub(ArduinoBtmClintMock):
        def send_cmd(self, spin: int): return 0; 
    btm_serial_api_stub = ArduinoBtmClintStub("COM4")  
    ball_thrower_stub = BallThrower(btm_serial_api_stub)
    monkeypatch.setattr(ball_thrower_api, "ball_thrower", ball_thrower_stub, raising=True)

    spin = {'spin': VAL}
    response = client.put( "/api/v1/ball_thrower/spin", json=spin, headers=superuser_token_headers)
    assert response.status_code == 200 
    assert response.json() == spin 

    # value validation 
    spin = {'spin': -101}
    response = client.put( "/api/v1/ball_thrower/spin", json=spin, headers=superuser_token_headers)
    assert response.status_code == 422 
    spin = {'spin': 101}
    response = client.put( "/api/v1/ball_thrower/spin", json=spin, headers=superuser_token_headers)
    assert response.status_code == 422 


def test_put_power(client, superuser_token_headers, monkeypatch):
    VAL = 10
    class ArduinoBtmClintStub(ArduinoBtmClintMock):
        def send_cmd(self, spin: int): return 0; 
    btm_serial_api_stub = ArduinoBtmClintStub("COM4")  
    ball_thrower_stub = BallThrower(btm_serial_api_stub)
    monkeypatch.setattr(ball_thrower_api, "ball_thrower", ball_thrower_stub, raising=True)

    power = {'shot_power': VAL}
    response = client.put( "/api/v1/ball_thrower/power", json=power, headers=superuser_token_headers)
    assert response.status_code == 200 
    assert response.json() == power 

    # value validation 
    power = {'shot_power': -1}
    response = client.put( "/api/v1/ball_thrower/power", json=power, headers=superuser_token_headers)
    assert response.status_code == 422 
    power = {'shot_power': 101}
    response = client.put( "/api/v1/ball_thrower/power", json=power, headers=superuser_token_headers)
    assert response.status_code == 422 