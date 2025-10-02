import random
import string
import re

def generate_password():
    """
    Generates a random password based on user-specified criteria.
    """
    print("\n--- Generate a New Password ---")
    try:
        length = int(input("Enter the desired password length (e.g., 12): "))
        if length <= 0:
            print("Password length must be a positive number.")
            return
    except ValueError:
        print("Invalid input. Please enter a number for the length.")
        return

    # Character sets
    use_lower = input("Include lowercase letters? (y/n): ").lower() == 'y'
    use_upper = input("Include uppercase letters? (y/n): ").lower() == 'y'
    use_digits = input("Include numbers? (y/n): ").lower() == 'y'
    use_symbols = input("Include symbols? (y/n): ").lower() == 'y'

    character_pool = ""
    if use_lower:
        character_pool += string.ascii_lowercase
    if use_upper:
        character_pool += string.ascii_uppercase
    if use_digits:
        character_pool += string.digits
    if use_symbols:
        character_pool += string.punctuation

    if not character_pool:
        print("\nError: You must select at least one character type.")
        return

    try:
        # Ensure the password is secure by using random.SystemRandom if available
        secure_random = random.SystemRandom()
        password = ''.join(secure_random.choice(character_pool) for _ in range(length))
        print("\n------------------------------------")
        print(f"  Generated Password: {password}")
        print("------------------------------------")
    except Exception as e:
        print(f"\nAn error occurred while generating the password: {e}")

def check_password_strength():
    """
    Assesses the strength of a given password and provides feedback.
    """
    print("\n--- Check Password Strength ---")
    password = input("Enter the password to check: ")

    if not password:
        print("Password cannot be empty.")
        return

    strength_score = 0
    feedback = []

    # 1. Length check
    if len(password) < 8:
        feedback.append("❌ Too short (less than 8 characters)")
    elif len(password) >= 12:
        strength_score += 2
        feedback.append("✅ Good length (12+ characters)")
    else:
        strength_score += 1
        feedback.append("✔️ Okay length (8-11 characters)")

    # 2. Character type checks
    if re.search(r'[a-z]', password):
        strength_score += 1
        feedback.append("✅ Contains lowercase letters")
    else:
        feedback.append("❌ Missing lowercase letters")

    if re.search(r'[A-Z]', password):
        strength_score += 1
        feedback.append("✅ Contains uppercase letters")
    else:
        feedback.append("❌ Missing uppercase letters")

    if re.search(r'\d', password):
        strength_score += 1
        feedback.append("✅ Contains numbers")
    else:
        feedback.append("❌ Missing numbers")

    if re.search(r'[\W_]', password): # \W matches any non-word character, _ is included for completeness
        strength_score += 1
        feedback.append("✅ Contains symbols")
    else:
        feedback.append("❌ Missing symbols")

    # Determine strength level based on score
    if strength_score <= 2:
        level = "Very Weak"
    elif strength_score <= 3:
        level = "Weak"
    elif strength_score == 4:
        level = "Medium"
    elif strength_score == 5:
        level = "Strong"
    else: # score of 6
        level = "Very Strong"

    print("\n--- Password Analysis ---")
    print(f"Strength Level: {level}")
    print("\nFeedback:")
    for item in feedback:
        print(f"- {item}")
    print("-------------------------")


def main_menu():
    """
    Displays the main menu and handles user input.
    """
    print("\n======================================")
    print("   Password Toolkit Main Menu")
    print("======================================")
    while True:
        print("\n1. Generate a secure password")
        print("2. Check password strength")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            generate_password()
        elif choice == '2':
            check_password_strength()
        elif choice == '3':
            print("Exiting the program. Stay secure!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()
