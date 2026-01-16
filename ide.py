from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import subprocess
import sys

compiler = Tk()
compiler.title('Tbiro IDE')
compiler.geometry('800x600')

file_path = ''

def set_file_path(path):
    global file_path
    file_path = path
    compiler.title(f'PyCode IDE - {path}')

def open_file():
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
    if not path:
        return

    with open(path, 'r', encoding='utf-8') as file:
        editor.delete('1.0', END)
        editor.insert('1.0', file.read())

    set_file_path(path)

def save_file():
    global file_path

    if file_path == '':
        path = asksaveasfilename(defaultextension='.py',
                                 filetypes=[('Python Files', '*.py')])
        if not path:
            return
        file_path = path

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(editor.get('1.0', END))

    set_file_path(file_path)

def run_code():
    if file_path == '':
        save_file()
        if file_path == '':
            return

    code_output.delete('1.0', END)

    command = [sys.executable, file_path]
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    output, error = process.communicate()

    if output:
        code_output.insert(END, output)
    if error:
        code_output.insert(END, error)

# ===== MENU =====
menu_bar = Menu(compiler)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Abrir', command=open_file)
file_menu.add_command(label='Salvar', command=save_file)
file_menu.add_separator()
file_menu.add_command(label='Sair', command=compiler.quit)
menu_bar.add_cascade(label='Arquivo', menu=file_menu)

run_menu = Menu(menu_bar, tearoff=0)
run_menu.add_command(label='Rodar (F5)', command=run_code)
menu_bar.add_cascade(label='Executar', menu=run_menu)

compiler.config(menu=menu_bar)

# ===== LAYOUT =====
paned = PanedWindow(compiler, orient=VERTICAL)
paned.pack(fill=BOTH, expand=1)

editor_frame = Frame(paned)
output_frame = Frame(paned)

paned.add(editor_frame)
paned.add(output_frame)

editor_scroll = Scrollbar(editor_frame)
editor_scroll.pack(side=RIGHT, fill=Y)

editor = Text(editor_frame, undo=True)
editor.pack(fill=BOTH, expand=1)
editor.config(yscrollcommand=editor_scroll.set)
editor_scroll.config(command=editor.yview)

output_scroll = Scrollbar(output_frame)
output_scroll.pack(side=RIGHT, fill=Y)

code_output = Text(output_frame, height=10, bg='#111', fg='#0f0')
code_output.pack(fill=BOTH, expand=1)
code_output.config(yscrollcommand=output_scroll.set)
output_scroll.config(command=code_output.yview)

# Atalho F5
compiler.bind('<F5>', lambda e: run_code())

compiler.mainloop()
