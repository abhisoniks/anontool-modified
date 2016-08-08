#!/usr/bin/env python
# @file         /home/mfukar/src/anontool/test/SHA512_test.py
# @author       Michael Foukarakis
# @version      1.0
# @date         Created:     Tue Feb 15, 2011 11:58 EET
#               Last Update: Tue Feb 15, 2011 11:59 EET
#------------------------------------------------------------------------
# Description:  SHA-384 and SHA-512 tests
#------------------------------------------------------------------------
# History:      None
# TODO:         None
#------------------------------------------------------------------------

import sys
from ctypes import *

nidslib = CDLL('../lib/libnids.so', RTLD_GLOBAL)
anonlib = CDLL('../lib/anonlib.so')

class SHA2_Context(Structure):
        _fields_ = [("total", c_ulonglong * 2),
                    ("state", c_ulonglong * 8),
                    ("buffer",    c_ubyte * 128),
                    ("ipad",      c_ubyte * 128),
                    ("opad",      c_ubyte * 128),
                    ("block_size",c_uint)
                   ]

class SHA2_Sum(Structure):
        _fields_ = [("buffer", c_ubyte * 64)]

def main():
        '''FIPS 180-2 test vectors (appendices C & D)'''
        SHA2_test_vectors = [
                ("abc",
                [0xCB, 0x00, 0x75, 0x3F, 0x45, 0xA3, 0x5E, 0x8B,
                 0xB5, 0xA0, 0x3D, 0x69, 0x9A, 0xC6, 0x50, 0x07,
                 0x27, 0x2C, 0x32, 0xAB, 0x0E, 0xDE, 0xD1, 0x63,
                 0x1A, 0x8B, 0x60, 0x5A, 0x43, 0xFF, 0x5B, 0xED,
                 0x80, 0x86, 0x07, 0x2B, 0xA1, 0xE7, 0xCC, 0x23,
                 0x58, 0xBA, 0xEC, 0xA1, 0x34, 0xC8, 0x25, 0xA7],
                [0xDD, 0xAF, 0x35, 0xA1, 0x93, 0x61, 0x7A, 0xBA,
                 0xCC, 0x41, 0x73, 0x49, 0xAE, 0x20, 0x41, 0x31,
                 0x12, 0xE6, 0xFA, 0x4E, 0x89, 0xA9, 0x7E, 0xA2,
                 0x0A, 0x9E, 0xEE, 0xE6, 0x4B, 0x55, 0xD3, 0x9A,
                 0x21, 0x92, 0x99, 0x2A, 0x27, 0x4F, 0xC1, 0xA8,
                 0x36, 0xBA, 0x3C, 0x23, 0xA3, 0xFE, 0xEB, 0xBD,
                 0x45, 0x4D, 0x44, 0x23, 0x64, 0x3C, 0xE8, 0x0E,
                 0x2A, 0x9A, 0xC9, 0x4F, 0xA5, 0x4C, 0xA4, 0x9F]),
                ("abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu",
                [0x09, 0x33, 0x0C, 0x33, 0xF7, 0x11, 0x47, 0xE8,
                 0x3D, 0x19, 0x2F, 0xC7, 0x82, 0xCD, 0x1B, 0x47,
                 0x53, 0x11, 0x1B, 0x17, 0x3B, 0x3B, 0x05, 0xD2,
                 0x2F, 0xA0, 0x80, 0x86, 0xE3, 0xB0, 0xF7, 0x12,
                 0xFC, 0xC7, 0xC7, 0x1A, 0x55, 0x7E, 0x2D, 0xB9,
                 0x66, 0xC3, 0xE9, 0xFA, 0x91, 0x74, 0x60, 0x39],
                [0x8E, 0x95, 0x9B, 0x75, 0xDA, 0xE3, 0x13, 0xDA,
                 0x8C, 0xF4, 0xF7, 0x28, 0x14, 0xFC, 0x14, 0x3F,
                 0x8F, 0x77, 0x79, 0xC6, 0xEB, 0x9F, 0x7F, 0xA1,
                 0x72, 0x99, 0xAE, 0xAD, 0xB6, 0x88, 0x90, 0x18,
                 0x50, 0x1D, 0x28, 0x9E, 0x49, 0x00, 0xF7, 0xE4,
                 0x33, 0x1B, 0x99, 0xDE, 0xC4, 0xB5, 0x43, 0x3A,
                 0xC7, 0xD3, 0x29, 0xEE, 0xB6, 0xDD, 0x26, 0x54,
                 0x5E, 0x96, 0xE5, 0x5B, 0x87, 0x4B, 0xE9, 0x09]),
                ("".join(['a' for i in range(1000000)]),
                [0x9D, 0x0E, 0x18, 0x09, 0x71, 0x64, 0x74, 0xCB,
                 0x08, 0x6E, 0x83, 0x4E, 0x31, 0x0A, 0x4A, 0x1C,
                 0xED, 0x14, 0x9E, 0x9C, 0x00, 0xF2, 0x48, 0x52,
                 0x79, 0x72, 0xCE, 0xC5, 0x70, 0x4C, 0x2A, 0x5B,
                 0x07, 0xB8, 0xB3, 0xDC, 0x38, 0xEC, 0xC4, 0xEB,
                 0xAE, 0x97, 0xDD, 0xD8, 0x7F, 0x3D, 0x89, 0x85],
                [0xE7, 0x18, 0x48, 0x3D, 0x0C, 0xE7, 0x69, 0x64,
                 0x4E, 0x2E, 0x42, 0xC7, 0xBC, 0x15, 0xB4, 0x63,
                 0x8E, 0x1F, 0x98, 0xB1, 0x3B, 0x20, 0x44, 0x28,
                 0x56, 0x32, 0xA8, 0x03, 0xAF, 0xA9, 0x73, 0xEB,
                 0xDE, 0x0F, 0xF2, 0x44, 0x87, 0x7E, 0xA6, 0x0A,
                 0x4C, 0xB0, 0x43, 0x2C, 0xE5, 0x77, 0xC3, 0x1B,
                 0xEB, 0x00, 0x9C, 0x5C, 0x2C, 0x49, 0xAA, 0x2E,
                 0x4E, 0xAD, 0xB2, 0x17, 0xAD, 0x8C, 0xC0, 0x9B])
                            ]
        '''RFC 4231 test vectors'''
        SHA2_HMAC_test_vectors = [
                ("Hi There",
                 "\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B",
                 [0xAF, 0xD0, 0x39, 0x44, 0xD8, 0x48, 0x95, 0x62,
                  0x6B, 0x08, 0x25, 0xF4, 0xAB, 0x46, 0x90, 0x7F,
                  0x15, 0xF9, 0xDA, 0xDB, 0xE4, 0x10, 0x1E, 0xC6,
                  0x82, 0xAA, 0x03, 0x4C, 0x7C, 0xEB, 0xC5, 0x9C,
                  0xFA, 0xEA, 0x9E, 0xA9, 0x07, 0x6E, 0xDE, 0x7F,
                  0x4A, 0xF1, 0x52, 0xE8, 0xB2, 0xFA, 0x9C, 0xB6],
                 [0x87, 0xAA, 0x7C, 0xDE, 0xA5, 0xEF, 0x61, 0x9D,
                  0x4F, 0xF0, 0xB4, 0x24, 0x1A, 0x1D, 0x6C, 0xB0,
                  0x23, 0x79, 0xF4, 0xE2, 0xCE, 0x4E, 0xC2, 0x78,
                  0x7A, 0xD0, 0xB3, 0x05, 0x45, 0xE1, 0x7C, 0xDE,
                  0xDA, 0xA8, 0x33, 0xB7, 0xD6, 0xB8, 0xA7, 0x02,
                  0x03, 0x8B, 0x27, 0x4E, 0xAE, 0xA3, 0xF4, 0xE4,
                  0xBE, 0x9D, 0x91, 0x4E, 0xEB, 0x61, 0xF1, 0x70,
                  0x2E, 0x69, 0x6C, 0x20, 0x3A, 0x12, 0x68, 0x54]),
                ("what do ya want for nothing?",
                 "Jefe",
                 [0xAF, 0x45, 0xD2, 0xE3, 0x76, 0x48, 0x40, 0x31,
                  0x61, 0x7F, 0x78, 0xD2, 0xB5, 0x8A, 0x6B, 0x1B,
                  0x9C, 0x7E, 0xF4, 0x64, 0xF5, 0xA0, 0x1B, 0x47,
                  0xE4, 0x2E, 0xC3, 0x73, 0x63, 0x22, 0x44, 0x5E,
                  0x8E, 0x22, 0x40, 0xCA, 0x5E, 0x69, 0xE2, 0xC7,
                  0x8B, 0x32, 0x39, 0xEC, 0xFA, 0xB2, 0x16, 0x49],
                 [0x16, 0x4B, 0x7A, 0x7B, 0xFC, 0xF8, 0x19, 0xE2,
                  0xE3, 0x95, 0xFB, 0xE7, 0x3B, 0x56, 0xE0, 0xA3,
                  0x87, 0xBD, 0x64, 0x22, 0x2E, 0x83, 0x1F, 0xD6,
                  0x10, 0x27, 0x0C, 0xD7, 0xEA, 0x25, 0x05, 0x54,
                  0x97, 0x58, 0xBF, 0x75, 0xC0, 0x5A, 0x99, 0x4A,
                  0x6D, 0x03, 0x4F, 0x65, 0xF8, 0xF0, 0xE6, 0xFD,
                  0xCA, 0xEA, 0xB1, 0xA3, 0x4D, 0x4A, 0x6B, 0x4B,
                  0x63, 0x6E, 0x07, 0x0A, 0x38, 0xBC, 0xE7, 0x37]),
                ("\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xDD",
                 "\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA",
                 [0x88, 0x06, 0x26, 0x08, 0xD3, 0xE6, 0xAD, 0x8A,
                  0x0A, 0xA2, 0xAC, 0xE0, 0x14, 0xC8, 0xA8, 0x6F,
                  0x0A, 0xA6, 0x35, 0xD9, 0x47, 0xAC, 0x9F, 0xEB,
                  0xE8, 0x3E, 0xF4, 0xE5, 0x59, 0x66, 0x14, 0x4B,
                  0x2A, 0x5A, 0xB3, 0x9D, 0xC1, 0x38, 0x14, 0xB9,
                  0x4E, 0x3A, 0xB6, 0xE1, 0x01, 0xA3, 0x4F, 0x27],
                 [0xFA, 0x73, 0xB0, 0x08, 0x9D, 0x56, 0xA2, 0x84,
                  0xEF, 0xB0, 0xF0, 0x75, 0x6C, 0x89, 0x0B, 0xE9,
                  0xB1, 0xB5, 0xDB, 0xDD, 0x8E, 0xE8, 0x1A, 0x36,
                  0x55, 0xF8, 0x3E, 0x33, 0xB2, 0x27, 0x9D, 0x39,
                  0xBF, 0x3E, 0x84, 0x82, 0x79, 0xA7, 0x22, 0xC8,
                  0x06, 0xB4, 0x85, 0xA4, 0x7E, 0x67, 0xC8, 0x07,
                  0xB9, 0x46, 0xA3, 0x37, 0xBE, 0xE8, 0x94, 0x26,
                  0x74, 0x27, 0x88, 0x59, 0xE1, 0x32, 0x92, 0xFB]),
                ("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD",
                "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19",
                [0x3E, 0x8A, 0x69, 0xB7, 0x78, 0x3C, 0x25, 0x85,
                 0x19, 0x33, 0xAB, 0x62, 0x90, 0xAF, 0x6C, 0xA7,
                 0x7A, 0x99, 0x81, 0x48, 0x08, 0x50, 0x00, 0x9C,
                 0xC5, 0x57, 0x7C, 0x6E, 0x1F, 0x57, 0x3B, 0x4E,
                 0x68, 0x01, 0xDD, 0x23, 0xC4, 0xA7, 0xD6, 0x79,
                 0xCC, 0xF8, 0xA3, 0x86, 0xC6, 0x74, 0xCF, 0xFB],
                [0xB0, 0xBA, 0x46, 0x56, 0x37, 0x45, 0x8C, 0x69,
                 0x90, 0xE5, 0xA8, 0xC5, 0xF6, 0x1D, 0x4A, 0xF7,
                 0xE5, 0x76, 0xD9, 0x7F, 0xF9, 0x4B, 0x87, 0x2D,
                 0xE7, 0x6F, 0x80, 0x50, 0x36, 0x1E, 0xE3, 0xDB,
                 0xA9, 0x1C, 0xA5, 0xC1, 0x1A, 0xA2, 0x5E, 0xB4,
                 0xD6, 0x79, 0x27, 0x5C, 0xC5, 0x78, 0x80, 0x63,
                 0xA5, 0xF1, 0x97, 0x41, 0x12, 0x0C, 0x4F, 0x2D,
                 0xE2, 0xAD, 0xEB, 0xEB, 0x10, 0xA2, 0x98, 0xDD]),
                ("Test With Truncation",
                 "\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C",
                 [0x3A, 0xBF, 0x34, 0xC3, 0x50, 0x3B, 0x2A, 0x23,
                  0xA4, 0x6E, 0xFC, 0x61, 0x9B, 0xAE, 0xF8, 0x97],
                 [0x41, 0x5F, 0xAD, 0x62, 0x71, 0x58, 0x0A, 0x53,
                  0x1D, 0x41, 0x79, 0xBC, 0x89, 0x1D, 0x87, 0xA6]
                ),
                ("Test Using Larger Than Block-Size Key - Hash Key First",
                 ''.join(['\xAA' for i in range(131)]),
                 [0x4E, 0xCE, 0x08, 0x44, 0x85, 0x81, 0x3E, 0x90,
                  0x88, 0xD2, 0xC6, 0x3A, 0x04, 0x1B, 0xC5, 0xB4,
                  0x4F, 0x9E, 0xF1, 0x01, 0x2A, 0x2B, 0x58, 0x8F,
                  0x3C, 0xD1, 0x1F, 0x05, 0x03, 0x3A, 0xC4, 0xC6,
                  0x0C, 0x2E, 0xF6, 0xAB, 0x40, 0x30, 0xFE, 0x82,
                  0x96, 0x24, 0x8D, 0xF1, 0x63, 0xF4, 0x49, 0x52],
                 [0x80, 0xB2, 0x42, 0x63, 0xC7, 0xC1, 0xA3, 0xEB,
                  0xB7, 0x14, 0x93, 0xC1, 0xDD, 0x7B, 0xE8, 0xB4,
                  0x9B, 0x46, 0xD1, 0xF4, 0x1B, 0x4A, 0xEE, 0xC1,
                  0x12, 0x1B, 0x01, 0x37, 0x83, 0xF8, 0xF3, 0x52,
                  0x6B, 0x56, 0xD0, 0x37, 0xE0, 0x5F, 0x25, 0x98,
                  0xBD, 0x0F, 0xD2, 0x21, 0x5D, 0x6A, 0x1E, 0x52,
                  0x95, 0xE6, 0x4F, 0x73, 0xF6, 0x3F, 0x0A, 0xEC,
                  0x8B, 0x91, 0x5A, 0x98, 0x5D, 0x78, 0x65, 0x98]),
                ("This is a test using a larger than block-size key and a larger than block-size data. The key needs to be hashed before being used by the HMAC algorithm.",
                 ''.join(['\xAA' for i in range(131)]),
                [0x66, 0x17, 0x17, 0x8E, 0x94, 0x1F, 0x02, 0x0D,
                 0x35, 0x1E, 0x2F, 0x25, 0x4E, 0x8F, 0xD3, 0x2C,
                 0x60, 0x24, 0x20, 0xFE, 0xB0, 0xB8, 0xFB, 0x9A,
                 0xDC, 0xCE, 0xBB, 0x82, 0x46, 0x1E, 0x99, 0xC5,
                 0xA6, 0x78, 0xCC, 0x31, 0xE7, 0x99, 0x17, 0x6D,
                 0x38, 0x60, 0xE6, 0x11, 0x0C, 0x46, 0x52, 0x3E],
                [0xE3, 0x7B, 0x6A, 0x77, 0x5D, 0xC8, 0x7D, 0xBA,
                 0xA4, 0xDF, 0xA9, 0xF9, 0x6E, 0x5E, 0x3F, 0xFD,
                 0xDE, 0xBD, 0x71, 0xF8, 0x86, 0x72, 0x89, 0x86,
                 0x5D, 0xF5, 0xA3, 0x2D, 0x20, 0xCD, 0xC9, 0x44,
                 0xB6, 0x02, 0x2C, 0xAC, 0x3C, 0x49, 0x82, 0xB1,
                 0x0D, 0x5E, 0xEB, 0x55, 0xC3, 0xE4, 0xDE, 0x15,
                 0x13, 0x46, 0x76, 0xFB, 0x6D, 0xE0, 0x44, 0x60,
                 0x65, 0xC9, 0x74, 0x40, 0xFA, 0x8C, 0x6A, 0x58])
                                 ]
        digest = SHA2_Sum()
        for block_size in [384, 512]:
                for buffer, sha384sum, sha512sum in SHA2_test_vectors:
                        anonlib.SHA2(c_char_p(buffer), len(buffer), byref(digest), c_int(block_size))

                        result = [byte for byte in digest.buffer]
                        result = result[:block_size/8]
                        if result != sha384sum and result != sha512sum:
                                raise AssertionError('[-] SHA2 test failed.')
        # HMAC-SHA-2 tests [RFC4231]
        for block_size in [384, 512]:
                for buffer, key, sha384sum, sha512sum in SHA2_HMAC_test_vectors:
                        anonlib.SHA2_hmac(c_char_p(key), len(key), c_char_p(buffer), len(buffer), byref(digest), c_int(block_size))

                        result = [byte for byte in digest.buffer]
                        # To truncate or not to truncate?
                        if key[0] == '\x0C':
                                result = result[:16]
                        else:
                                result = result[:block_size/8]
                        if result != sha384sum and result != sha512sum:
                                raise AssertionError('[-] SHA2 test failed.')

        print('[+] SHA2 test passed.')

if __name__ == '__main__':
        main()