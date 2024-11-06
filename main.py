def hex_to_dec(hex_line):
    """
    Converts a hexadecimal string into a list of decimal values.

    Args:
        hex_line (str): A string containing hexadecimal values.

    Returns:
        list: A list of decimal integers corresponding to each byte in the hexadecimal string.
    """
    decimal_numbers = [int(hex_line[i:i + 2], 16) for i in range(0, len(hex_line), 2)]
    return decimal_numbers


def ciphers_to_dec(cipher_text):
    """
    Converts a list of hexadecimal cipher strings into a list of lists containing decimal values.

    Args:
        cipher_text (list of str): A list where each element is a string representing hexadecimal cipher text.

    Returns:
        list: A list of lists where each sublist contains decimal integers corresponding to the cipher text.
    """
    decimal_cipher = []
    for line in cipher_text:
        decimal_cipher.append(hex_to_dec(line))
    return decimal_cipher


def text_to_decimal(plain_text):
    """
    Converts a string of plain text into a list of decimal values based on their ASCII codes.

    Args:
        plain_text (str): A string containing the plain text to be converted.

    Returns:
        list: A list of decimal values representing the ASCII codes of the characters in the plain text.
    """
    decimal_values = [ord(char) for char in plain_text]
    return decimal_values


def assign_spaces(decimal_cipher, boolean_array):
    """
    Assigns spaces to positions in the boolean array where spaces are detected in the cipher text
    by XORing pairs of cipher lines and checking if they produce printable characters.

    Args:
        decimal_cipher (list of list of int): A list of lists where each sublist contains decimal integers
                                              representing cipher text.
        boolean_array (list of list of bool): A list of lists used to mark positions where spaces are likely to appear.

    Returns:
        list of list of bool: The updated boolean array where `True` indicates that a space is likely in that position.
    """
    for column in range(len(decimal_cipher[0])):
        for fixed_line in range(8):
            is_valid = True
            for variable_line in range(8):
                result = decimal_cipher[fixed_line][column] ^ decimal_cipher[variable_line][column]
                if not (32 <= result <= 126 or result == 0):
                    is_valid = False
                    break
            boolean_array[fixed_line][column] = is_valid
    return boolean_array


def crack_message(decimal_cipher, boolean_array, cracked_plain_text):
    """
    Cracks the cipher text by using the boolean array to detect positions of spaces and determining the
    corresponding plain text characters.

    Args:
        decimal_cipher (list of list of int): A list of lists where each sublist contains decimal integers
                                              representing cipher text.
        boolean_array (list of list of bool): A list of lists indicating where spaces are likely to appear.
        cracked_plain_text (list of list of str): A list of lists representing the partially cracked plain text.

    Returns:
        list of list of str: The updated plain text where detected characters are inserted at appropriate positions.
    """
    for column in range(len(decimal_cipher[0])):
        for fixed_line in range(8):
            if boolean_array[fixed_line][column]:  # Check only if it's valid
                for variable_line in range(8):
                    result = decimal_cipher[fixed_line][column] ^ decimal_cipher[variable_line][column] ^ 32
                    if 32 <= result <= 126:  # Check if it's printable
                        cracked_plain_text[variable_line][column] = chr(result)
    return cracked_plain_text


cipher_text = [
    "F9B4228898864FCB32D83F3DFD7589F109E33988FA8C7A9E9170FB923065F52DD648AA2B8359E1D122122738A8B9998BE278B2BD7CF3313C7609",
    "F5BF229F8F9B1C8832C0212DFD7F92EA18FF29C7E6C968848D6EFAC16074F129D640AB67CE59E3DC6109212AB4EB959FFD34F3B269EB292C7409",
    "FDAF668499C801C734813F3BF3718FF91AEA2C88FC862B999D6EE7C16369F83ADF57FF28CD18FCCC6F0D2B2BB5A295DEF436B0A164EF3C267014",
    "FDFB35858B8403882EC4392CE03289F50CF82588FC816ECB8B63F3843076F52CC059B035C718E0DB220D3B33B3A28692F478B2B07EF03D216B09",
    "E4BE239FCA9A0ADE29C43869FD74DBE31CE835DAE19D72CB9567FD897168FD2CDE5DFF35C65CFAD667136E29B2A7989BE339B1BA71F63C267A09",
    "F8BE279F848101CF60C9203EB26694B00EF929DCEDC9788E9B77EC843075FB39C759BE35C618E6C622016E31A2A8938DE239A1AA3DEC23267316",
    "E7BE2598988D4FC325D86F2CEA7193F117EC2588E19A2B859D67FA847426F230C10EAC3ECE55EAC170092D7FACAE8FDEF436B0A164EF3C267014",
    "E7BE259898811BD160C03B69E67A9EB01CF330CDE69A6ECB9764BE946367F636DF47AB3E835BE0C06E046E3BA6A69799F478A0B67EEA3A266B03"
]

# Convert cipher text to a list of decimal numbers
decimal_cipher = ciphers_to_dec(cipher_text)

# Initialize boolean array to assign the spaces positions
# Initialize cracked plain text list to decrypt letters in known space columns
boolean_array = [[False for _ in row] for row in decimal_cipher]
cracked_plain_text = [['$' for _ in row] for row in decimal_cipher]

# Assign spaces to boolean array
boolean_array = assign_spaces(decimal_cipher, boolean_array)

# Crack the message known space positions
cracked_plain_text = crack_message(decimal_cipher, boolean_array, cracked_plain_text)

for line in cracked_plain_text:
    print("".join(line))
print("\n")

# The resulted cracked message is:

# $od$rn cryptogra$$$ $equ$$es c$$$ful a$$ $ig$r$u$ a$a$$$$$
# $dd$ess randomiz$$$o$ co$$d pr$$$nt ma$$c$ou$ $a$l $t$$$$$
# $t $s not practi$$$ $o r$$y so$$$y on $$m$et$i$ $nc$y$$$$$
# $ s$all never re$$$ $he $$me p$$$word $$ $ul$i$l$ a$c$$$$$
# $ee$ review of s$$$r$ty $$chan$$$s red$$e$ v$l$e$ab$l$$$$$
# $ea$ning how to $$$t$ se$$re s$$$ware $$ $ n$c$s$ar$ $$$$$
# $ec$re key excha$$$ $s n$$ded $$$ symm$$r$c $e$ $nc$y$$$$$
# $ec$rity at the $$$e$se $$ usa$$$ity c$$l$ d$m$g$ s$c$$$$$

# First assumpton was made by me is that the first plain text contain those words: "modern" "cryptography" "requires" "careful" "rigorous"
# Second assumpton was made by me is that the third plain text contain this word at the end: "encryption
# The words mentioned was very straightforward to deduce
# I set the list plain_text1 to the assumed first plain text till the index of the encryption word in the third row
# Generate the key by XORing the plain text with the cipher text
plain_text1 = 'Modern cryptography requires careful and rigorou'
plain_text2 = 'encryption'
decimal_plain_text1 = text_to_decimal(plain_text1)
decimal_plain_text2 = text_to_decimal(plain_text2)
key = []

# Get the Key by Xoring the plain texts known with the cipher texts
for column1 in range(len(decimal_plain_text1)):
    key.append(decimal_plain_text1[column1] ^ decimal_cipher[0][column1])
for column2 in range(len(decimal_plain_text2)):
    key.append(decimal_plain_text2[column2] ^ decimal_cipher[2][column2 + len(decimal_plain_text1)])

# Xor all the cipher texts with the key cracked to get all the plain messages
final_message = []
for row in range(8):
    row_message = []
    for column in range(len(key)):
        plain_word = decimal_cipher[row][column] ^ key[column]
        row_message.append(chr(plain_word))
    final_message.append(row_message)

for line in final_message:
    print("".join(line))
