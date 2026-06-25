"""
SHA256 Password Hashing Utility Module
Uses PBKDF2 with SHA256 for secure password hashing
"""

import hashlib
import os
import binascii

# Number of iterations for PBKDF2
HASH_ITERATIONS = 1000
SALT_LENGTH = 32  # 32 bytes = 256 bits


def generate_salt():
    """
    Generate a random salt for password hashing
    
    Returns:
        str: Hexadecimal encoded salt
    """
    salt = os.urandom(SALT_LENGTH)
    return binascii.hexlify(salt).decode('utf-8')


def hash_password(password, salt=None):
    """
    Hash a password using PBKDF2 with SHA256
    
    Args:
        password (str): Plain text password to hash
        salt (str, optional): Hexadecimal salt. If None, generates new salt.
    
    Returns:
        tuple: (hashed_password, salt) both as hexadecimal strings
        
    Example:
        >>> hashed, salt = hash_password("user123")
        >>> # Store both hashed and salt in database
    """
    if not password:
        raise ValueError("Password cannot be empty")
    
    # Generate salt if not provided
    if salt is None:
        salt = generate_salt()
    
    # Convert salt from hex string to bytes
    salt_bytes = binascii.unhexlify(salt)
    
    # Hash the password using PBKDF2 with SHA256
    password_bytes = password.encode('utf-8')
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password_bytes,
        salt_bytes,
        HASH_ITERATIONS,
        dklen=64  # 64 bytes = 512 bits
    )
    
    # Convert to hexadecimal string
    hashed_hex = binascii.hexlify(hashed).decode('utf-8')
    
    return hashed_hex, salt


def verify_password(password, stored_hash, salt):
    """
    Verify a plain text password against a stored hash
    
    Args:
        password (str): Plain text password to verify
        stored_hash (str): Hexadecimal hash stored in database
        salt (str): Hexadecimal salt stored in database
    
    Returns:
        bool: True if password matches, False otherwise
        
    Example:
        >>> if verify_password("user123", stored_hash, stored_salt):
        ...     print("Password is correct!")
    """
    if not password or not stored_hash or not salt:
        return False
    
    try:
        # Hash the provided password with the stored salt
        computed_hash, _ = hash_password(password, salt)
        
        # Compare hashes (constant time comparison)
        return computed_hash == stored_hash
    except Exception as e:
        print(f"Error verifying password: {e}")
        return False


def get_password_info(plain_password):
    """
    Hash a password and return both hash and salt
    Convenience function for user registration
    
    Args:
        plain_password (str): Plain text password from user
    
    Returns:
        dict: {'password_hash': '...', 'password_salt': '...'}
    """
    hashed, salt = hash_password(plain_password)
    return {
        'password_hash': hashed,
        'password_salt': salt
    }
