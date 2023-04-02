from WordBoard import WordBoard


def main():
    print("Word Search Puzzle Brute Force")
    print()
    size = input(
        "Masukkan Ukuran Grid (Return/Enter untuk menggunakan Default) (Default = 16x16): ")
    color = input("Color (Return/Enter for Default): ")
    file_name = input(
        "Masukkan Nama File jika ingin menggunakan file baru (Return/Enter untuk memakai words.txt sebagai default): ")
    check = "a"
    words = []
    while check:
        check = input(
            "Masukkan Kata (Kosongkan dan Return/Enter untuk langsung menjalankan sistem): ")
        words.append(check)

    size = int(size) if size else 16
    color = color if color else "yellow"
    file_name = file_name if file_name else "words.txt"
    words = words[:-1] if words[:-1] else None

    WordBoard(size=size, color=color, file_name=file_name, words=words)


if __name__ == "__main__":
    main()
