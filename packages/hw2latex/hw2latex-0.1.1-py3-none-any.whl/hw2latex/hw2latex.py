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
    latex_code += "\\caption{Пример таблицы}\n"
    latex_code += "\\label{tab:example}\n"
    latex_code += "\\end{table}\n"

    return latex_code


def imagetolatex(image_path, caption):
    latex_code = f"""
\\begin{{figure}}
    \\centering
    \\includegraphics{{{image_path}}}
    \\caption{{{caption}}}
    \\label{{fig:image}}
\\end{{figure}}
"""
    return latex_code
