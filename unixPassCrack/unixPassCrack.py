import argparse
from passlib.hash import sha512_crypt


def test_pass(crypt_pass, password):
    try:
        # Extract the salt from the stored hash
        salt = crypt_pass.split('$')[2]

        # Hash the password using the extracted salt
        hashed_password = sha512_crypt.using(salt=salt).hash(password)

        # Compare the hashed password with the stored hash
        print("hashed_password:", hashed_password)
        print("crypt_pass:", crypt_pass)
        if hashed_password == crypt_pass:
            return "[+] Found PASSWORD: " + password

    except IndexError:
        pass  # Handle invalid or unsupported hash formats

    return ""

def main():
    parser = argparse.ArgumentParser(description="Crack passwords from shadow file using a dictionary attack")
    parser.add_argument("-f", dest="passfile", help="Path to shadow file", required=True)
    parser.add_argument("-d", dest="dictionary", help="Path to password dictionary", required=True)
    args = parser.parse_args()

    passfile = args.passfile
    dictionary = args.dictionary

    try:
        with open(passfile, "r") as pass_file:
            with open(dictionary, "r") as dict_file:
                pass_dict = dict_file.read().split("\n")

                for line in pass_file:
                    if ":" in line:
                        shadow_text = line.split(":")
                        user, crypt_pass = shadow_text[0], shadow_text[1]
                        print(f"[*] Cracking Password For: {user}")

                        for password in pass_dict[:-1]:
                            result = test_pass(crypt_pass.strip(), password)
                            print("Trying password: " + password)
                            if result:
                                print(result)
                                break

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

