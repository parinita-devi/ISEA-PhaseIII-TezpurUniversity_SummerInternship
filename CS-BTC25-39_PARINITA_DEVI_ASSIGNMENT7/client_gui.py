import socket
import tkinter as tk
from tkinter import messagebox

SERVER_IP = "10.0.0.1"
SERVER_PORT = 12345

class ApplicationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Assignment 7 - Secure Client GUI")
        self.root.geometry("380x300")
        self.sock = None

        tk.Label(root, text="Secure Network Client", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(root, text="Username:").pack()
        self.entry_user = tk.Entry(root)
        self.entry_user.pack(pady=5)

        tk.Label(root, text="Password:").pack()
        self.entry_pass = tk.Entry(root, show="*")
        self.entry_pass.pack(pady=5)

        self.btn_login = tk.Button(root, text="Login", command=self.login, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.btn_login.pack(pady=10)

        self.lbl_status = tk.Label(root, text="Status: Disconnected", fg="gray")
        self.lbl_status.pack(pady=5)

    def connect_server(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((SERVER_IP, SERVER_PORT))
            self.lbl_status.config(text="Status: Connected", fg="green")
            return True
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to server: {e}")
            self.lbl_status.config(text="Status: Disconnected", fg="red")
            return False

    def login(self):
        if not self.sock:
            if not self.connect_server():
                return

        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        if not username or not password:
            messagebox.showwarning("Warning", "Please enter both username and password.")
            return

        try:
            request = f"LOGIN|{username}|{password}"
            self.sock.sendall(request.encode())

            response = self.sock.recv(1024).decode()

            if "AUTH_SUCCESS" in response or "SUCCESS" in response:
                messagebox.showinfo("Success", "Authentication Successful!")
                self.lbl_status.config(text=f"Logged in as: {username}", fg="green")
            else:
                messagebox.showerror("Auth Error", response)
                if "locked" in response.lower():
                    self.sock.close()
                    self.sock = None
        except Exception as e:
            messagebox.showerror("Error", f"Communication failed: {e}")
            self.sock = None

if __name__ == "__main__":
    root = tk.Tk()
    app = ApplicationGUI(root)
    root.mainloop()