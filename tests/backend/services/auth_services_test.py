import pytest
from app.services.auth_service import hash_password, check_password, signup, login, delete_user
from app.models.user_model import User

### ENCRYPTION TESTS ###
def test_hash_password():
    password = "securepassword"
    hashed = hash_password(password)

    assert hashed != password
    
    # Ensure the hash is a valid bcrypt hash (starts with "$2b$")
    assert hashed.startswith("$2b$")

def test_check_password():
    password = "securepassword"
    hashed = hash_password(password)

    assert check_password(password, hashed)
    assert not check_password("wrongpassword", hashed)

@pytest.fixture
def mock_user():
    # mocks a User entity
    return User(id=1, username="testuser", password="hashedpass")

### SIGNUP TESTS ###
def test_signup_success(mocker, mock_user):
    # mocks functions
    mock_get_user = mocker.patch("app.services.auth_service.get_user_by_username", return_value=None)
    mock_create_user = mocker.patch("app.services.auth_service.create_user", return_value=mock_user)

    response = signup("testuser", "password123")

    assert isinstance(response, User)
    assert response.username == "testuser"

    mock_get_user.assert_called_once_with("testuser")
    mock_create_user.assert_called_once()
    
def test_signup_user_already_exists(mocker):
    mocker.patch("app.services.auth_service.get_user_by_username", return_value=User(id=1, username="existinguser", password="hashedpass"))
    
    response = signup("existinguser", "password123")
    assert response == {"error": "Username already exists"}

### LOGIN TESTS ###
def test_login_user_not_found(mocker):
    mocker.patch("app.services.auth_service.get_user_by_username", return_value=None)

    response = login("nonexistent", "password123")
    assert response == {"error": "User not found"}

def test_login_invalid_password(mocker):
    valid_hashed_password = hash_password("correctpassword")

    mocker.patch("app.services.auth_service.get_user_by_username", return_value=User(id=1, username="testuser", password=valid_hashed_password))

    response = login("testuser", "wrongpassword")
    assert response == {"error": "Invalid credentials"}

def test_login_success(mocker):
    hashed_password = "$2b$12$hashedpasswordstring"
    mocker.patch("app.services.auth_service.get_user_by_username", return_value=User(id=1, username="testuser", password=hashed_password))
    mocker.patch("app.services.auth_service.check_password", return_value=True)

    response = login("testuser", "password123")
    assert response == {"message": "Login successful"}

### DELETION TESTS ###
def test_delete_user(mocker):
    mocker.patch("app.services.auth_service.delete_user_by_id", return_value={"message": "User deleted"})
    
    response = delete_user(1)
    assert response == {"message": "User deleted"}