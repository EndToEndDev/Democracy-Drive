import xml.etree.ElementTree as ET
import customtkinter as ctk
from tkinter import messagebox
import threading

def code():
    print("Read function triggered!")  # Debug print statement

    # Function to read and sort XML data by 'date'
    def read_and_sort_xml(file_path):
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Parse the XML entries into a list of dictionaries
            entries = []
            for entry in root.findall('entry'):
                name = entry.find('name').text
                answer = entry.find('answer').text
                date = entry.find('date').text
                entries.append({'name': name, 'answer': answer, 'date': date})

            # Sort the entries by date (or name if desired)
            sorted_entries = sorted(entries, key=lambda x: x['date'])
            return sorted_entries
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read or parse XML: {e}")
            return []

    # Function to create the GUI and display sorted XML data
    def create_gui(sorted_entries):
        sorted_window = ctk.CTkToplevel()  # A new window
        sorted_window.title("Sorted XML Viewer")
        sorted_window.geometry("1750x700")
        # Set the window to full-screen
        sorted_window.attributes('-fullscreen', False)

        # Create a Canvas widget for the scrollable area
        canvas = ctk.CTkCanvas(sorted_window)
        canvas.pack(side="left", fill="both", expand=True)

        # Create a Scrollbar widget for the canvas
        scrollbar = ctk.CTkScrollbar(sorted_window, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Link the canvas to the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a Frame inside the canvas to hold the text content
        content_frame = ctk.CTkFrame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        # Update the canvas scrollregion whenever the content frame is resized
        def update_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        content_frame.bind("<Configure>", update_scrollregion)

        # Function to toggle the style of the name when checkbox is clicked
        def toggle_name_style(name_label, name_strike, name_text):
            if name_strike.get():  # If the checkbox is checked
                # Apply grey and simulate strikethrough by creating a line through the label
                name_label.configure(text=name_text, text_color='grey', font=('Arial', 10, 'italic'))
                # Create a line to simulate the strikethrough effect
                strike_through_line = ctk.CTkCanvas(name_label, height=2, width=name_label.winfo_width())
                strike_through_line.create_line(0, 1, name_label.winfo_width(), 1, fill="grey", width=2)
                strike_through_line.place(x=0, y=name_label.winfo_height() // 2)
            else:
                name_label.configure(text=name_text, text_color='black', font=('Arial', 10))  # Default style

        # Dynamically add each entry from the sorted XML
        for entry in sorted_entries:
            # Create a Frame for each entry to display Name, Answer, Date
            entry_frame = ctk.CTkFrame(content_frame)
            entry_frame.pack(fill="x", pady=5, padx=10)

            # Variable to store the checkbox state
            name_strike = ctk.BooleanVar()

            # Create labels inside the entry frame
            name_label = ctk.CTkLabel(entry_frame, text=f"Name: {entry['name']}", anchor="w", width=200)
            name_label.pack(side="left", padx=10)

            # Create the checkbox and attach the toggle function to change the style of the name
            name_checkbox = ctk.CTkCheckBox(entry_frame, variable=name_strike, text="Strike-through", command=lambda name_label=name_label, name_strike=name_strike, name_text=entry['name']: toggle_name_style(name_label, name_strike, name_text))
            name_checkbox.pack(side="left", padx=10)

            answer_label = ctk.CTkLabel(entry_frame, text=f"Answer: {entry['answer']}", anchor="w", width=500)
            answer_label.pack(side="left", padx=10)

            date_label = ctk.CTkLabel(entry_frame, text=f"Date: {entry['date']}", anchor="w")
            date_label.pack(side="right", padx=10)

            # Calculate word count for the answer text
            word_count = len(entry['answer'].split())

            # Create a label for the word count and pack it to the right of the "Date"
            word_count_label = ctk.CTkLabel(entry_frame, text=f"Words: {word_count}", anchor="w")
            word_count_label.pack(side="right", padx=10)

        # Function to close the window when the button is clicked
        def close_window():
            sorted_window.quit()  # This will close the window when the button is clicked

        # Create a button to close the window and place it at the bottom
        close_button = ctk.CTkButton(sorted_window, text="Close", command=close_window)
        close_button.pack(side="bottom", pady=20)

    # Main function to run the program
    def main():
        file_path = "output.xml"  # Path to the XML file
        sorted_entries = read_and_sort_xml(file_path)
        if sorted_entries:
            create_gui(sorted_entries)

    # Create a separate thread to handle the GUI window
    def run_in_thread():
        main()

    # Run the main function in a separate thread
    threading.Thread(target=run_in_thread).start()

# Run the code function
code()
