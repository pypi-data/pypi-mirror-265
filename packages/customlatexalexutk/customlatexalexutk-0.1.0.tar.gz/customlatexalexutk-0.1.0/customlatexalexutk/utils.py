from typing import Any, Literal
import os

def generate_table(list_of_lists: list[list[str]], align_letter: Literal["l", "c", "r"]):
    assert align_letter in ["l", "c", "r"]
    
    n_cols = len(list_of_lists[0])  # number of cols for |c|c|c|
    tabular_annotation = '|'.join([f'{align_letter}'] * n_cols)  # crating |c|c|c|
    # formatting each row of table to `cell1 & cell2 & cell3 \\`
    table_contents = [' ' + ' & '.join(row) + '\\\\' for row in list_of_lists]
    table_contents_str = '\n'.join(table_contents)
    for row in list_of_lists:
        ' ' + ' & '.join(row) + '\\\\'
    latex_table = ('\\begin{center}\n'
                   f'\\begin{{tabular}}{{ |{tabular_annotation}| }}\n'
                   '\\hline\n'
                   f'{table_contents_str}\n'
                   '\\hline\n'
                   '\\end{tabular}\n'
                   '\\end{center}\n')

    return latex_table


def tex_file_wrapper(graphicspath_string, /, *tex_blocks):
    tex_blocks_joined = '\n'.join(tex_blocks)
    
    latex_file = ('\\documentclass{article}\n'
                  '\\usepackage{graphicx}\n'
                  '\\usepackage[utf8x]{inputenc}\n'
                  f'{graphicspath_string}\n'
                  '\\begin{document}\n'
                  f'{tex_blocks_joined}\n'
                  '\\end{document}')

    return latex_file


def generate_graphics_path(*image_folders):
    image_folders = set(image_folders)
    graphicspath_string =  '}{'.join(image_folders)
    graphicspath_string = f'\\graphicspath{{{{{graphicspath_string}}}}}'
    
    return graphicspath_string


def generate_image(image_path):
    image_folder, file_name = os.path.split(image_path)
    return image_folder, f'\\includegraphics{{{file_name}}}'

