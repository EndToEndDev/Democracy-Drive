import random
import customtkinter as ctk
from tkinter import messagebox
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time
import xml.etree.ElementTree as ET
import datetime

# Function to generate random port number
def generate_random_port():
    return random.randint(8000, 8080)

today = datetime.date.today()
formated_today = today.strftime("%d")

# Function to start the server
def start_server(question, port, host="192.168.1.80", stop_event=None, status_label=None, shutdown_event=None, timer_duration=0, ip_port_label=None, submit_button=None, user_response_textbox=None):
    try:
        test_data = {
            "name": "Test",
            "answer": "Test Answer",
            "day of": f"{formated_today}"
        }
        root = ET.Element("output")

        for key, value in test_data.items():
            element = ET.SubElement(root, key)
            element.text = str(value)
        tree = ET.ElementTree(root)

        tree.write("output.xml")
        # Define the HTML content that will be returned by the server
        html_code = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Democracy Drive</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    color: #333;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    flex-direction: column;
                }

                h1 {
                    color: #333;
                }

                form {
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    width: 100%;
                    max-width: 400px;
                    text-align: center;
                }

                label {
                    font-size: 16px;
                    margin-bottom: 8px;
                    display: block;
                    color: #555;
                }

                textarea {
                    width: 100%;
                    min-height: 50px;
                    padding: 10px;
                    font-size: 16px;
                    margin-bottom: 20px;
                    border: 2px solid #ccc;
                    border-radius: 4px;
                    transition: border-color 0.3s ease, height 0.2s ease;
                    resize: none;
                    overflow-y: auto;
                }

                textarea:focus {
                    border-color: #007bff;
                    outline: none;
                }

                button {
                    background-color: #007bff;
                    color: #fff;
                    border: none;
                    padding: 10px 20px;
                    font-size: 16px;
                    border-radius: 4px;
                    cursor: pointer;
                    transition: background-color 0.3s ease;
                }

                button:hover {
                    background-color: #0056b3;
                }

                h2 {
                    color: #333;
                    margin-top: 30px;
                }

                #storedValue {
                    font-size: 18px;
                    color: #555;
                    background-color: #e9ecef;
                    padding: 10px;
                    border-radius: 4px;
                    width: 100%;
                    max-width: 400px;
                    margin-top: 10px;
                    text-align: center;
                }

                #timer {
                    font-size: 18px;
                    color: #f44336;
                    margin-top: 30px;
                    font-weight: bold;
                }

                #ipPort {
                    font-size: 16px;
                    color: #007bff;
                    margin-top: 10px;
                    font-weight: normal;
                }
            </style>
            <script>
                function storeInput() {
                    let userInput = document.getElementById("userResponse").value;
                    document.getElementById("storedValue").textContent = "You entered: " + userInput;
                    document.getElementById("userResponse").value = "";
                    return false;
                }

                function autoResize() {
                    const textarea = document.getElementById('userResponse');
                    textarea.style.height = 'auto';
                    textarea.style.height = (textarea.scrollHeight) + 'px';
                }

                function updateTimer(remainingTime) {
                    document.getElementById("timer").textContent = "Time remaining: " + remainingTime + " seconds";
                }
            </script>
        '''
        html_code_2 = f'''
        </head>
        <body>
            <h1>Ask a Question</h1>
            <h2>{question}</h2>
            <form onsubmit="return storeInput()">
                <label for="userResponse">Enter your response:</label>
                <textarea id="userResponse" placeholder="Type your answer here" required oninput="autoResize()"></textarea>
                <button type="submit" id="submitButton" { 'disabled' if shutdown_event.is_set() else '' }>Submit</button>
            </form>
            
            <h2>Stored Response:</h2>
            <p id="storedValue">No response yet.</p>

            <p id="timer">Time remaining: {timer_duration} seconds</p>
            <p id="ipPort">Server running at {host}:{port}</p>
        </body>
        </html>
        '''

        overall_html_code = html_code + html_code_2

        class normUserHTTP(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(overall_html_code, "utf-8"))
                
            def do_POST(self):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(overall_html_code, "utf-8"))

        # Create and start the HTTP server
        server = HTTPServer((host, port), normUserHTTP)
        print(f"Server running at {host}:{port}")
        
        # Update the status label to show the server is running
        if status_label:
            status_label.configure(text=f"Server running at {host}:{port}")

        # Start the countdown timer thread
        countdown_thread = threading.Thread(target=update_timer, args=(timer_duration, status_label, shutdown_event, ip_port_label))
        countdown_thread.daemon = True
        countdown_thread.start()

        # Loop to serve requests until stop event is set
        while not stop_event.is_set():
            try:
                server.handle_request()  # Handle a single HTTP request
            except Exception as e:
                print(f"Error occurred: {e}")
                break
            # Check for shutdown event to stop the server
            if shutdown_event.is_set():
                break

        # Gracefully stop the server
        print("Stopping server...")
        if status_label:
            status_label.configure(text="Server stopped.")
        server.server_close()

        # Disable submit button and response textbox on shutdown
        if submit_button:
            submit_button.configure(state=ctk.DISABLED)
        if user_response_textbox:
            user_response_textbox.configure(state='disabled')

    except Exception as e:
        print(f"Error occurred while starting the server: {e}")
        messagebox.showerror("Server Error", f"An error occurred while starting the server: {e}")

# Function to update the timer
def update_timer(timer_duration, status_label, shutdown_event, ip_port_label):
    while timer_duration > 0 and not shutdown_event.is_set():
        time.sleep(1)
        timer_duration -= 1
        # Update the GUI timer label
        status_label.configure(text=f"Time remaining: {timer_duration} seconds")
    
    if timer_duration <= 0:
        shutdown_event.set()  # Trigger shutdown when timer expires
        status_label.configure(text="Server shutting down automatically...")

# Function to handle the GUI interaction
def start_gui():
    stop_event = threading.Event()  # Create an event to stop the server thread
    shutdown_event = threading.Event()  # Event for shutdown timer

    # Create the main window using customtkinter with dark mode enabled
    root = ctk.CTk()
    root.title("Democracy Drive Bellwork Server")

    # Enable dark mode for the customtkinter window
    ctk.set_appearance_mode("dark")

    # Set window size and layout
    root.geometry("400x475")
    root.resizable(False, False)

    # Create a label and entry for the question
    question_label = ctk.CTkLabel(root, text="Enter today's question:")
    question_label.pack(pady=10)
    question_entry = ctk.CTkEntry(root, width=300)
    question_entry.pack(pady=5)

    # Create a label and entry for the host
    host_label = ctk.CTkLabel(root, text="Enter host (optional, default: 192.168.1.80):")
    host_label.pack(pady=10)
    host_entry = ctk.CTkEntry(root, width=300)
    host_entry.pack(pady=5)

    # Create a label and entry for the timer
    timer_label = ctk.CTkLabel(root, text="Enter timer duration (seconds):")
    timer_label.pack(pady=10)
    timer_entry = ctk.CTkEntry(root, width=300)
    timer_entry.pack(pady=5)

    # Create a button to start the server
    start_button = ctk.CTkButton(root, text="Start Server", command=lambda: on_start_button_click(question_entry, host_entry, timer_entry, start_button, stop_button, status_label, stop_event, shutdown_event, submit_button, user_response_textbox))
    start_button.pack(pady=20)

    # Create a button to stop the server
    stop_button = ctk.CTkButton(root, text="Stop Server", command=lambda: on_stop_button_click(stop_event, start_button, stop_button, status_label), state=ctk.DISABLED)
    stop_button.pack(pady=10)

    # Label to display server status
    status_label = ctk.CTkLabel(root, text="Server status: Not running", anchor="w", wraplength=350)
    status_label.pack(pady=10, padx=20, fill="x", anchor="w")

    # Label to display IP/Port information
    ip_port_label = ctk.CTkLabel(root, text="IP:Port: Not set yet", anchor="w", wraplength=350)
    ip_port_label.pack(pady=5, padx=20, fill="x", anchor="w")

    # Create a response textbox and submit button
    user_response_textbox = ctk.CTkEntry(root, width=300, placeholder_text="Enter your answer here")
    user_response_textbox.pack(pady=5)
    submit_button = ctk.CTkButton(root, text="Submit", state=ctk.DISABLED)
    submit_button.pack(pady=10)

    # Function to handle the start button click
    def on_start_button_click(question_entry, host_entry, timer_entry, start_button, stop_button, status_label, stop_event, shutdown_event, submit_button, user_response_textbox):
        question = question_entry.get()
        if not question:
            messagebox.showwarning("Input Error", "Please enter a question before starting the server.")
            return

        port = generate_random_port()
        host = host_entry.get() or "192.168.1.80"
        timer_duration = int(timer_entry.get()) if timer_entry.get().isdigit() else 0

        # Start the server in a new thread
        server_thread = threading.Thread(target=start_server, args=(question, port, host, stop_event, status_label, shutdown_event, timer_duration, ip_port_label, submit_button, user_response_textbox))
        server_thread.daemon = True
        server_thread.start()

        # Update the GUI with IP and Port information
        ip_port_label.configure(text=f"Server running at {host}:{port}")

        # Disable the start button and enable the stop button once the server starts
        start_button.configure(state=ctk.DISABLED)
        stop_button.configure(state=ctk.NORMAL)

    # Function to handle the stop button click
    def on_stop_button_click(stop_event, start_button, stop_button, status_label):
        if stop_event.is_set():
            messagebox.showwarning("Server Error", "The server is already stopped or not started yet.")
            return
        stop_event.set()
        status_label.configure(text="Server stopped.")
        start_button.configure(state=ctk.NORMAL)
        stop_button.configure(state=ctk.DISABLED)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    start_gui()
#test changes