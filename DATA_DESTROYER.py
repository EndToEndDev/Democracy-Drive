import os
import customtkinter as ctk
import tkinter.messagebox as messagebox

def file():
    # Function to delete the output.xml file after confirmation
    def destroy_file():
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete 'output.xml'? This action cannot be undone.")
    
        if confirm:  # If the user clicks 'Yes'
            try:
                # Check if the file exists
                if os.path.exists("output.xml"):
                    os.remove("output.xml")  # Delete the file
                    messagebox.showinfo("Success", "The file 'output.xml' has been destroyed.")
                else:
                    messagebox.showwarning("File Not Found", "The file 'output.xml' does not exist.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while deleting the file: {e}")
        else:
            # User clicked 'No', so we cancel the deletion
            messagebox.showinfo("Cancelled", "File deletion cancelled.")

    # Creating the GUI using Toplevel window (avoid mainloop conflict)
    destroy_window = ctk.CTkToplevel()  # A new window, separate from the main root window
    destroy_window.geometry("250x250")
    destroy_window.title("Destroy File")

    # Add a button that destroys the output.xml file when clicked
    destroy_button = ctk.CTkButton(destroy_window, text="Destroy", command=destroy_file)
    destroy_button.pack(pady=50)

    # Don't call `mainloop()` here; it's already running in the main program loop.
    # The `Toplevel()` window will behave like a normal window in the existing event loop.

# You should **not** call `file()` automatically in your script. Instead, call it when needed:
# file()  # This should not be called here unless it's specifically needed.