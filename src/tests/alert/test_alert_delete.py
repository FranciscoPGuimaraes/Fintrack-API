import pytest
import requests
from tests.utils.test_utils import (
    BASE_URL,
    register_user,
    add_alert,
    delete_alert,
    generate_random_email,
    generate_random_date,
)

# ------------------------------------------------------------------------------------------------------------

# Tests with the alert deletion endpoint


# Error test - missing email query parameter
def test_alert_delete_missing_email():
    """
    Tests if the delete endpoint returns a 400 error when the required 'email' parameter is missing.
    """
    response = requests.delete(f"{BASE_URL}/delete/alert")
    assert (
        response.status_code == 400
    ), f"Expected 400 for missing email parameter, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "The 'email' parameter is required." in json_response["detail"]


# Error test - nonexistent email
def test_alert_delete_nonexistent_email():
    """
    Tests if the delete endpoint returns a 404 error for an email that does not exist in the database.
    """
    params = {"email": "nonexistent@example.com"}
    response = delete_alert(params)
    assert (
        response.status_code == 404
    ), f"Expected 404 for nonexistent email, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Email not found" in json_response["detail"]


# Error test - invalid email format
def test_alert_delete_invalid_email_format():
    """
    Tests if the delete endpoint returns a 400 error when the email is not in a valid format.
    """
    params = {"email": "invalidemailformat"}
    response = delete_alert(params)
    assert (
        response.status_code == 400
    ), f"Expected 400 for invalid email format, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert (
        "The email must be in the format 'name@domain.com' or 'name@domain.br'."
        in json_response["detail"]
    )


# Success test - delete alert with valid email
def test_alert_delete_success():
    """
    Tests if the delete endpoint successfully deletes an alert for a valid registered email.
    """
    # Register a user to test alert deletion
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "User registration failed during alert deletion test."

    # Add alert data for the registered user
    date = generate_random_date()
    add_alert_data = {
        "email_id": email,
        "item_type": "Saldo Negativo",
        "value": 50.00,
        "annotation": "Saldo abaixo do limite",
        "date": date,
    }
    add_alert_response = add_alert(add_alert_data)
    assert (
        add_alert_response.status_code == 200
    ), f"Expected status 200, got {add_alert_response.status_code}"

    # Valid delete key
    params = {"email": email}
    response = delete_alert(params)
    assert (
        response.status_code == 200
    ), f"Expected 200 for successful alert deletion, got {response.status_code}"
    json_response = response.json()
    assert "message" in json_response
    assert "Alert deleted successfully." in json_response["message"]


# Method not allowed test
@pytest.mark.parametrize("method", ["post", "put", "get", "patch"])
def test_alert_delete_disallowed_methods(method):
    """
    Tests if methods other than DELETE return a 405 error for the alert deletion endpoint.
    """
    response = getattr(requests, method)(f"{BASE_URL}/delete/alert")
    assert (
        response.status_code == 405
    ), f"Expected 405 for {method.upper()}, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
