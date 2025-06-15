import streamlit as st
import hashlib
import json
import os
from pathlib import Path

# User Authentication Classes (Same as your original)
class User:
    def __init__(self, username, password_hash, salt):
        self.username = username
        self.password_hash = password_hash
        self.salt = salt
    
    def verify_password(self, password):
        """Verify if the provided password matches the stored hash"""
        new_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            self.salt.encode('utf-8'),
            100000
        ).hex()
        return new_hash == self.password_hash

class UserManager:
    def __init__(self, data_file='users.json'):
        self.data_file = data_file
        self.users = {}
        self.load_users()
    
    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                try:
                    data = json.load(f)
                    for username, user_data in data.items():
                        self.users[username] = User(
                            username=username,
                            password_hash=user_data['password_hash'],
                            salt=user_data['salt']
                        )
                except json.JSONDecodeError:
                    self.users = {}
    
    def save_users(self):
        """Save users to JSON file"""
        data = {}
        for username, user in self.users.items():
            data[username] = {
                'password_hash': user.password_hash,
                'salt': user.salt
            }
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)
    
    def register(self, username, password):
        """Register a new user"""
        if username in self.users:
            return False, "Username already exists"
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        
        # Generate salt and hash the password
        salt = os.urandom(16).hex()
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        
        # Create and store the new user
        self.users[username] = User(username, password_hash, salt)
        self.save_users()
        return True, "Registration successful"
    
    def login(self, username, password):
        """Authenticate a user"""
        if username not in self.users:
            return False, "Username not found"
        
        user = self.users[username]
        if user.verify_password(password):
            return True, "Login successful"
        else:
            return False, "Incorrect password"

# Streamlit App Integration
def main():
    st.set_page_config(
        page_title="EatS Health Tracker",
        page_icon="🏋️",
        layout="centered"
    )
    
    user_manager = UserManager()
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    
    # Login/Register Section
    if not st.session_state.authenticated:
        st.title("EatS Health Tracker")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form"):
                st.subheader("Login")
                login_username = st.text_input("Username", key="login_username")
                login_password = st.text_input("Password", type="password", key="login_password")
                login_submitted = st.form_submit_button("Login")
                
                if login_submitted:
                    success, message = user_manager.login(login_username, login_password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.username = login_username
                        st.rerun()
                    else:
                        st.error(message)
        
        with tab2:
            with st.form("register_form"):
                st.subheader("Register")
                reg_username = st.text_input("Username", key="reg_username")
                reg_password = st.text_input("Password", type="password", key="reg_password")
                reg_submitted = st.form_submit_button("Register")
                
                if reg_submitted:
                    success, message = user_manager.register(reg_username, reg_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
    
    # Main App (After Authentication)
    else:
        st.title(f"Welcome, {st.session_state.username}!")
        
        # Logout button
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()
        
        # Main App Navigation
        st.subheader("Health Trackers")
        
        cols = st.columns(3)
        with cols[0]:
            if st.button("Food Tracker 🍽️"):
                st.switch_page("food/food.py")
        with cols[1]:
            if st.button("Sleep Tracker 😴"):
                st.switch_page("sleep/app.py")
        with cols[2]:
            if st.button("BMI Tracker ⚖️"):
                st.switch_page("bmi.py")
        
        # User Profile Section
        with st.expander("Profile Settings"):
            st.write(f"Logged in as: {st.session_state.username}")
            if st.button("Change Password"):
                # Implement password change functionality
                st.info("Password change feature coming soon!")

if __name__ == "__main__":
    main()
