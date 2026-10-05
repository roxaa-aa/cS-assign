def ceaser_encrpytion(pt: str, shift: int) -> str:
    ct = []
    shift = shift % 26

    for char in pt:
        if char.isupper():
            ct.append(chr((ord(char) - ord("A") + shift) % 26 + ord("A")))
        elif char.islower():
            ct.append(chr((ord(char) - ord("a") + shift) % 26 + ord("a")))
        else:
            ct.append(char)
    return "".join(ct)


def main():
    message = input("Enter the message to be encrypted: ")
    while True:
        try:
            key = int(input("Enter the keyshift (1 - 25): "))
            if 1 <= key <= 25:
                break
            else:
                print("Please enter a number between 1 and 25.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 25.")
    encryptedText = ceaser_encrpytion(message, key)

    with open("encrypted_message.txt", "w", encoding="utf-8") as file:
        file.write(encryptedText)

    print("Message encrypted and saved to 'encrypted_message.txt'")
    print(f"Encrypted text is: {encryptedText}")


if __name__ == "__main__":
    main()
