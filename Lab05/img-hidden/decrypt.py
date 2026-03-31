import sys
from PIL import Image

def decode_image(encoded_image_path):
    img = Image.open(encoded_image_path)
    width, height = img.size
    binary_message = ""

    # Lấy các bit cuối cùng từ mỗi kênh màu của mỗi pixel
    for row in range(height):
        for col in range(width):
            pixel = img.getpixel((col, row))
            for color_channel in range(3):
                binary_message += format(pixel[color_channel], '08b')[-1]

    message = ""
    # Giải mã chuỗi nhị phân thành ký tự (mỗi 8 bit là 1 ký tự)
    for i in range(0, len(binary_message), 8):
        char_bin = binary_message[i:i+8]
        char = chr(int(char_bin, 2))
        
        # Kiểm tra dấu hiệu kết thúc (16 bit cuối trong encrypt.py)
        # Sách trang 169 dùng logic kiểm tra marker để dừng
        if binary_message[i:i+16] == '1111111111111110':
            break
        message += char

    return message

def main():
    if len(sys.argv) != 2:
        print("Usage: python decrypt.py <encoded_image_path>")
        return

    encoded_image_path = sys.argv[1]
    decoded_message = decode_image(encoded_image_path)
    print("Decoded message:", decoded_message)

if __name__ == "__main__":
    main()