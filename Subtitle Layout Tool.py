import re
import os

# 获取文件地址
current_directory = os.getcwd()

folder_name = "txt_files"
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

folder_path = current_directory
srt_files = [f for f in os.listdir(folder_path) if f.endswith('.srt')]

for srt_file in srt_files:
    txt_path = os.path.join(current_directory, srt_file)
    output_file = os.path.join(current_directory, folder_name, srt_file[:-4] + '.txt')

    # 如果一行不是空行并且没有“-->”符号并且不全是数字，那么提取该行文本
    def remove_lines_with_numbers(input_file, output_file):
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        with open(output_file, 'w', encoding='utf-8', errors='ignore') as f:
            for line in lines[1:]:
                words = line.strip().split()
                if len(words) > 0 and not "-->" in line and not line.strip().isdigit():
                    f.write(line)

    remove_lines_with_numbers(txt_path, output_file)

    # 如果文本中有{***}和[***]，那么删除该内容
    def remove_content_inside_curly_brackets(file_path):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()

        content = re.sub(r'\{.*?\}', '', content)
        content = re.sub(r'\[.*?\]', '', content)

        with open(file_path, 'w', encoding='utf-8', errors='ignore') as file:
            file.write(content)

    remove_content_inside_curly_brackets(output_file)

    # 替换字符，把中文字符替换成英文字符，并且删除<i>和</i>等符号
    with open(output_file, 'r', encoding='utf-8') as file:
        content = file.read()

    old_chars = ['’', '–', '…', '“', '”', '<i>', '</i>', '- ']
    new_chars = ["'", "", ".", '"', '"', '', '', '']
    for i in range(len(old_chars)):
        content = content.replace(old_chars[i], new_chars[i])

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content)

    # 如果一行文本中末尾是"."号，那么就执行两次回车键操作，如果不是那么拼接下一行文本
    def process_text(file_name):
        output = ""
        with open(file_name, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                # 去除空白字符
                line = line.strip()
                # 检查行末是否是"."号
                if line.endswith('.'):
                    line = line + '\n' + '\n'
                    output += line  # 拼接行文本
                else:
                    output += line + " "  # 拼接行文本
        return output

    result = process_text(output_file)

    with open(output_file, "w", errors='ignore') as file:
        print(result, file=file)

    # 去掉行前面的空格
    with open(output_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w') as output_file:
        for line in lines:
            if line[0] == ' ':
                line = line[1:]
            output_file.write(line)
