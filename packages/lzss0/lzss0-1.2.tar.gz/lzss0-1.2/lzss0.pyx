# I LOVE CYTHON <333

cdef extern from "lzss.h":
    ctypedef unsigned char uchar
    ctypedef unsigned int  uint

    cdef struct lzss_param:
        uint  EI
        uint  EJ
        uint  P
        uchar init_chr
    
    uint lzss_decompress(uchar* src, int srclen, uchar* dst, int dstlen, lzss_param param)
    uint lzss_compress(uchar* src, int srclen, uchar* dst, int dstlen, lzss_param param)

def decompress(zbytes: bytes, bytessz=-1, refsz=12, lensz=4, ini=0) -> bytes:
    if ((refsz + lensz) % 8) != 0:
        raise ValueError("Codefield sum MUST be divisible by 8")

    if bytessz == -1:
        bytessz = len(zbytes) * 4 # some arbitrary number

    __bytes = b"\0" * bytessz

    bytessz = lzss_decompress(zbytes[:len(zbytes)], len(zbytes), __bytes[:bytessz], bytessz, lzss_param(EI=refsz, EJ=lensz, P=(refsz + lensz)/8, init_chr=ini))

    if bytessz == 0:
        raise ValueError("Bad decompression")

    _bytes = bytearray(b"\0" * bytessz)
    for i in range(bytessz):
        _bytes[i] = __bytes[i]

    return bytes(_bytes)

def compress(_bytes: bytes, refsz=12, lensz=4, ini=0) -> bytes:
    if ((refsz + lensz) % 8) != 0:
        raise ValueError("Codefield sum MUST be divisible by 8")

    _zbytes = b"\0" * len(_bytes)

    zbytessz = lzss_compress(_bytes[:len(_bytes)], len(_bytes), _zbytes[:len(_bytes)], len(_bytes), lzss_param(EI=refsz, EJ=lensz, P=(refsz + lensz)/8, init_chr=ini))

    if zbytessz == 0 or zbytessz >= len(_bytes):
        raise ValueError("Bad compression")

    zbytes = bytearray(b"\0" * zbytessz)
    for i in range(zbytessz):
        zbytes[i] = _zbytes[i]

    return bytes(zbytes)
