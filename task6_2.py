import os


def ceaser_decryption(ct: str, shift: int) -> str:
    pt = []
    shift = shift % 26

    for char in ct:
        if char.isupper():
            pt.append(chr((ord(char) - ord("A") - shift) % 26 + ord("A")))
        elif char.islower():
            pt.append(chr((ord(char) - ord("a") - shift) % 26 + ord("A")))
        else:
            pt.append(char)

    return "".join(pt)


def scr_eng(txt: str) -> int:
    common = {
        "the",
        "be",
        "to",
        "and",
        "of",
        "a",
        "an",
        "in",
        "that",
        "this",
        "have",
        "had",
        "has",
        "i",
        "it",
        "for",
        "not",
        "on",
        "with",
        "he",
        "she",
        "they",
        "them",
        "as",
        "him",
        "her",
        "you",
        "do",
        "at",
        "is",
        "im",
    }
    words = txt.lower().split()
    return sum(1 for word in words if word.strip(".,!?\"'") in common)


def main():
    file_path = "encrypted_message.txt"
    if not os.path.exists(file_path):
        print(f"Error: '{file_path} not found in current folder")
        return

    with open(file_path, "r", encoding="utf-8") as file:
        ct = file.read().strip()

    print(f"Read encrypted text: {ct}")
    print("Testing all possible keys:")

    best = None
    best_score = -1
    best_text = ""

    for key in range(1, 26):
        decrypted = ceaser_decryption(ct, key)
        scr = scr_eng(decrypted)

        print(f"Key {key:02d}: {decrypted}")

        if scr > best_score:
            best_score = scr
            best = key
            best_text = decrypted

    print(" - - - - - - -")

    if best_score > 0:
        print(f"Most likely plaintext (key {best}): '{best_text}")
    else:
        print("Manually pick out the most reasonable plaintext.")


if __name__ == "__main__":
    main()
