# One-Time Pad Ciphertext Decryption

This project implements a solution to decrypt ciphertexts that were encrypted using a one-time pad key that was improperly reused. The ciphertexts, which represent eight English sentences of the same length, were encrypted using the same key, resulting in vulnerability to cryptanalysis.

The objective is to determine the complete plaintexts for all eight ciphertexts, which only contain English letters and spaces, without punctuation or special characters.

## Project Overview

In this project, we approach the problem using cryptanalysis techniques tailored for one-time pad ciphertexts that share the same encryption key. Since reusing a one-time pad key makes it possible to recover plaintext through comparisons, we leverage the following strategy:

1. **Identify Possible Space Positions**: By analyzing each pair of ciphertexts, we exploit the XOR properties to identify positions likely to contain spaces. Since XOR-ing with a space character (`0x20` in ASCII) affects only alphabetic characters, this property is useful in determining likely positions of spaces.

2. **Iterative Plaintext Recovery**: Once spaces are identified, we utilize this information to deduce individual letters. By XOR-ing corresponding bytes where we suspect spaces in one ciphertext, we reveal the letter in the other ciphertext.

3. **Final Guesses**: Using patterns, common English words, and context from partial plaintexts, we make educated guesses for any remaining unknown characters to complete the sentences.

## Approach

The decryption approach consists of these main steps:

1. **Load Ciphertexts**: The program reads the hexadecimal ciphertexts from the provided link.
2. **XOR Pair Analysis**: For each pair of ciphertexts, XOR corresponding bytes to find likely spaces by checking for ASCII-aligned characters.
3. **Space Deduction**: Use probable space positions to deduce letters across the sentences.
4. **Guess Remaining Characters**: Apply common words and patterns in English to fill in any remaining gaps in the plaintext.

This approach, leveraging patterns in English sentences and repeated key usage, allows us to recover the complete plaintexts from the ciphertexts.
