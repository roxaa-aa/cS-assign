import hmac as _hmac

s_box = [
    0xC,
    0x5,
    0x6,
    0xB,
    0x9,
    0x0,
    0xA,
    0xD,
    0x3,
    0xE,
    0xF,
    0x8,
    0x7,
    0x1,
    0x2,
    0x4,
]


def substitution_byte(b: int) -> int:
    hi = (b >> 4) & 0x0F
    lo = b & 0x0F
    return (s_box[hi] << 4) | s_box[lo]


p_box = [3, 0, 6, 2, 7, 1, 5, 4]


def permute_byte(b: int) -> int:
    out = 0
    for out_ind, in_ind in enumerate(p_box):
        bit = (b >> in_ind) & 1
        out |= bit << out_ind
    return out


def rotL32(val: int, shift: int) -> int:
    shift = shift % 32
    return (val << shift) | (val >> (32 - shift) & 0xFFFFFFFF)


def hash_bytes(data: bytes) -> str:
    state = 0x6A09E667
    padded = bytearray(data)
    padded.append(0x80)
    msg_len = len(data) & 0xFF
    padded.append(msg_len)

    for ind, byte_val in enumerate(padded):
        sub_val = substitution_byte(byte_val)
        perm_val = permute_byte(sub_val)
        state = (state ^ (perm_val << ((ind % 4) * 8))) & 0xFFFFFFFF

        for r in range(4):
            shift_mix = ((state << 5) ^ (state >> 3)) & 0xFFFFFFFF
            state = (state + shift_mix + 0x9E3779B9) & 0xFFFFFFFF
            state = rotL32(state, 13)
            state ^= state >> 16

    return f"{state:08x}"


def hash(message: str) -> str:
    return hash_bytes(message.encode("utf-8"))


BLOCK_SIZE = 64
IPAD = 0x36
OPAD = 0x5C


def _prepare_key(key: bytes) -> bytes:
    if len(key) > BLOCK_SIZE:
        key = hash_bytes(key).encode("ascii")
    return key.ljust(BLOCK_SIZE, b"\x00")


def mac(key: bytes, message: str) -> str:
    k = _prepare_key(key)
    inner_key = bytes(b ^ IPAD for b in k)
    outer_key = bytes(b ^ OPAD for b in k)

    inner_digest = hash_bytes(inner_key + message.encode("utf-8"))
    return hash_bytes(outer_key + inner_digest.encode("ascii"))


def verify(key: bytes, message: str, tag: str) -> bool:
    return _hmac.compare_digest(mac(key, message), tag)


if __name__ == "__main__":
    msg1 = "Hello, world!"
    msg2 = "Hello, world!"
    msg3 = "Hello. world!"

    key = b"shared-secret-key"
    wrong_key = b"attacker-guess"

    print(hash(msg1))
    print(hash(msg2))
    print(hash(msg3))

    tag1 = mac(key, msg1)
    tag2 = mac(key, msg2)
    tag3 = mac(key, msg3)
    print(tag1)
    print(tag2)
    print(tag3)
    print(mac(wrong_key, msg1))

    print(verify(key, msg1, tag1))
    print(verify(key, msg3, tag1))
    print(verify(wrong_key, msg1, tag1))
