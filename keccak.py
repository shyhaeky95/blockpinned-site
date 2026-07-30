#!/usr/bin/env python3
"""keccak256 thuần thư viện chuẩn — để `build.py` tự sinh selector từ CHỮ KÝ hàm.

VÌ SAO KHÔNG DÙNG THƯ VIỆN: bộ sinh site phải dựng được bằng Python trắng, vì repo
công khai là thứ người khác clone về chạy lại. Thêm `eth_hash` vào đây là thêm một
bước cài đặt vào giữa "tôi nói bạn kiểm được" và "bạn kiểm được".

VÌ SAO KHÔNG GÕ CỨNG SELECTOR: một selector gõ tay sai vẫn là 4 byte hợp lệ. Nó sẽ
gọi một hàm KHÁC (hoặc không hàm nào) và trả về số 0 hoặc revert — tức lỗi hiện ra
như "số liệu", không như lỗi. Sinh từ chữ ký thì cái người đọc thấy trên trang
(`getModuleValidatorsBalance(uint256)`) và cái thật sự được gọi là MỘT thứ.

🔴 `hashlib.sha3_256` KHÔNG phải keccak256 — khác nhau đúng một byte padding (0x06 so
với 0x01), và nó là chỗ người ta sai nhiều nhất khi làm việc này bằng stdlib.

Tự kiểm chạy ngay lúc import: 5 vector đã biết. Sai một cái là NỔ, không cảnh báo.
"""

_RC = (0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
       0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
       0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
       0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
       0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
       0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008)
_R = ((0, 36, 3, 41, 18),
      (1, 44, 10, 45, 2),
      (62, 6, 43, 15, 61),
      (28, 55, 25, 21, 56),
      (27, 20, 39, 8, 14))
_M = (1 << 64) - 1
_RATE = 136                      # keccak256: 1600 − 2×256 bit = 1088 bit = 136 byte


def _rol(x: int, n: int) -> int:
    return ((x << n) | (x >> (64 - n))) & _M


def _keccak_f(A: list) -> list:
    for rnd in range(24):
        C = [A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4] for x in range(5)]
        D = [C[(x - 1) % 5] ^ _rol(C[(x + 1) % 5], 1) for x in range(5)]
        A = [[A[x][y] ^ D[x] for y in range(5)] for x in range(5)]
        B = [[0] * 5 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                B[y][(2 * x + 3 * y) % 5] = _rol(A[x][y], _R[x][y])
        A = [[B[x][y] ^ ((~B[(x + 1) % 5][y]) & B[(x + 2) % 5][y] & _M)
              for y in range(5)] for x in range(5)]
        A[0][0] ^= _RC[rnd]
    return A


def keccak256(data: bytes) -> bytes:
    m = bytearray(data)
    m.append(0x01)                          # padding của KECCAK (sha3 dùng 0x06)
    while len(m) % _RATE:
        m.append(0x00)
    m[-1] ^= 0x80
    A = [[0] * 5 for _ in range(5)]
    for off in range(0, len(m), _RATE):
        blk = m[off:off + _RATE]
        for i in range(_RATE // 8):
            A[i % 5][i // 5] ^= int.from_bytes(blk[i * 8:(i + 1) * 8], "little")
        A = _keccak_f(A)
    return b"".join(A[i % 5][i // 5].to_bytes(8, "little") for i in range(4))[:32]


def selector(ky: str) -> str:
    """4 byte đầu của keccak256(chữ ký hàm) — ví dụ 'owner()' → '0x8da5cb5b'."""
    return "0x" + keccak256(ky.encode()).hex()[:8]


# ── TỰ KIỂM: chạy lúc import, sai là chết ngay chứ không đi tiếp ────────────────
_VECTOR = [
    (b"", "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"),
    (b"abc", "4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45"),
]
_SELECTOR = [("owner()", "0x8da5cb5b"),                     # control của script desk
             ("totalSupply()", "0x18160ddd"),
             ("transfer(address,uint256)", "0xa9059cbb")]
for _d, _h in _VECTOR:
    if keccak256(_d).hex() != _h:
        raise SystemExit(f"🔴 keccak256 SAI trên vector {_d!r} — không được dùng để sinh selector")
for _k, _s in _SELECTOR:
    if selector(_k) != _s:
        raise SystemExit(f"🔴 selector('{_k}') = {selector(_k)}, phải là {_s}")


if __name__ == "__main__":
    import sys
    print("✅ 5/5 vector tự kiểm đạt")
    for a in sys.argv[1:]:
        print(f"  {a:44} → {selector(a)}")
