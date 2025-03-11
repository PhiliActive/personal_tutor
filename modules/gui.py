import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter.font import Font
from modules.meeting_manager import MeetingManager
from modules.logger import logger

class MISGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Tutor Meeting Tracker")
        self.root.geometry("800x700")  # Adjusted window size
        self.root.configure(bg="#F5F5F5")  # Light background
        self.root.overrideredirect(True)  # Remove default title bar

        # Initialize MeetingManager
        self.meeting_manager = MeetingManager()

        # Custom fonts
        self.title_font = Font(family="Helvetica", size=18, weight="bold")
        self.label_font = Font(family="Helvetica", size=12)
        self.button_font = Font(family="Helvetica", size=10, weight="bold")

        # Create custom title bar
        self.create_custom_title_bar()

        # Create styles
        self.create_styles()

        # Create GUI elements
        self.create_widgets()

    def create_custom_title_bar(self):
        """Create a custom title bar with #5f295f background."""
        # Title bar frame
        title_bar = tk.Frame(self.root, bg="#5f295f", relief="raised", bd=0)
        title_bar.pack(fill=tk.X)

        # Title label
        title_label = tk.Label(
            title_bar,
            text="Personal Tutor Meeting Tracker",
            font=self.title_font,
            fg="white",  # White text
            bg="#5f295f"  # Deep purple background
        )
        title_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Close button
        close_button = tk.Button(
            title_bar,
            text="×",
            font=self.title_font,
            fg="black",  # Black text
            bg="#5f295f",
            bd=0,
            command=self.root.destroy  # Close the application
        )
        close_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Bind mouse events to allow dragging the window
        title_bar.bind("<ButtonPress-1>", self.start_move)
        title_bar.bind("<ButtonRelease-1>", self.stop_move)
        title_bar.bind("<B1-Motion>", self.on_move)

    def start_move(self, event):
        """Start moving the window."""
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        """Stop moving the window."""
        self.x = None
        self.y = None

    def on_move(self, event):
        """Move the window."""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def create_styles(self):
        """Creates custom styles for widgets."""
        style = ttk.Style()
        style.configure("TLabel", foreground="black", background="#F5F5F5", font=self.label_font)
        style.configure("TButton", font=self.button_font, padding=10, background="#5f295f", foreground="black")  # Black text
        style.configure("Accent.TButton", font=self.button_font, padding=10, background="#5f295f", foreground="black", borderwidth=5, focusthickness=3, focuscolor='none')  # Black text
        style.configure("TEntry", font=self.label_font, padding=5)


    def create_widgets(self):
        """Create and arrange GUI elements."""
        # Main frame for the content
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Add meeting frame (using grid for column layout)
        add_frame = ttk.Frame(main_frame)
        add_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Configure grid weights for resizing
        add_frame.grid_columnconfigure(1, weight=1)  # Make the second column expandable

        # Date input
        ttk.Label(add_frame, text="Date (YYYY-MM-DD):", style="TLabel").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = ttk.Entry(add_frame, font=self.label_font, style="TEntry")
        self.date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")  # Expand horizontally

        # Time input
        ttk.Label(add_frame, text="Time (HH:MM):", style="TLabel").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.time_entry = ttk.Entry(add_frame, font=self.label_font, style="TEntry")
        self.time_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")  # Expand horizontally

        # Topics input
        ttk.Label(add_frame, text="Topics:", style="TLabel").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.topics_entry = ttk.Entry(add_frame, font=self.label_font, style="TEntry")
        self.topics_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")  # Expand horizontally

        # Referrals input
        ttk.Label(add_frame, text="Referrals:", style="TLabel").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.referrals_entry = ttk.Entry(add_frame, font=self.label_font, style="TEntry")
        self.referrals_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")  # Expand horizontally

        # Add meeting button (styled with #5f295f and black text)
        add_button = ttk.Button(
            add_frame,
            text="Add Meeting",
            command=self.add_meeting,
            style="Accent.TButton"
        )
        add_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")  # Full width row

        # View/Search frame
        view_frame = ttk.Frame(main_frame)
        view_frame.pack(fill=tk.X, pady=10)

        # Configure grid weights for resizing
        view_frame.grid_columnconfigure(1, weight=1)  # Make the search entry expandable

        # View all button (styled with #5f295f and black text)
        view_button = ttk.Button(
            view_frame,
            text="View All Meetings",
            command=self.view_all_meetings,
            style="Accent.TButton"
        )
        view_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Search entry
        self.search_entry = ttk.Entry(view_frame, font=self.label_font, style="TEntry")
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")  # Expand horizontally

        # Search button (styled with #5f295f and black text)
        search_button = ttk.Button(
            view_frame,
            text="Search",
            command=self.search_meetings,
            style="Accent.TButton"
        )
        search_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")  # Expand horizontally

        # Clear button (styled with #5f295f and black text)
        clear_button = ttk.Button(
            view_frame,
            text="Clear",
            command=self.clear_results,
            style="Accent.TButton"
        )
        clear_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")  # Place next to the search button

        # Result text area
        self.result_text = scrolledtext.ScrolledText(
            main_frame,
            font=self.label_font,
            bg="white",
            fg="black",  # Black text on white background
            insertbackground="black"
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=10)

    def clear_results(self):
        """Clear the result text area."""
        self.result_text.delete(1.0, tk.END)  # Clear all text
        logger.info("Cleared the result text area.")

    def add_meeting(self):
        """Add a new meeting."""
        date = self.date_entry.get()
        time = self.time_entry.get()
        topics = self.topics_entry.get()
        referrals = self.referrals_entry.get()

        # Call the add_meeting function and get the result
        success, message = self.meeting_manager.add_meeting(date, time, topics, referrals)

        # Display the result in a messagebox
        if success:
            messagebox.showinfo("Success", message)
            self.date_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)
            self.topics_entry.delete(0, tk.END)
            self.referrals_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", message)

    def view_all_meetings(self):
        """View all meetings."""
        try:
            meetings = self.meeting_manager.view_all_meetings()
            self.result_text.delete(1.0, tk.END)  # Clear the text area
            if not meetings:
                self.result_text.insert(tk.END, "No meetings found.\n")
            else:
                self.result_text.insert(tk.END, "--- All Meetings ---\n\n")
                for meeting in meetings:
                    self.result_text.insert(tk.END, f"ID: {meeting[0]}, Date: {meeting[1]}, Time: {meeting[2]}, Topics: {meeting[3]}, Referrals: {meeting[4]}\n\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve meetings: {e}")

    def search_meetings(self):
        """Search meetings by keyword."""
        keyword = self.search_entry.get()
        if not keyword:
            messagebox.showwarning("Input Error", "Please enter a search keyword.")
            return

        try:
            meetings = self.meeting_manager.search_meetings(keyword)
            self.result_text.delete(1.0, tk.END)  # Clear the text area
            if not meetings:
                self.result_text.insert(tk.END, f"No meetings found matching '{keyword}'.\n")
            else:
                self.result_text.insert(tk.END, f"--- Meetings Matching '{keyword}' ---\n")
                for meeting in meetings:
                    self.result_text.insert(tk.END, f"ID: {meeting[0]}, Date: {meeting[1]}, Time: {meeting[2]}, Topics: {meeting[3]}, Referrals: {meeting[4]}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search meetings: {e}")