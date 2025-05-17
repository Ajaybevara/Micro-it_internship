import tkinter as tk
import time

def update_clock():
    current_time = time.strftime('%H:%M:%S')
    current_date = time.strftime('%A, %d %B %Y')
    time_label.config(text=current_time)
    date_label.config(text=current_date)
    time_label.after(1000, update_clock)
root = tk.Tk()
root.title("Digital Clock")
root.geometry("400x200")
root.configure(bg="#1e1e1e")
date_label = tk.Label(root, font=('Arial', 16), fg='cyan', bg='#1e1e1e')
date_label.pack(pady=10)
time_label = tk.Label(root, font=('Arial', 48, 'bold'), fg='lime', bg='#1e1e1e')
time_label.pack(pady=10)

update_clock()
root.mainloop()
