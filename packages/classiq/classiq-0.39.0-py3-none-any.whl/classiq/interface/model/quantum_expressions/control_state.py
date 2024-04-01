from classiq.exceptions import ClassiqValueError


def min_unsigned_bit_length(number: int) -> int:
    if number < 0:
        raise ClassiqValueError(
            f"Quantum register is not signed but control value "
            f"'{number}' is negative"
        )
    return 1 if number == 0 else number.bit_length()


def min_signed_bit_length(number: int) -> int:
    pos_val = abs(number)
    is_whole = pos_val & (pos_val - 1) == 0
    if number <= 0 and is_whole:
        return min_unsigned_bit_length(pos_val)
    return min_unsigned_bit_length(pos_val) + 1


def min_bit_length(number: int, is_signed: bool) -> int:
    return (
        min_signed_bit_length(number) if is_signed else min_unsigned_bit_length(number)
    )


def to_twos_complement(value: int, bits: int, is_signed: bool) -> str:
    required_bits = min_bit_length(value, is_signed)
    if bits < required_bits:
        raise ClassiqValueError(
            f"Cannot express '{value}' using {bits} bits: "
            f"at least {required_bits} bits are required"
        )
    if value >= 0:
        return bin(value)[2:].zfill(bits)[::-1]
    mask = (1 << bits) - 1
    value = (abs(value) ^ mask) + 1
    return bin(value)[:1:-1].rjust(bits, "1")
