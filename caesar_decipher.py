# Caesar Decryption tool for CSCI361 S3 2020
# Developed and tested in Python 3.7.2, Windows 10 Pro Version 2004
# Written by Jon K, 2020

import string
import sys
import argparse


# Main function of program - takes in the input file to read into text and iterates decryption with k {1, 26}
# Also displays each key's MIC and the computed key for cipher, as well as the correctly decrypted text with all
# symbols stripped and uppercase letters
def main():
    input_file_name = parse_cli_args()
    cipher_text = read_text_file(input_file_name)
    cipher_text = retain_alpha(cipher_text)
    all_mic = []

    # From 1 - 26
    for k in range(1, 27):
        current_key_mic = mic(decrypt(cipher_text, k))
        all_mic.append(current_key_mic)

        if k < 10:
            print("Key: 0{0} --- MIC: {1}".format(k, current_key_mic))
        else:
            print("Key: {0} --- MIC: {1}".format(k, current_key_mic))

    key = get_key(all_mic)
    print("\nThe key for this cipher is {0}\n".format(key))
    print("Decrypted Text\n----------------\n")
    print(decrypt(cipher_text, key))


# Function to parse command line argument - in this case a single --input file
def parse_cli_args():
    parser = argparse.ArgumentParser("caesar_decipher")
    parser.add_argument("-in", "--input", help="input file name", type=str, required=True, dest="input_file")
    args = parser.parse_args()
    return args.input_file


# Function to read given data file and returns data in a string
def read_text_file(file):
    try:
        with open (file, 'r') as file:
            file_data = file.read()
        return file_data
    except FileNotFoundError:
        print("File does not exist!")
        sys.exit(0)


# Strips all non alphabetical characters in cipher text and returns uppercased ct without symbols/punctuations
def retain_alpha(ct):
    stripped = []
    for c in ct:
        if c.isalpha():
            stripped.append(c)

    return (''.join(stripped)).upper()


# Caesar Cipher decryption function that takes in a cipher text and key
def decrypt(cipher_text, key):
    decrypted = []
    for c in cipher_text:
        char_ascii = ord(c)
        if ord('A') <= char_ascii <= ord('Z'):
            char_ascii = char_ascii - key
            if char_ascii < ord('A'):
                char_ascii = char_ascii + ord('Z') - ord('A') + 1
        decrypted_char = chr(char_ascii)
        decrypted.append(decrypted_char)
    return ''.join(decrypted)


# Function that takes in a string and calculates the mutual index of coincidence of string given
# probability is a list of probability of occurrence of each letter provided in the assignment
# N is the length of given text
# character_frequencies is a dict of {C : n} from A-Z, initialized with all 0s
# frequency_list is a list of all n from A-Z from character_frequencies for cleaner iteration
# MIC is calculated by the sum of probability at i multiplied by frequency of character at i divided by N
# Meaning to say {A: 10, B:20 .. Z: 3}, 10 * 0.082 + 20 * 0.015 + 3 * 0.001 for A-Z.
# For a correctly decrypted text, the MIC will result in 0.065 (given sufficient text length)
def mic(text):
    probability = [0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.020, 0.061, 0.070, 0.002, 0.008, 0.040, 0.024, 0.067,
                   0.075, 0.019, 0.001, 0.060, 0.063, 0.091, 0.028, 0.010, 0.023, 0.001, 0.020, 0.001]
    N = len(text)
    mutual_index_coincidence = 0
    character_frequencies = dict.fromkeys(string.ascii_uppercase, 0)

    for char in text:
        if char in character_frequencies:
            character_frequencies[char] += 1

    frequency_list = list(character_frequencies.values())
    # 0 to 26 exclusive
    for i in range(26):
        mutual_index_coincidence += (probability[i] * frequency_list[i]) / N

    return mutual_index_coincidence


# Function to return cipher key based on a list of MIC iterated with different k from 1 - 26 (in main)
# This function checks for the max MIC in the list (likely to be 0.065 given sufficient text) and gives a margin of 10%
# just in case text length is not long enough and MIC is thrown off a little. The key is returned with the index of
# max(mic) + 1
def get_key(list_mic):
    max_mic = max(list_mic)
    if max_mic * 0.9 <= 0.065 <= max_mic * 1.1:
        key = list_mic.index(max_mic) + 1
    return key


main()
