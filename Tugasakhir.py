import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from collections import deque

class WarnetSystem:
    def __init__(self):
        self.computers = {f"PC-{i+1}": None for i in range(5)}  
        self.queue = deque()  
        self.history = []  
        self.price_per_hour = 5000  

    def book_computer(self, name, pc_name):
        if pc_name in self.computers and self.computers[pc_name] is None:
            self.computers[pc_name] = {"name": name, "start_time": datetime.now()}
            self.history.append((pc_name, name))
            return f"{name} berhasil memesan {pc_name} pada {self.computers[pc_name]['start_time']:%H:%M}"
        elif pc_name in self.computers and self.computers[pc_name] is not None:
            self.queue.append(name)
            return f"{pc_name} sudah digunakan, {name} masuk antrean."
        else:
            return f"{pc_name} tidak valid."
        
    def reset_system(self):
        self.computers = {f"PC-{i+1}": None for i in range(5)}  
        self.queue.clear()
        self.history.clear()
        return "udah tutup"

    def release_computer(self, pc_name):
        if pc_name in self.computers and self.computers[pc_name]:
            user_data = self.computers[pc_name]
            name = user_data["name"]
            start_time = user_data["start_time"]
            end_time = datetime.now()
            duration = (end_time - start_time).seconds // 60
            duration_in_hours = duration / 60
            cost = round(duration_in_hours * self.price_per_hour)

            self.computers[pc_name] = None

            if self.queue:
                next_user = self.queue.popleft()
                self.computers[pc_name] = {"name": next_user, "start_time": datetime.now()}
                return f"{name} selesai menggunakan {pc_name}. Durasi: {duration} menit ({duration_in_hours:.2f} jam). Biaya: Rp {cost}.\n{next_user} sekarang menggunakan {pc_name}."
            
            return f"{name} selesai menggunakan {pc_name}. Durasi: {duration} menit ({duration_in_hours:.2f} jam). Biaya: Rp {cost}."
        return "belum masuk udah selesai aja"
    def get_status(self):
        status = "Status Komputer:\n"
        for pc, user_data in self.computers.items():
            if user_data:
                name = user_data["name"]
                start_time = user_data["start_time"]
                status += f"{pc}: {name} (Mulai: {start_time:%H:%M:%S})\n"
            else:
                status += f"{pc}: masih kosong\n"
        
        status += "\nDisini antrinya:\n"
        status += ", ".join(self.queue) if self.queue else "ini tempat antri"
        return status
    
class WarnetGUI:
    def __init__(self, root):
        self.warnet = WarnetSystem()
        self.root = root
        self.root.title("Booking kumanet")
        self.root.configure(bg="#0A0A3F")  
        self.create_widgets()

    def create_widgets(self):
        self.label_title = tk.Label(
            self.root, 
            text="Booking kumanet", 
            font=("Comic Sans MS", 30, "bold"), 
            bg="#FF0000",  
            fg="white",
            pady=5
        )
        self.label_title.pack(fill="x")

        self.text_status = tk.Text(
            self.root, 
            height=12, 
            width=50, 
            state="disabled", 
            bg="#002B5B",  
            fg="white", 
            font=("Courier", 12, "bold")
        )
        self.text_status.pack(pady=20)

        self.label_name = tk.Label(
            self.root, 
            text="Nama Pelanggan:", 
            bg="#0A0A3F", 
            fg="#FF5555", 
            font=("Arial", 12, "italic")
        )
        self.label_name.pack()
        self.entry_name = tk.Entry(
            self.root, 
            bg="#333", 
            fg="#FF5555", 
            insertbackground="#FF5555", 
            font=("Arial", 12)
        )
        self.entry_name.pack(pady=10)

        self.label_pc = tk.Label(
            self.root, 
            text="Pilih Komputer:", 
            bg="#0A0A3F", 
            fg="#FF5555", 
            font=("Arial", 12, "italic")
        )
        self.label_pc.pack()
        self.pc_options = tk.StringVar()
        self.pc_options.set("PC-1")
        self.computer_menu = tk.OptionMenu(
            self.root, self.pc_options, *self.warnet.computers.keys()
        )
        self.computer_menu.config(
            bg="#333", 
            fg="#FF5555", 
            font=("Arial", 12)
        )
        self.computer_menu.pack(pady=20)
        
        self.button_book = tk.Button(
            self.root, 
            text="Booking Komputer", 
            command=self.book_computer, 
            bg="#FF3333", 
            fg="white", 
            font=("Verdana", 14, "bold"), 
            relief="raised"
        )
        self.button_book.pack(pady=10, fill="x", padx=50)

        self.button_release = tk.Button(
            self.root, 
            text="Selesai Menggunakan", 
            command=self.release_computer, 
            bg="#FF6666", 
            fg="white", 
            font=("Verdana", 14, "bold"), 
            relief="raised"
        )
        self.button_release.pack(pady=10, fill="x", padx=50)

        self.button_reset = tk.Button(
            self.root, 
            text="Reset Sistem", 
            command=self.reset_system, 
            bg="#FF9933", 
            fg="white", 
            font=("Verdana", 14, "bold"), 
            relief="raised"
        )
        self.button_reset.pack(pady=10, fill="x", padx=50)

        self.update_status()

    def book_computer(self):
        name = self.entry_name.get().strip()
        pc_name = self.pc_options.get()
        if name:
            result = self.warnet.book_computer(name, pc_name)
            messagebox.showinfo("ALERTA!!!", result)
            self.entry_name.delete(0, tk.END)
        else:
            messagebox.showwarning("ALERTA!!!", "isi nama dulu")
        self.update_status()

    def release_computer(self):
        pc_name = self.pc_options.get()
        result = self.warnet.release_computer(pc_name)
        messagebox.showinfo("ALERTA!!!", result)
        self.update_status()
        
    def reset_system(self):
        result = self.warnet.reset_system()
        messagebox.showinfo("Sistem Reset", result)
        self.update_status()

    def update_status(self):
        status = self.warnet.get_status()
        self.text_status.config(state="normal")
        self.text_status.delete(1.0, tk.END)
        self.text_status.insert(tk.END, status)
        self.text_status.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = WarnetGUI(root)
    root.mainloop()
