from passlib.hash import sha512_crypt

def test_pass(crypt_pass, password, salt):
    try:
        # Hash the password using the specified salt
        hashed_password = sha512_crypt.using(salt=salt).hash(password)

        # Compare the hashed password with the stored hash
        if hashed_password == crypt_pass:
            return "[+] Found PASSWORD: " + password

    except IndexError:
        pass  # Handle invalid or unsupported hash formats

    return ""

def main():
    user = "jeff"
    # Replace the following values with your actual hashed password and the password to test
    stored_hash = "$y$j9T$oUgaEKm0gzs6Pz.Dx/lTdU8y$.nVwmjXSmEhwU1kRSd8QhIcaBvrkLx8DxvxvgiWhMg9::0:99999:7:::"
    test_password = "34334"
    salt = "$y$j9T$oUgaEKm0gzs6Pz.Dx/lTdU8y$"

    try:
        print(f"[*] Cracking Password For: {user}")

        result = test_pass(stored_hash.strip(), test_password, salt)
        print(f"Trying password: {test_password}")

        if result:
            print(result)
        else:
            print("[-] Password not found")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
