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


def hash(message: str) -> str:
    state = 0x6A09E667
    msg_bytes = message.encode("utf-8")
    padded = bytearray(msg_bytes)
    padded.append(0x80)
    msg_len = len(msg_bytes) & 0xFF
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


if __name__ == "__main__":
    msg1 = "Hello, world!"
    msg2 = "Hello, world!"
    msg3 = "Hello. world!"

    print(f"Input 1: '{msg1}'\nHash 1: '{hash(msg1)}'")
    print(f"Input 2: '{msg2}'\nHash 2: '{hash(msg2)}'")
    print(f"Input 3: '{msg3}'\nHash 3: '{hash(msg3)}'")
