import os
import shutil

# Функція для транслітерації імен файлів
def normalize(filename):
    translit_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
        'и': 'i', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'shch', 'ь': '', 'ю': 'iu', 'я': 'ia',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'Ye', 'Ж': 'Zh', 'З': 'Z',
        'И': 'Y', 'І': 'I', 'Ї': 'Yi', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O',
        'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch',
        'Ш': 'Sh', 'Щ': 'Shch', 'Ь': '', 'Ю': 'Yu', 'Я': 'Ya'
    }

    normalized = ""
    for char in filename:
        if char.isalpha() and char in translit_map:
            normalized += translit_map[char]
        elif char.isalnum():
            normalized += char
        else:
            normalized += '_'
    return normalized

# Функція для сортування папки
def sort_folder(folder_path):
    file_extensions = {
        'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
        'videos': ('AVI', 'MP4', 'MOV', 'MKV'),
        'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
        'music': ('MP3', 'OGG', 'WAV', 'AMR'),
        'archives': ('ZIP', 'GZ', 'TAR')
    }

    unknown_extensions = set()

    # Отримуємо список всіх файлів та папок у вказаній директорії
    items = os.listdir(folder_path)

    for item in items:
        item_path = os.path.join(folder_path, item)

        # Ігноруємо папки "archives", "videos", "audio", "documents" та "images"
        if os.path.isdir(item_path) and item.lower() in ('archives', 'videos', 'audio', 'documents', 'images'):
            continue

        # Обробляємо файли
        if os.path.isfile(item_path):
            filename, extension = os.path.splitext(item)
            extension = extension[1:].upper()

            # Знаходимо категорію за розширенням файлу
            category = None
            for key, values in file_extensions.items():
                if extension in values:
                    category = key
                    break

            if category:
                # Створюємо папку категорії, якщо вона не існує
                category_path = os.path.join(folder_path, category)
                if not os.path.exists(category_path):
                    os.makedirs(category_path)

                # Перейменовуємо файл та переміщуємо його до відповідної категорії
                normalized_name = normalize(filename)
                new_path = os.path.join(category_path, normalized_name + extension)
                shutil.move(item_path, new_path)
            else:
                # Розширення невідоме, додаємо його до списку невідомих розширень
                unknown_extensions.add(extension)

        # Обробляємо папки рекурсивно
        elif os.path.isdir(item_path):
            sort_folder(item_path)

    return unknown_extensions

# Приклад використання
folder_path = input("Введіть шлях до папки: ")
unknown_extensions = sort_folder(folder_path)

# Виведення результатів
print("Файли розподілені за категоріями.")
print("Перелік усіх відомих скрипту розширень:")
for category, extensions in file_extensions.items():
    print(category.capitalize(), ":", ", ".join(extensions))
print("Перелік всіх розширень, які скрипту невідомі:")
print(", ".join(unknown_extensions))