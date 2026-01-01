import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import main
import cv2
import sys
import os

# Adjust sys.path to include src directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import main module functions
from src import main


# Main application class
class ModernMotionApp:

    # Initialize the main GUI window and all components
    def __init__(self, root):
        self.root = root
        self.root.title("🎥 AI Motion Detection & Face Recognition")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0a0e27")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.minsize(1000, 700)

        self.thread = None
        self.running = False

        self.setup_styles()
        self.create_header()
        self.create_main_content()
        self.create_control_panel()
        self.create_status_bar()

    # Setup custom styles for buttons and widgets
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Start button style
        style.configure('Start.TButton',
                        font=('Segoe UI', 11, 'bold'),
                        background='#00d9ff',
                        foreground='white',
                        borderwidth=0,
                        focuscolor='none',
                        padding=12)
        style.map('Start.TButton', background=[('active', '#00b8d4')])

        # Stop button style
        style.configure('Stop.TButton',
                        font=('Segoe UI', 11, 'bold'),
                        background='#ff4757',
                        foreground='white',
                        borderwidth=0,
                        focuscolor='none',
                        padding=12)
        style.map('Stop.TButton', background=[('active', '#ee5a6f')])

        # Register button style
        style.configure('Register.TButton',
                        font=('Segoe UI', 11, 'bold'),
                        background='#ffa502',
                        foreground='white',
                        borderwidth=0,
                        focuscolor='none',
                        padding=12)
        style.map('Register.TButton', background=[('active', '#ff9500')])

    # Create header section with title and subtitle
    def create_header(self):
        header_frame = tk.Frame(self.root, bg="#1e2749", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        # Title label
        title_label = tk.Label(header_frame,
                               text="🎥 AI Motion Detection System",
                               font=("Segoe UI", 24, "bold"),
                               bg="#1e2749",
                               fg="#00d9ff")
        title_label.pack(side="left", padx=30, pady=20)

        # Subtitle label
        subtitle_label = tk.Label(header_frame,
                                  text="Real-time Face Recognition & Motion Tracking",
                                  font=("Segoe UI", 11),
                                  bg="#1e2749",
                                  fg="#8892b0")
        subtitle_label.pack(side="left", padx=10, pady=20)

    # Create main content area for video feed
    def create_main_content(self):
        main_container = tk.Frame(self.root, bg="#0a0e27")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Video container
        video_container = tk.Frame(main_container, bg="#1e2749", relief="flat", bd=0)
        video_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Video display label
        self.video_label = tk.Label(video_container,
                                    text="📹\n\nCamera Feed Will Appear Here\n\nClick 'Start Detection' to begin",
                                    font=("Segoe UI", 16),
                                    bg="#0f1729",
                                    fg="#8892b0",
                                    relief="flat",
                                    bd=0)
        self.video_label.pack(fill="both", expand=True, padx=3, pady=3)

    # Create control panel with Start, Stop, and Register buttons
    def create_control_panel(self):
        control_frame = tk.Frame(self.root, bg="#1e2749", height=100)
        control_frame.pack(fill="x", padx=20, pady=(0, 10))
        control_frame.pack_propagate(False)

        # Button container
        button_container = tk.Frame(control_frame, bg="#1e2749")
        button_container.pack(expand=True)

        # Start button
        self.start_button = tk.Button(button_container,
                                      text="▶ Start Detection",
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

        # Register Face button
        register_button = tk.Button(button_container,
                                    text="👤 Register New Face",
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
                                     text="⬛ Stop Detection",
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

        # Add hover effects to buttons
        self.add_hover_effect(self.start_button, "#00d9ff", "#00b8d4")
        self.add_hover_effect(register_button, "#ffa502", "#ff9500")
        self.add_hover_effect(self.stop_button, "#ff4757", "#ee5a6f")

    # Add hover effect to buttons
    def add_hover_effect(self, button, normal_color, hover_color):

        # Enter event handler
        def on_enter(e):
            if button['state'] != 'disabled':
                button['background'] = hover_color

        # Leave event handler
        def on_leave(e):
            if button['state'] != 'disabled':
                button['background'] = normal_color

        # Bind events to button
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    # Create status bar at the bottom of the window
    def create_status_bar(self):
        status_frame = tk.Frame(self.root, bg="#1e2749", height=60)
        status_frame.pack(fill="x", side="bottom")
        status_frame.pack_propagate(False)

        # Status indicator (colored dot)
        self.status_indicator = tk.Label(status_frame,
                                         text="●",
                                         font=("Segoe UI", 20),
                                         bg="#1e2749",
                                         fg="#64748b")
        self.status_indicator.pack(side="left", padx=20)

        # Status text
        self.status_text = tk.StringVar()
        self.status_text.set("Ready to start detection")

        # Status label
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


    # Handle window closing event
    def on_closing(self):
        if self.running:
            self.stop_detection()
        self.root.destroy()

    # Update the video frame in the GUI
    def update_frame(self, frame):
        try:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)

            label_width = self.video_label.winfo_width()
            label_height = self.video_label.winfo_height()

            # Resize image to fit label while maintaining aspect ratio
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

            # Convert to ImageTk format
            imgtk = ImageTk.PhotoImage(img)
            self.root.after(0, self._update_label, imgtk)
        except Exception as e:
            print(f"[Error]: Frame update failed: {e}")

    # Internal method to update the video label
    def _update_label(self, imgtk):
        self.video_label.configure(image=imgtk, text="")
        self.video_label.image = imgtk

    # Update the status message in the GUI
    def update_status(self, msg):
        self.root.after(0, self._update_status_ui, msg)

    # Internal method to update status text and color indicator
    def _update_status_ui(self, msg):
        self.status_text.set(msg)
        if "started" in msg.lower() or "monitoring" in msg.lower():
            self.status_indicator.config(fg="#00d9ff")
        elif "motion" in msg.lower():
            self.status_indicator.config(fg="#ffa502")
        elif "error" in msg.lower() or "failed" in msg.lower():
            self.status_indicator.config(fg="#ff4757")
        elif "stopped" in msg.lower():
            self.status_indicator.config(fg="#64748b")
        else:
            self.status_indicator.config(fg="#00d9ff")

    # Start the motion detection in a new thread
    def start_detection(self):
        if not self.running:
            self.running = True
            main.stop_flag = False
            self.start_button.config(state="disabled", bg="#64748b")
            self.stop_button.config(state="normal", bg="#ff4757")
            self.update_status("🔍 Initializing camera...")

            self.thread = threading.Thread(target=self._run_detection, daemon=True)
            self.thread.start()

    # Run the motion detection loop
    def _run_detection(self):
        try:
            main.log_motion_for_gui(self.update_frame, self.update_status)
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}")
            print(f"[ERROR]: Detection failed: {e}")
        finally:
            self.root.after(0, self._reset_buttons)

    # Stop the motion detection
    def stop_detection(self):
        if self.running:
            main.stop_flag = True
            self.running = False
            self.update_status("⏳ Stopping detection...")
            self._reset_buttons()

    # Reset Start/Stop buttons to default state
    def _reset_buttons(self):
        self.start_button.config(state="normal", bg="#00d9ff")
        self.stop_button.config(state="disabled", bg="#64748b")

    # Register a new face safely
    def on_register_face_click(self):
        main.register_new_face_threadsafe(self.root)

# Launch the GUI application
def main_app():
    """Launch the GUI application"""
    root = tk.Tk()
    app = ModernMotionApp(root)
    root.mainloop()

# Run the GUI application
if __name__ == "__main__":
    main_app()