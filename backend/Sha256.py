import hashlib

def texto_a_sha256(texto):
    sha256_hash = hashlib.sha256(texto.encode('utf-8')).hexdigest()
    return sha256_hash

# Ejemplo de uso
if __name__ == "__main__":
    texto = input("Introduce el texto a convertir a SHA256: ")
    print("SHA256:", texto_a_sha256(texto))