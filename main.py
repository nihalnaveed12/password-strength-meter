import streamlit as st
import re
import random
import string
import pyperclip  # For copying text to clipboard

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    # Check length
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    # Check for uppercase letters
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Password should contain at least one uppercase letter.")

    # Check for lowercase letters
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Password should contain at least one lowercase letter.")

    # Check for digits
    if re.search(r'[0-9]', password):
        score += 1
    else:
        feedback.append("Password should contain at least one digit.")

    # Check for special characters
    if re.search(r'[!@#$%^&*]', password):
        score += 1
    else:
        feedback.append("Password should contain at least one special character (!@#$%^&*).")

    # Determine strength
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Moderate"
    else:
        strength = "Strong"

    return strength, score, feedback

# Function to generate a strong password
def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Common passwords blacklist
common_passwords = ["password", "123456", "qwerty", "admin", "letmein"]

# Streamlit app
st.set_page_config(page_title="Password Strength Meter", page_icon="🔒")

# Custom CSS for better UI
st.markdown(
    """
    <style>
    .stProgress > div > div > div > div {
        background-color: green;
    }
    .stSlider > div > div > div > div > div {
        background-color: white;
        padding: 1px 2px                       
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# App title and description
st.title("🔒 Password Strength Meter")
st.write("Check the strength of your password and get suggestions to improve it.")

# Password input with visibility toggle
password = st.text_input("Enter your password:", type="password", placeholder="Type your password here...", key="password_input")

# Real-time feedback
if password:
    if password.lower() in common_passwords:
        st.error("🚨 This password is too common. Please choose a stronger one.")
    else:
        strength, score, feedback = check_password_strength(password)
        
        # Display strength with a color-coded progress bar
        
        st.write("### Password Strength Progress:")
        if strength == "Weak":
            st.progress(score / 5)
        elif strength == "Moderate":
            st.progress(score / 5)
        else:
            st.progress(score / 5)
        
        st.write("### Password Strength Score:")
        if strength == "Weak":
           st.warning(f"🚨 {strength} Password - This Password can be more secure") 
        elif strength == "Moderate":
            st.warning(f"🚨 {strength} Password - This Password can be more secure") 
            
        # Display feedback
        if feedback:
            st.write("### 📝 Suggestions to improve your password:")
            for suggestion in feedback:
                st.write(f"- {suggestion}")
        else:
            st.success("🎉 Your password is strong! Good job!")

# Password generator
st.write("---")
st.write("### 🔑 Generate a Strong Password")
password_length = st.slider("Select password length", min_value=8, max_value=20, value=12)
if st.button("Generate Strong Password"):
    strong_password = generate_strong_password(password_length)
    st.session_state.generated_password = strong_password  # Store password in session state
    st.code(strong_password, language="text")

# Copy to clipboard button
if "generated_password" in st.session_state:
    if st.button("Copy to Clipboard"):
        pyperclip.copy(st.session_state.generated_password)
        st.success("Password copied to clipboard!")

if "password_history" not in st.session_state:
    st.session_state.password_history = []

if password:
    st.session_state.password_history.append(password)
    if len(st.session_state.password_history) > 5:
        st.session_state.password_history.pop(0)

st.write("---")
st.write("### 📜 Recent Passwords")
for pwd in st.session_state.password_history:
    st.write(f"- {pwd}")

# Footer
st.write("---")
st.write("*Nihal Naveed Password Strength Meter*") 
