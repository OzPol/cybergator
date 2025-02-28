import unittest
from unittest.mock import patch, ANY
from app.services.auth_service import hash_password, check_password, signup, login, delete_user
from app.models.user_model import User

class TestAuthService(unittest.TestCase):
    ### ENCRYPTION TESTS ###
    def test_hash_password(self):
        password = "securepassword"
        hashed = hash_password(password)

        self.assertNotEqual(hashed, password)
        self.assertTrue(hashed.startswith("$2b$"))

    def test_check_password(self):
        password = "securepassword"
        hashed = hash_password(password)

        self.assertTrue(check_password(password, hashed))
        self.assertFalse(check_password("wrongpassword", hashed))
        
    ### SIGNUP TESTS ###
    @patch("app.services.auth_service.get_user_by_username", return_value=None)
    @patch("app.services.auth_service.create_user")
    def test_signup_success(self, mock_create_user, mock_get_user):
        """Ensure signup works correctly with mocked DB calls"""

        mock_create_user.return_value = User(id=1, username="userpytest", password="hashedpass")

        response = signup("userpytest", "password123")

        self.assertIsInstance(response, User)
        self.assertEqual(response.username, "userpytest")

        mock_get_user.assert_called_once_with("userpytest")

        mock_create_user.assert_called_once_with(ANY)
        created_user = mock_create_user.call_args[0][0]
        self.assertEqual(created_user.username, "userpytest")
        
    @patch("app.services.auth_service.get_user_by_username")
    def test_signup_user_already_exists(self, mock_get_user):
        """Ensure signup prevents duplicate users"""

        mock_get_user.return_value = User(id=1, username="existinguser", password="hashedpass")

        response = signup("existinguser", "password123")

        self.assertEqual(response, {"error": "Username already exists"})
        mock_get_user.assert_called_once_with("existinguser")
        
    ### LOGIN TESTS ###
    @patch("app.services.auth_service.get_user_by_username", return_value=None)
    def test_login_user_not_found(self, mock_get_user):
        """Ensure login fails for non-existent users"""

        response = login("nonexistent", "password123")

        self.assertEqual(response, {"error": "User not found"})
        mock_get_user.assert_called_once_with("nonexistent")

    @patch("app.services.auth_service.get_user_by_username")
    def test_login_invalid_password(self, mock_get_user):
        """Ensure login fails if the password is incorrect"""

        valid_hashed_password = hash_password("correctpassword")
        mock_get_user.return_value = User(id=1, username="testuser", password=valid_hashed_password)

        response = login("testuser", "wrongpassword")

        self.assertEqual(response, {"error": "Invalid credentials"})
        mock_get_user.assert_called_once_with("testuser")

    @patch("app.services.auth_service.get_user_by_username")
    @patch("app.services.auth_service.check_password", return_value=True)
    def test_login_success(self, mock_check_password, mock_get_user):
        """Ensure login succeeds when credentials match"""

        hashed_password = hash_password("password123")
        mock_get_user.return_value = User(id=1, username="testuser", password=hashed_password)

        response = login("correctuser", "password123")

        self.assertEqual(response, {"message": "Login successful"})
        mock_get_user.assert_called_once_with("correctuser")
        mock_check_password.assert_called_once_with("password123", hashed_password)
        
    ### DELETE USER TESTS ###
    @patch("app.services.auth_service.delete_user_by_id")
    def test_delete_user(self, mock_delete_user_by_id):
        """Ensure user deletion is handled correctly"""

        mock_delete_user_by_id.return_value = {"message": "User deleted"}

        response = delete_user(1)

        self.assertEqual(response, {"message": "User deleted"})
        mock_delete_user_by_id.assert_called_once_with(1)
        
    @patch("app.services.auth_service.delete_user_by_id")
    def test_delete_non_existent_user(self, mock_delete_user_by_id):
        """Ensure attempting to delete a non-existent user returns an error"""

        mock_delete_user_by_id.return_value = {"error": "User not found"}

        response = delete_user(999) 

        self.assertEqual(response, {"error": "User not found"})
        mock_delete_user_by_id.assert_called_once_with(999)

if __name__ == "__main__":
    unittest.main()

