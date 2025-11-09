import math
import random
import hashlib
import numpy as np
from typing import Tuple, List

def sha256_hash(message: str) -> str:
    """
    Generate SHA256 hash of a message
    Args:
        message (str): Message to hash
    Returns:
        SHA256 hash of the message
    """
    return hashlib.sha256(message.encode()).hexdigest()

def caesar_encrypt(message: str, shift: int) -> str:
    """
    Encrypt a message using Caesar cipher
    Args:
        message (str): Message to encrypt
        shift (int): Number of positions to shift
    Returns:
        Encrypted message
    """
    encrypted = ""
    for char in message:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            encrypted += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            encrypted += char
    return encrypted

def caesar_decrypt(encrypted: str, shift: int) -> str:
    """
    Decrypt a Caesar cipher encrypted message
    Args:
        encrypted (str): Encrypted message
        shift (int): Number of positions that were shifted
    Returns:
        Decrypted message
    """
    return caesar_encrypt(encrypted, -shift)

def hill_encrypt(message: str, key_matrix: np.ndarray) -> str:
    """
    Encrypt a message using Hill cipher
    Args:
        message (str): Message to encrypt
        key_matrix (np.ndarray): 2x2 key matrix
    Returns:
        Encrypted message
    """
    # Pad message if needed
    if len(message) % 2 != 0:
        message += 'X'
    
    # Convert message to numbers (A=0, B=1, etc.)
    message_nums = [ord(c.upper()) - ord('A') for c in message if c.isalpha()]
    
    # Reshape into pairs
    pairs = np.array(message_nums).reshape(-1, 2)
    
    # Encrypt each pair
    encrypted_nums = []
    for pair in pairs:
        result = np.dot(key_matrix, pair) % 26
        encrypted_nums.extend(result)
    
    # Convert back to letters
    return ''.join([chr(num + ord('A')) for num in encrypted_nums])

def hill_decrypt(encrypted: str, key_matrix: np.ndarray) -> str:
    """
    Decrypt a Hill cipher encrypted message
    Args:
        encrypted (str): Encrypted message
        key_matrix (np.ndarray): 2x2 key matrix
    Returns:
        Decrypted message
    """
    # Calculate inverse matrix
    det = int(np.round(np.linalg.det(key_matrix)))
    det_inv = pow(det % 26, -1, 26)
    adj_matrix = np.array([[key_matrix[1, 1], -key_matrix[0, 1]],
                          [-key_matrix[1, 0], key_matrix[0, 0]]])
    inv_matrix = (det_inv * adj_matrix) % 26
    
    # Use inverse matrix to decrypt
    return hill_encrypt(encrypted, inv_matrix)