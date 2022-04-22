import tkinter as tk
from tkinter.filedialog import askdirectory
import dense


class ReadF:

    def open_file(self):

        # открыть папку
        self.directorypath = askdirectory()

        # очистить текст бокс
        txt_edit.delete("1.0", tk.END)

        message = f'''{self.directorypath} - папка открыта!
'''
        txt_edit.insert(tk.END, message)

    def clicked(self):

        self.resalt()

    def resalt(self):

        text = self.directorypath
        text = dense.run(text)
        for n, i in enumerate(text):
            if i:
                message = f'''{i}
'''
                txt_edit.insert(tk.END, message, )


def close():
    window.destroy()


window = tk.Tk()
window.title("Анализ аудиодефекта - высокочастотный гул")

window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=1200, weight=1)

txt_edit = tk.Text(window)
fr_buttons = tk.Frame(window)

rf = ReadF()
btn_open = tk.Button(fr_buttons, text="Открыть", command=rf.open_file)
btn_save = tk.Button(fr_buttons, text="Анализ", command=rf.clicked)
btn_close = tk.Button(fr_buttons, text="Выход", command=close)

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)
btn_close.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")


window.mainloop()