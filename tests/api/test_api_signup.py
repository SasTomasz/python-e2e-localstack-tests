import pytest
import os
from api.post_sign_up import SignUp
from dotenv import load_dotenv
import requests
from api.data.register import RegisterRequestDto  # Import the dataclass
from generators.user_generator import get_random_user  # Import the user generator

load_dotenv()

@pytest.fixture
def sign_up_api():
    return SignUp()

def test_successful_api_signup(sign_up_api: SignUp):
    user_data = get_random_user()
    response = sign_up_api.api_call(user_data)
    try:
        response.raise_for_status()
        assert response.status_code == 201, "Expected status code 201"
        assert response.json()['token'] is not None, "Token should not be None"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"HTTPError occurred: {str(e)}")

def test_should_return_400_for_too_short_username(sign_up_api: SignUp):
    user_data = get_random_user()
    user_data.username = "ad"  # Too short
    try:
        sign_up_api.api_call(user_data)
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 400, "Expected status code 400 for too short username"

def test_should_return_400_for_too_short_password(sign_up_api: SignUp):
    user_data = get_random_user()
    user_data.password = "123"  # Too short
    try:
        sign_up_api.api_call(user_data)
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 400, "Expected status code 400 for too short password"

def test_should_return_400_for_invalid_email(sign_up_api: SignUp):
    user_data = get_random_user()
    user_data.email = "not-an-email"  # Invalid email format
    try:
        sign_up_api.api_call(user_data)
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 400, "Expected status code 400 for invalid email"

# Response code should be 400 or 422 but actually is 500
def test_should_return_400_for_unsupported_role(sign_up_api: SignUp):
    user_data = get_random_user()
    user_data.roles = ["UNSUPPORTED_ROLE"]  # Assuming this role is not supported
    try:
        sign_up_api.api_call(user_data)
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 400, "Expected status code 400 for unsupported role"

# Tests for 422 Unprocessable Entity
def test_should_return_422_for_existing_username(sign_up_api: SignUp):
    user_data = get_random_user()
    user_data.username = os.getenv("ADMIN_USERNAME")  # Known existing username
    try:
        sign_up_api.api_call(user_data)
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 422, "Expected status code 422 for existing username"

# Response code should be 400 or 422 but actually is 500
def test_should_return_422_for_existing_email(sign_up_api: SignUp):
    user_data = get_random_user()
    user_data.email = os.getenv("ADMIN_EMAIL")  # Known existing email
    try:
        sign_up_api.api_call(user_data)
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 422, "Expected status code 422 for existing email"