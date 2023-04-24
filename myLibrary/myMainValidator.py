import re

class MainValidation:
    @staticmethod
    def is_valid_email(email):
        """
        Check if email is valid
        """
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return True
        return False
    
    @staticmethod
    def is_strong_password(password):
        """
        Check if password is strong
        """
        if re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
            return True
        return False
    
    @staticmethod
    def is_valid_phone(phone):
        """
        Check if phone number is valid
        """
        if re.match(r'^\+?\d{9,15}$', phone):
            return True
        return False
    
    @staticmethod
    def is_valid_age(age):
        """
        Check if age is valid
        """
        if age > 0 and age < 150:
            return True
        return False
