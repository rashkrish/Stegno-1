import cv2
import numpy as np

def to_bin(data): # Converts data to binary format as string
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")


def encode(image_name, secret_data):
    image = cv2.imread(image_name) # read the image
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8 # maximum bytes to encode
    
    if len(secret_data) > n_bytes:
        raise ValueError("Insufficient bytes, need bigger image or less data!!!")
    print("...Encoding data...")
    
    secret_data += "=====" # add delimiter (stopping criteria)
    data_index = 0
    
    binary_secret_data = to_bin(secret_data) # convert data to binary
    data_len = len(binary_secret_data) # size of data to hide
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel) # convert RGB values to binary format
            
            # modify the least significant bit only if there is still data to store
            if data_index < data_len:
                pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2) # least significant red pixel bit
                data_index += 1
            if data_index < data_len:
                pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2) # least significant green pixel bit
                data_index += 1
                
            if data_index < data_len:
                pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2) # least significant blue pixel bit
                data_index += 1
            
            if data_index >= data_len: # It just break out of the loop if data is encoded
                break
    print("Encoding Done!!!")
    return image


def decode(image_name):
    print("...Decoding Data...")
    image = cv2.imread(image_name) # read the image
    binary_data = ""
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    
    all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ] # split by 8-bits
    
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))  # convert from bits to characters
        if decoded_data[-5:] == "=====":
            break
    return decoded_data[:-5]

if __name__ == "__main__":

    print("*********** Welcome to Image Steganography ************\n1. Encode\n2. Decode\n")
    a = int(input("Choose your option: "))
    print("\nNote: The code works for only those cover images having .png extension.")
    input_image = input("\nEnter the path of image file: ")
    
    if (a == 1):
        print("Enter The Secret Message: ",end="")
        secret_data = input()
        output_image = input("Enter output image name with extension including the directory where you want to save it: ")
        
        encoded_image = encode(image_name=input_image, secret_data=secret_data)  # encode the message into the image
        cv2.imwrite(output_image, encoded_image)# save the output image (encoded image)
        
    elif (a==2):
        decoded_data = decode(input_image) # decode the secret data from the image
        print("Decoded data:", decoded_data)
