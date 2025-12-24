import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import cv2
import main

class ModernMotionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎥 AI Motion Detection & Face Recognition")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0a0e27")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Set minimum window size
        self.root.minsize(1000, 700)
        
        self.thread = None
        self.running = False
        
        # Configure custom styles
        self.setup_styles()
        
        # Create GUI components
        self.create_header()
        self.create_main_content()
        self.create_control_panel()
        self.create_status_bar()
        
    def setup_styles(self):
        """Configure custom ttk styles for modern look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Start.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       background='#00d9ff',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=12)
        style.map('Start.TButton',
                 background=[('active', '#00b8d4')])
        
        style.configure('Stop.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       background='#ff4757',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=12)
        style.map('Stop.TButton',
                 background=[('active', '#ee5a6f')])
        
        style.configure('Register.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       background='#ffa502',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=12)
        style.map('Register.TButton',
                 background=[('active', '#ff9500')])
        
    def create_header(self):
        """Create the header section"""
        header_frame = tk.Frame(self.root, bg="#1e2749", height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(header_frame,
                              text="🎥 AI Motion Detection System",
                              font=("Segoe UI", 24, "bold"),
                              bg="#1e2749",
                              fg="#00d9ff")
        title_label.pack(side="left", padx=30, pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(header_frame,
                                 text="Real-time Face Recognition & Motion Tracking",
                                 font=("Segoe UI", 11),
                                 bg="#1e2749",
                                 fg="#8892b0")
        subtitle_label.pack(side="left", padx=10, pady=20)
        
    def create_main_content(self):
        """Create the main content area with video feed"""
        # Main container
        main_container = tk.Frame(self.root, bg="#0a0e27")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Video frame with border
        video_container = tk.Frame(main_container, bg="#1e2749", relief="flat", bd=0)
        video_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Video label with placeholder
        self.video_label = tk.Label(video_container,
                                   text="📹\n\nCamera Feed Will Appear Here\n\nClick 'Start Detection' to begin",
                                   font=("Segoe UI", 16),
                                   bg="#0f1729",
                                   fg="#8892b0",
                                   relief="flat",
                                   bd=0)
        self.video_label.pack(fill="both", expand=True, padx=3, pady=3)
        
    def create_control_panel(self):
        """Create the control panel with buttons"""
        control_frame = tk.Frame(self.root, bg="#1e2749", height=100)
        control_frame.pack(fill="x", padx=20, pady=(0, 10))
        control_frame.pack_propagate(False)
        
        # Button container for centering
        button_container = tk.Frame(control_frame, bg="#1e2749")
        button_container.pack(expand=True)
        
        # Start button
        self.start_button = tk.Button(button_container,
                                     text="▶  Start Detection",
                                     font=('Segoe UI', 12, 'bold'),
                                     bg='#00d9ff',
                                     fg='white',
                                     activebackground='#00b8d4',
                                     activeforeground='white',
                                     relief="flat",
                                     bd=0,
                                     padx=30,
                                     pady=15,
                                     cursor="hand2",
                                     command=self.start_detection)
        self.start_button.pack(side="left", padx=10)
        
        # Register button
        register_button = tk.Button(button_container,
                                   text="👤  Register New Face",
                                   font=('Segoe UI', 12, 'bold'),
                                   bg='#ffa502',
                                   fg='white',
                                   activebackground='#ff9500',
                                   activeforeground='white',
                                   relief="flat",
                                   bd=0,
                                   padx=30,
                                   pady=15,
                                   cursor="hand2",
                                   command=self.on_register_face_click)
        register_button.pack(side="left", padx=10)
        
        # Stop button
        self.stop_button = tk.Button(button_container,
                                    text="⬛  Stop Detection",
                                    font=('Segoe UI', 12, 'bold'),
                                    bg='#ff4757',
                                    fg='white',
                                    activebackground='#ee5a6f',
                                    activeforeground='white',
                                    relief="flat",
                                    bd=0,
                                    padx=30,
                                    pady=15,
                                    cursor="hand2",
                                    state="disabled",
                                    command=self.stop_detection)
        self.stop_button.pack(side="left", padx=10)
        
        # Hover effects
        self.add_hover_effect(self.start_button, "#00d9ff", "#00b8d4")
        self.add_hover_effect(register_button, "#ffa502", "#ff9500")
        self.add_hover_effect(self.stop_button, "#ff4757", "#ee5a6f")
        
    def add_hover_effect(self, button, normal_color, hover_color):
        """Add hover effect to buttons"""
        def on_enter(e):
            if button['state'] != 'disabled':
                button['background'] = hover_color
        
        def on_leave(e):
            if button['state'] != 'disabled':
                button['background'] = normal_color
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
    def create_status_bar(self):
        """Create the status bar at the bottom"""
        status_frame = tk.Frame(self.root, bg="#1e2749", height=60)
        status_frame.pack(fill="x", padx=0, pady=0, side="bottom")
        status_frame.pack_propagate(False)
        
        # Status indicator
        self.status_indicator = tk.Label(status_frame,
                                        text="●",
                                        font=("Segoe UI", 20),
                                        bg="#1e2749",
                                        fg="#64748b")
        self.status_indicator.pack(side="left", padx=20)
        
        # Status text
        self.status_text = tk.StringVar()
        self.status_text.set("Ready to start detection")
        
        status_label = tk.Label(status_frame,
                               textvariable=self.status_text,
                               font=("Segoe UI", 11),
                               bg="#1e2749",
                               fg="#8892b0",
                               anchor="w")
        status_label.pack(side="left", fill="x", expand=True, padx=10)
        
        # Info label
        info_label = tk.Label(status_frame,
                            text="Powered by OpenCV & Face Recognition",
                            font=("Segoe UI", 9),
                            bg="#1e2749",
                            fg="#64748b")
        info_label.pack(side="right", padx=20)
        
    def on_closing(self):
        """Handle window closing"""
        if self.running:
            self.stop_detection()
        self.root.destroy()
        
    def update_frame(self, frame):
        """Update the video frame in the GUI (thread-safe)"""
        try:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            
            # Calculate aspect ratio and resize
            label_width = self.video_label.winfo_width()
            label_height = self.video_label.winfo_height()
            
            if label_width > 1 and label_height > 1:
                img_aspect = img.width / img.height
                label_aspect = label_width / label_height
                
                if img_aspect > label_aspect:
                    new_width = label_width - 20
                    new_height = int(new_width / img_aspect)
                else:
                    new_height = label_height - 20
                    new_width = int(new_height * img_aspect)
                
                img = img.resize((new_width, new_height), Image.LANCZOS)
            
            imgtk = ImageTk.PhotoImage(img)
            self.root.after(0, self._update_label, imgtk)
        except Exception as e:
            print(f"[Error]: Frame update failed: {e}")
            
    def _update_label(self, imgtk):
        """Helper to update label in main thread"""
        self.video_label.configure(image=imgtk, text="")
        self.video_label.image = imgtk
        
    def update_status(self, msg):
        """Update status message (thread-safe)"""
        self.root.after(0, self._update_status_ui, msg)
        
    def _update_status_ui(self, msg):
        """Update status UI elements"""
        self.status_text.set(msg)
        
        # Update indicator color based on status
        if "started" in msg.lower() or "monitoring" in msg.lower():
            self.status_indicator.config(fg="#00d9ff")  # Blue
        elif "motion" in msg.lower():
            self.status_indicator.config(fg="#ffa502")  # Orange
        elif "error" in msg.lower() or "failed" in msg.lower():
            self.status_indicator.config(fg="#ff4757")  # Red
        elif "stopped" in msg.lower():
            self.status_indicator.config(fg="#64748b")  # Gray
        else:
            self.status_indicator.config(fg="#00d9ff")  # Blue
            
    def start_detection(self):
        """Start the detection process"""
        if not self.running:
            self.running = True
            main.stop_flag = False
            self.start_button.config(state="disabled", bg="#64748b")
            self.stop_button.config(state="normal", bg="#ff4757")
            
            self.update_status("🔍 Initializing camera...")
            
            self.thread = threading.Thread(
                target=self._run_detection,
                daemon=True
            )
            self.thread.start()
            
    def _run_detection(self):
        """Wrapper to handle detection errors"""
        try:
            main.log_motion_for_gui(self.update_frame, self.update_status)
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}")
            print(f"[ERROR]: Detection failed: {e}")
        finally:
            self.root.after(0, self._reset_buttons)
            
    def stop_detection(self):
        """Stop the detection process"""
        if self.running:
            main.stop_flag = True
            self.running = False
            self.update_status("⏳ Stopping detection...")
            self._reset_buttons()
            
    def _reset_buttons(self):
        """Reset button states"""
        self.start_button.config(state="normal", bg="#00d9ff")
        self.stop_button.config(state="disabled", bg="#64748b")
        
    def on_register_face_click(self):
        """Handle face registration"""
        main.register_new_face_threadsafe(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernMotionApp(root)
    root.mainloop()