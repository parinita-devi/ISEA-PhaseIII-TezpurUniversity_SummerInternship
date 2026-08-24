import socket
import tkinter as tk
from tkinter import messagebox
import json
import time

with open("config.json", "r") as f:
    CONFIG = json.load(f)

SERVER_IP = CONFIG["server_ip"]
SERVER_PORT = CONFIG["server_port"]

class ApplicationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Assignment 8 - Scalable Client GUI")
        self.root.geometry("380x320")
        self.sock = None
        self.is_connected = False

        tk.Label(root, text="Scalable Network Client", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(root, text="Username:").pack()
        self.entry_user = tk.Entry(root)
        self.entry_user.pack(pady=5)

        tk.Label(root, text="Password:").pack()
        self.entry_pass = tk.Entry(root, show="*")
        self.entry_pass.pack(pady=5)

        self.btn_login = tk.Button(root, text="Login", command=self.login, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.btn_login.pack(pady=10)

        self.lbl_status = tk.Label(root, text="Status: Connecting...", fg="orange")
        self.lbl_status.pack(pady=5)

        self.connect_server()

    def connect_server(self, retries=3):
        for attempt in range(retries):
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.settimeout(5.0)
                self.sock.connect((SERVER_IP, SERVER_PORT))
                self.is_connected = True
                self.lbl_status.config(text=f"Status: Connected to {SERVER_IP}", fg="green")
                return True
            except Exception:
                self.lbl_status.config(text=f"Reconnecting (Attempt {attempt+1}/{retries})...", fg="orange")
                time.sleep(1)
        
        self.lbl_status.config(text="Status: Disconnected", fg="red")
        self.is_connected = False
        return False

    def login(self):
        if not self.is_connected:
            if not self.connect_server():
                messagebox.showerror("Error", "Server unreachable.")
                return

        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        if not username or not password:
            messagebox.showwarning("Warning", "Please enter username and password.")
            return

        try:
            request = f"LOGIN|{username}|{password}"
            self.sock.sendall(request.encode())

            response = self.sock.recv(1024).decode()

            if "AUTH_SUCCESS" in response:
                messagebox.showinfo("Success", response)
                self.lbl_status.config(text=f"Status: Logged in as {username}", fg="blue")
            else:
                messagebox.showerror("Auth Error", response)
        except Exception as e:
            messagebox.showerror("Connection Lost", "Attempting automatic reconnect...")
            self.sock = None
            self.connect_server()

if __name__ == "__main__":
    root = Tk = tk.Tk()
    app = ApplicationGUI(root)
    root.mainloop()