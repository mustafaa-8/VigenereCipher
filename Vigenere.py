from random import randint # For generating random shift values
import pandas as pd # For handling records in a DataFrame
import os # For checking file existence

file_path = "Projects\\VigenereCipher\\records.json"

if os.path.exists(file_path): # Load existing records if file exists
    df = pd.read_json(file_path)
else: # Initialize empty DataFrame if no file exists
    df = pd.DataFrame(columns=['encryptedtext', 'shift'])
    
def encrypt(text):   # Encrypt the text using Vigenere cipher with the given key
    global df
    result = ""
    shift_list = []

    for i in text:
        if i.isalpha():
            shift = randint(1 , 25)
            shift_list.append(shift)
            if i.isupper():
                result += chr((ord(i) + shift - 65) % 26 + 65)  # Encrypt uppercase letters
            elif i.islower():
                result += chr((ord(i) + shift - 97) % 26 + 97)  # Encrypt lowercase letters
            else:
                result += i # Non-alphabetic characters remain unchanged

    new_row = {'encryptedtext': result, 'shift': shift_list.copy()} 
    df.loc[len(df)] = new_row # Append new record to DataFrame
    df.to_json(file_path, orient="records" , indent=4) # Save DataFrame to JSON   

    return result

def decrypt(text, shift_list):
    result = ""
    k = 0
    
    for char in text:
        if char.isalpha(): 
            shift = shift_list[k]
            if char.isupper():
                result += chr((ord(char) - shift - 65) % 26 + 65) # Decrypt uppercase letters
            elif char.islower():
                result += chr((ord(char) - shift - 97) % 26 + 97) # Decrypt lowercase letters
            else:
                result += char
            k+=1
        
    return result
    k = 0

def choice_check(choice):
    if choice == 1:
        text = input("Enter text to encrypt: ")
        print("Encryption Successful!\nEncrypted text:", encrypt(text))
    
    elif choice == 2:
        print("There are", len(df), "records available.") # Show available records
        for i in range(len(df)):
            print(f"{i+1}. {df.loc[i, 'encryptedtext']}")
        record_choice = int(input("Select a record number to decrypt: ")) - 1
        if 0 <= record_choice < len(df):
            encrypted_text = df.loc[record_choice, 'encryptedtext'] # Get encrypted text from selected record
            shift_list = df.loc[record_choice, 'shift']
            print("Decryption Successful!\nDecrypted text:", decrypt(encrypted_text, shift_list)) # Decrypt using stored shift value    
        else:
            print("Invalid record number.") 
    elif choice == 0:
        df.to_json(file_path, orient="records" , indent=4) # Save DataFrame to JSON
        print("Thank you for using the Vigenere Cipher program. Goodbye!")
        exit()        

def main():
    choice = -1
    while choice != 0 : # Main loop
        print("""Make a choice:
1. Encrypt
2. Decrypt
0. Exit""")
        try:
            choice = int(input("Enter your choice: "))
            print("\n\n")
            if choice in [0, 1, 2]:
                choice_check(choice)
            else:
                print("Invalid choice. Please choose 0, 1, or 2.")    
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__" :
    main()