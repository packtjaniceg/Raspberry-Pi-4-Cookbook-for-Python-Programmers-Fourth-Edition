#!/usr/bin/python3
''' encryptdecrypt.py '''

def encrypt_text(input_text, key):
    ''' Takes the input_text and encrypts it, returning the result '''
    input_text = input_text.upper()
    result = ""
    for letter in input_text:
        #Ascii Uppercase 65-90  Lowercase 97-122 (Full range 32-126)
        ascii_value = ord(letter)
        #Exclude non-characters from encryption
        if (ord("A") > ascii_value) or (ascii_value > ord("Z")):
            result += letter
        else:
            #Apply encryption key
            key_value = ascii_value+key
            #Ensure we just use A-Z regardless of key
            if not (ord("A")) < key_value < ord("Z"):
                key_value = ord("A") + \
                    (key_value-ord("A"))%(ord("Z")-ord("A")+1)
            #Add the encoded letter to the result string
            result += str(chr(key_value))
    return result

def main():
    ''' Test function, only called if script executed directly '''
    print("Please enter text to scramble:")
    #Get user input
    try:
        user_input = input()
        scrambled_result = encrypt_text(user_input, 10)
        print(f"Result: {scrambled_result}")
        print("To un-scramble, press enter again")
        input()
        unscrambled_result = encrypt_text(scrambled_result, -10)
        print(f"Result: {unscrambled_result}")
    except UnicodeDecodeError:
        print("Sorry: Only ASCII Characters are supported")

if __name__ == "__main__":
    main()
#End
