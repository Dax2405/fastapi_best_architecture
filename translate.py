import os
import re
from libretranslatepy import LibreTranslateAPI


def process_directory(directory: str, lt: LibreTranslateAPI) -> None:
    """Process a directory of files and translate them.

    Args:
        directory (str): The directory containing the files to translate.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".py", ".sql")):
                process_file(os.path.join(root, file), lt)

def process_file(file_path: str, lt: LibreTranslateAPI) -> None:
    """Process a single file and translate its content.

    Args:
        file_path (str): The path to the file to translate.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.readlines()
    print(f"Processing file: {file_path}")
    translated_content: list[str] = []
    for line in content:
        if re.search(r'[\u4e00-\u9fff]', line):
            leading_whitespace = re.match(r"^\s*", line).group(0)

            matches = re.findall(r'["\']([^"\']*[\u4e00-\u9fff]+[^"\']*)["\']', line)
            for match in matches:
                translated = translate_text(match, lt)
                line: str = line.replace(match, translated)
                print(f"Translated string: {match} -> {translated}")
                

            if re.search(r'#.*[\u4e00-\u9fff]+', line):
                match = re.search(r'#(.*[\u4e00-\u9fff]+)', line)
                if match:
                    chinese_text = match.group(1).strip()
                    translated: str = translate_text(chinese_text, lt)
                    line = line.replace(chinese_text, translated)
                    print(f"Translated comment: {chinese_text} -> {translated}")
            
            if re.search(r'.*[\u4e00-\u9fff]+', line):
                match = re.search(r'(.*[\u4e00-\u9fff]+)', line)
                if match:
                    chinese_text = match.group(1).strip()
                    translated: str = translate_text(chinese_text, lt)
                    line = line.replace(chinese_text, translated)
                    print(f"Translated comment: {chinese_text} -> {translated}")  
                

            line = f"{leading_whitespace}{line.strip()}\n"

        translated_content.append(line)
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(translated_content)
    
    
    
def translate_text(text, lt) -> str:
    """Translate text using LibreTranslate API.

    Args:
        text (str): The text to translate.
        lt (LibreTranslateAPI): The LibreTranslate API instance.

    Returns:
        str: The translated text.
    """
    try:
        translated = lt.translate(text, "zh", "en")
        return translated
    except Exception as e:
        print(f"Error translating text: {text}\n{e}")
        return text
    

if __name__ == "__main__":
    lt: LibreTranslateAPI = LibreTranslateAPI("http://127.0.0.1:5000")
    process_directory(f"{os.path.dirname(__file__)}/backend", lt)
