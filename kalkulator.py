import tkinter as tk
from tkinter import messagebox
import sqlite3

# Fungsi untuk menghitung ekspresi matematika
def calculate():
    try:
        result = eval(entry.get())
        if isinstance(result, int):
            result_label.config(text="Hasil: {}".format(result)) 
        else:
            result_label.config(text="Hasil: {:.2f}".format(result)) 
        save_to_history(entry.get(), result) 
    except Exception as e: 
        messagebox.showerror("Error", str(e)) 

# Fungsi untuk menyimpan perhitungan ke dalam database SQLite3
def save_to_history(expression, result):
    conn = sqlite3.connect('calculator_history.db') 
    c = conn.cursor() 
    c.execute("CREATE TABLE IF NOT EXISTS history (expression TEXT, result REAL)")
    c.execute("INSERT INTO history VALUES (?, ?)", (expression, result))
    conn.commit() 
    conn.close()
 
# Fungsi untuk menampilkan histori perhitungan
def show_history():
    conn = sqlite3.connect('calculator_history.db') 
    c = conn.cursor()
    c.execute("SELECT * FROM history")
    history = c.fetchall()
    conn.close()
    if not history:
        messagebox.showinfo("Info", "Histori kosong")
        return

    history_window = tk.Toplevel(root)
    history_window.title("History")
    history_label = tk.Label(history_window, text="History:")
    history_label.grid(row=0, column=0, padx=10, pady=5)
    row_num = 1
    for item in history:
        expression, result = item
        history_text = expression + " = {:.2f}".format(result)
        history_item_label = tk.Label(history_window, text=history_text)
        history_item_label.grid(row=row_num, column=0, padx=10, pady=2, sticky="w")

        # Tombol untuk memasukkan hasil histori ke kotak masukan
        insert_button = tk.Button(history_window, text="Gunakan", command=lambda res=result: insert_history_result(res))
        insert_button.grid(row=row_num, column=1, padx=5, pady=2, sticky="e")

        row_num += 1
        
# Fungsi untuk memasukkan hasil histori ke kotak masukan
def insert_history_result(result):
    entry.delete(0, tk.END)  
    entry.insert(tk.END, str(result))  
    
# Fungsi untuk membersihkan kotak masukan
def clear_entry():
    entry.delete(0, tk.END) 

# Membuat GUI
root = tk.Tk() 
root.title("Kalkulator") 
root.configure(bg='black') 
root.geometry("350x600")  
root.resizable(False, False) 

# Frame untuk hasil dan kotak masukan
result_frame = tk.Frame(root, bg="#000000")  
result_frame.pack(pady=10) 

entry = tk.Entry(result_frame, width=25, font=("Segoe UI", 20), bd=5, justify="right", bg="#000000", fg="#ffffff")

entry.pack(padx=10, pady=10)

result_label = tk.Label(result_frame, text="Hasil: ", font=("Segoe UI", 14), bg="#000000", fg="#ffffff")

result_label.pack(padx=10, pady=5) 

# Frame untuk tombol-tombol kalkulator
button_frame = tk.Frame(root, bg="#000000")  
button_frame.pack() 

buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '+',  '%' , '=', 'C'
]

row_num = 1
col_num = 0
for button in buttons: #Memulai iterasi melalui setiap elemen dalam list tombol.
    if button == '=':
        tk.Button(button_frame, text=button, width=6, height=2, font=("Segoe UI", 14), bg="#0078D7", fg="#ffffff", command=calculate).grid(row=row_num, column=col_num, padx=5, pady=5)
    elif button == '0':
        tk.Button(button_frame, text=button, width=14, height=2, font=("Segoe UI", 14), bg="#202020", fg="#ffffff", command=lambda b=button: entry.insert(tk.END, b)).grid(row=row_num, column=col_num, columnspan=2, padx=5, pady=5)
        col_num += 1
    elif button == 'C':
        tk.Button(button_frame, text=button, width=6, height=2, font=("Segoe UI", 14), bg="#D70000", fg="#ffffff", command=clear_entry).grid(row=row_num, column=col_num, padx=5, pady=5)
    elif button == '%':
        tk.Button(button_frame, text=button, width=6, height=2, font=("Segoe UI", 14), bg="#202020", fg="#ffffff", command=lambda b=button: entry.insert(tk.END, b)).grid(row=row_num, column=col_num, padx=5, pady=5)
    else:
        tk.Button(button_frame, text=button, width=6, height=2, font=("Segoe UI", 14), bg="#202020", fg="#ffffff", command=lambda b=button: entry.insert(tk.END, b)).grid(row=row_num, column=col_num, padx=5, pady=5)
    col_num += 1
    if col_num > 3:
        col_num = 0
        row_num += 1
    

# Tombol untuk menampilkan histori
history_button = tk.Button(root, text="History", font=("Segoe UI", 12), bg="#000000", fg="#ffffff", command=show_history)
history_button.pack(pady=5)

root.mainloop()
#Memulai event loop utama aplikasi, sehingga aplikasi akan terus berjalan hingga jendela ditutup.#
