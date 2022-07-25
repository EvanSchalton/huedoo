# from typing import Optional
# import json
# import os
# PATH = "/workspaces/huedoo/huedoo/hue_api/models/resources/resource.py"

# with open(PATH) as in_file:
#     lines = in_file.readlines()

# OUTPUT_DIR = "/workspaces/huedoo/huedoo/hue_api/models/resources/output"


# def make_file_name(class_name):
#     replacement_chars = "abcdefghijklmnopqrstuvwxyz"
#     replacement_dict = dict(zip(replacement_chars.upper(), replacement_chars))
#     output: str = ""
#     for index, letter in enumerate(class_name):

#         if letter in replacement_dict:
#             if index == 0:
#                 output += replacement_dict[letter]
#                 continue

#             output += f"_{replacement_dict[letter]}"
#             continue

#         output += letter

#     return output


# import_lines: dict[str, str] = {}
# classes: dict[str, tuple[list[str], dict[str, str]]] = {}

# current_class_name: Optional[str] = None
# current_class_lines: list[str] = []
# current_class_imports: dict[str, str] = {}
# for line in lines:

#     if "import" in line:
#         imports = [i.strip() for i in line.split("import")[-1].split(",")]
#         for i in imports:
#             if i not in import_lines:
#                 import_lines[i] = line
#                 continue
#             if len(line) > import_lines[i]:
#                 import_lines[i] = line

#     # print(line)

#     if "class" in line:
#         print(current_class_name)
#         if current_class_name is not None:
#             print("\nSaving Class")
#             print(current_class_name)
#             print("\n".join(current_class_imports.values()))
#             print("\n".join(current_class_lines))
#             print()

#             classes[current_class_name] = (
#                 current_class_lines,
#                 current_class_imports
#             )
#             current_class_name = None

#         current_class_name = line.replace("class ", "").split("(")[0]
#         current_class_lines = [line]
#         current_class_imports: dict[str, str] = {}
#         print(line, current_class_name, "\n")
#         continue

#     if current_class_name is not None:
#         current_class_lines.append(line)
#         for i, line in import_lines.items():
#             if i in line:
#                 current_class_imports[i] = line


# if current_class_name is not None:
#     classes[current_class_name] = (current_class_lines, current_class_imports)
#     current_class_lines = []

# print(json.dumps(import_lines, indent=2))
# print()
# print(json.dumps(classes, indent=2))


# for klass, (lines, imports) in classes.items():
#     class_body = "".join(lines)
#     with open(os.path.join(OUTPUT_DIR, f"{make_file_name(klass)}.py"), "w+") as out_py:
#         out_py.write("".join(v for k, v in imports.items() if k in class_body))
#         out_py.write("\n")
#         out_py.write(class_body)


import os
from glob import glob
DIR = "/workspaces/huedoo/huedoo/hue_api/models/resources"

for pyfile in glob(os.path.join(DIR, "*.py")):
    print(f"from .{pyfile.split('/')[-1][:-3]} import *")
