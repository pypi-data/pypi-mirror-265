def generate_latex_table(data):
    # Начало таблицы
    latex_code = "\\begin{table}[h!]\n"
    latex_code += "\\centering\n"
    latex_code += "\\begin{tabular}{|" + "|".join(["c"] * len(data[0])) + "|}\n"
    latex_code += "\\hline\n"

    # Заполнение таблицы данными
    for row in data:
        latex_code += " & ".join(map(str, row)) + " \\\\ \n"
        latex_code += "\\hline\n"

    # Завершение таблицы
    latex_code += "\\end{tabular}\n"
    latex_code += "\\caption{Exemple_table}\n"
    latex_code += "\\label{tab:example}\n"
    latex_code += "\\end{table}\n"

    return latex_code


def imagetolatex(image_path, caption='exemple_image'):
    latex_code = r"""
\\begin{{figure}}
    \\centering
    \\includegraphics[width=0.5\textwidth]{{{image_path}}}
    \\caption{{{caption}}}
    \\label{{fig:image}}
\\end{{figure}}
"""
    return latex_code

def file_latex(f_table, f_image, data, image_path):
    latex_code = '''
\\documentclass{article}
\\usepackage{graphicx}
\\usepackage[utf8x]{inputenc}
\\graphicspath{{./img}}
\\begin{document}
'''
    latex_code+= f_table(data)
    latex_code+= f_image(image_path)
    
    latex_code+= '\end{document}'
    return latex_code
   

    
    