import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, session

from app.controllers.auth_controller import auth_bp
from app.models.user_model import User

class TestAuthController(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Set up a test Flask app"""
        cls.app = Flask(__name__)
        cls.app.secret_key = "test_secret" 
        cls.app.register_blueprint(auth_bp)
        cls.client = cls.app.test_client()

    ### SIGNUP TESTS ###
    @patch("app.controllers.auth_controller.signup")
    def test_signup_success(self, mock_signup):
        """Ensure /signup works correctly"""
        
        mock_user = MagicMock(spec=User)
        mock_user.to_dict.return_value = {"id": 1, "username": "testuser"}

        mock_signup.return_value = mock_user  

        response = self.client.post("/signup", json={"username": "testuser", "password": "password123"})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"id": 1, "username": "testuser"})

        mock_signup.assert_called_once_with("testuser", "password123")

    @patch("app.controllers.auth_controller.signup") 
    def test_signup_existing_user(self, mock_signup):
        """Ensure /signup returns an error if the username already exists"""
        mock_signup.return_value = {"error": "Username already exists"}

        response = self.client.post("/signup", json={"username": "existinguser", "password": "password123"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Username already exists"})

        mock_signup.assert_called_once_with("existinguser", "password123")
        
    @patch("app.controllers.auth_controller.signup")
    def test_signup_missing_fields(self, mock_signup):
        """Ensure /api/auth/signup returns an error if username or password is missing"""
        response = self.client.post("/signup", json={"username": ""})  

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Username and password are required"})

        response = self.client.post("/signup", json={"password": "password123"})  

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Username and password are required"})

        mock_signup.assert_not_called()
        
    ### LOGIN TESTS ###
    @patch("app.controllers.auth_controller.login")
    def test_login_success(self, mock_login):
        """Ensure /api/auth/login works correctly"""
        mock_login.return_value = {"message": "Login successful"}

        with self.client.session_transaction() as sess:
            sess.clear()  # Ensure no user is logged in before test

        response = self.client.post("/login", json={"username": "testuser", "password": "password123"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Login successful"})

        mock_login.assert_called_once_with("testuser", "password123")

    @patch("app.controllers.auth_controller.login")
    def test_login_invalid_credentials(self, mock_login):
        """Ensure /api/auth/login returns an error for invalid credentials"""
        mock_login.return_value = {"error": "Invalid credentials"}

        with self.client.session_transaction() as sess:
            sess.clear()  # Ensure no user is logged in before the test

        response = self.client.post("/login", json={"username": "testuser", "password": "wrongpassword"})

        self.assertEqual(response.status_code, 401)  
        self.assertEqual(response.json, {"error": "Invalid credentials"})

        mock_login.assert_called_once_with("testuser", "wrongpassword")

    def test_login_already_logged_in(self):
        """Ensure /api/auth/login returns an error if user is already logged in"""
        with self.client.session_transaction() as sess:
            sess["user"] = "testuser"  # Simulate logged-in user

        response = self.client.post("/login", json={"username": "testuser", "password": "password123"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "you are already logged in."})

    @patch("app.controllers.auth_controller.login")
    def test_login_missing_fields(self, mock_login):
        """Ensure /api/auth/login returns an error if username or password is missing"""
        response = self.client.post("/login", json={"username": ""})  # Missing password
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Username and password are required"})

        response = self.client.post("/login", json={"password": "password123"})  # Missing username
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Username and password are required"})

        mock_login.assert_not_called()
        
    ### SESSION TESTS (/me) ###
    def test_get_current_user_logged_in(self):
        """Ensure /api/auth/me returns the logged-in user"""
        with self.client.session_transaction() as sess:
            sess["user"] = "testuser"

        response = self.client.get("/me")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"username": "testuser"})

    def test_get_current_user_not_logged_in(self):
        """Ensure /api/auth/me returns an error if no user is logged in"""
        with self.client.session_transaction() as sess:
            sess.clear()  # Ensure session is empty

        response = self.client.get("/me")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {"error": "User not logged in"})
        
    ### LOGOUT TESTS ###
    def test_logout_success(self):
        """Ensure /api/auth/logout works correctly"""
        with self.client.session_transaction() as sess:
            sess["user"] = "testuser"  

        response = self.client.post("/logout")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Logout successful"})

    def test_logout_not_logged_in(self):
        """Ensure /api/auth/logout returns an error if no user is logged in"""
        with self.client.session_transaction() as sess:
            sess.clear() 

        response = self.client.post("/logout")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {"error": "User not logged in"})
        
    ### DELETE USER TESTS ###
    @patch("app.controllers.auth_controller.delete_user")
    def test_delete_user_success(self, mock_delete_user):
        """Ensure /api/auth/user/<id> deletes a user successfully"""
        mock_delete_user.return_value = {"message": "User deleted"}

        response = self.client.delete("/user/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "User deleted"})

        mock_delete_user.assert_called_once_with(1)

    @patch("app.controllers.auth_controller.delete_user")
    def test_delete_non_existent_user(self, mock_delete_user):
        """Ensure /api/auth/user/<id> returns an error if user does not exist"""
        mock_delete_user.return_value = {"error": "User not found"}

        response = self.client.delete("/user/999")  

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "User not found"})

        mock_delete_user.assert_called_once_with(999)

if __name__ == "__main__":
    unittest.main()
