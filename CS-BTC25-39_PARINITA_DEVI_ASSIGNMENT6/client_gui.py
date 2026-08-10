import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class ChatClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Client TCP Chat Application")
        self.root.geometry("550x450")

        self.client_socket = None
        self.username = ""
        self.is_connected = False

        self.build_login_window()

    # --- Login Screen ---
    def build_login_window(self):
        self.login_frame = ttk.Frame(self.root, padding=20)
        self.login_frame.pack(expand=True)

        ttk.Label(self.login_frame, text="Username:").grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = ttk.Entry(self.login_frame, width=25)
        self.username_entry.grid(row=0, column=1, pady=5)

        ttk.Label(self.login_frame, text="Server IP:").grid(row=1, column=0, sticky="w", pady=5)
        self.ip_entry = ttk.Entry(self.login_frame, width=25)
        self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self.login_frame, text="Port:").grid(row=2, column=0, sticky="w", pady=5)
        self.port_entry = ttk.Entry(self.login_frame, width=25)
        self.port_entry.insert(0, "5000")
        self.port_entry.grid(row=2, column=1, pady=5)

        self.connect_btn = ttk.Button(self.login_frame, text="Connect", command=self.connect_to_server)
        self.connect_btn.grid(row=3, column=0, columnspan=2, pady=15)

    def connect_to_server(self):
        self.username = self.username_entry.get().strip()
        server_ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()

        if not self.username:
            messagebox.showerror("Error", "Username cannot be empty!")
            return

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((server_ip, int(port)))
            
            # Send username right after connecting
            self.client_socket.send(self.username.encode('utf-8'))
            self.is_connected = True

            # Switch to chat window
            self.login_frame.destroy()
            self.build_chat_window()

            # Start background thread to listen for incoming messages
            threading.Thread(target=self.receive_messages, daemon=True).start()

        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")

    # --- Chat Interface Screen ---
    def build_chat_window(self):
        # Top Header
        top_frame = ttk.Frame(self.root, padding=5)
        top_frame.pack(fill="x")

        self.status_label = ttk.Label(
            top_frame, 
            text=f"User: {self.username} | Status: Connected", 
            foreground="green"
        )
        self.status_label.pack(side="left")

        self.disconnect_btn = ttk.Button(top_frame, text="Disconnect", command=self.disconnect)
        self.disconnect_btn.pack(side="right")

        # Chat Area (Scrolled text display)
        body_frame = ttk.Frame(self.root, padding=5)
        body_frame.pack(fill="both", expand=True)

        self.chat_area = scrolledtext.ScrolledText(body_frame, state='disabled', wrap='word')
        self.chat_area.pack(fill="both", expand=True)

        # Bottom Input Area
        bottom_frame = ttk.Frame(self.root, padding=5)
        bottom_frame.pack(fill="x")

        self.msg_entry = ttk.Entry(bottom_frame)
        self.msg_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.msg_entry.bind("<Return>", lambda event: self.send_message())

        self.send_btn = ttk.Button(bottom_frame, text="Send", command=self.send_message)
        self.send_btn.pack(side="right")

    def send_message(self):
        msg = self.msg_entry.get().strip()
        if msg and self.is_connected:
            try:
                self.client_socket.send(msg.encode('utf-8'))
                # Show own sent message locally in chat window
                if not msg.startswith("/msg "):
                    self.display_message(f"You: {msg}")
                self.msg_entry.delete(0, tk.END)
            except Exception as e:
                self.display_message(f"Error sending message: {e}")

    def receive_messages(self):
        """Runs in background thread to continuously read messages from server."""
        while self.is_connected:
            try:
                msg = self.client_socket.recv(1024).decode('utf-8')
                if not msg:
                    break
                self.display_message(msg)
            except:
                break

    def display_message(self, msg):
        """Safely appends message to chat text widget."""
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, msg + "\n")
        self.chat_area.see(tk.END)  # Auto-scroll to bottom
        self.chat_area.config(state='disabled')

    def disconnect(self):
        self.is_connected = False
        if self.client_socket:
            self.client_socket.close()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClientGUI(root)
    root.mainloop()
