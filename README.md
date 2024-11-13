Overview:
The code is for a simple server that hosts an HTML form where users can submit answers to a given question. The server runs locally on the machine and can be controlled through a GUI (Graphical User Interface). The GUI allows for controlling the server's start and stop actions, as well as setting the duration for which the server should run.


Imports:
random: Used for generating a random port number between 8000 and 8080 to avoid port conflicts.
customtkinter as ctk: CustomTkinter is a library used to create a modern, customizable GUI with Tkinter.
messagebox: Provides a way to show message boxes in Tkinter (used for warnings and errors).
http.server: A built-in Python library to create an HTTP server. HTTPServer is used to run the server, and BaseHTTPRequestHandler is used to handle HTTP requests.
threading: Used to run certain tasks (like starting the server or the timer) in separate threads, allowing concurrent execution without blocking the main GUI.
time: Used for pausing execution (e.g., in the countdown timer).


Functions Breakdown:
1. generate_random_port():
This function returns a random port number between 8000 and 8080. It ensures that the server doesn't run on a fixed port but on a dynamically chosen one within this range.

def generate_random_port():

    return random.randint(8000, 8080)
2. start_server():
This is the main function that starts the server. It performs the following tasks:

HTML Template: It generates an HTML page that will be served by the HTTP server. The page includes:

A form to accept user responses.
A timer that shows how much time is left before the server shuts down.
An option to display the entered response and disable the submit button after the server shuts down.

Server Setup: The HTTPServer is initialized with the BaseHTTPRequestHandler class, which defines how the server should respond to incoming GET and POST requests. It responds by serving the generated HTML page.

Timer Thread: A separate thread (countdown_thread) is created to handle the countdown timer for the server's duration. This thread updates the timer on the GUI.

Server Loop: The server enters a loop where it listens for incoming HTTP requests. It will continue handling requests until the stop_event is set (i.e., the server should stop). If the timer reaches zero, it triggers a shutdown of the server.

Graceful Shutdown: Once the server stops (either due to the countdown or user action), the submit button and the response textbox are disabled, and the server is gracefully closed.

def start_server(question, port, host="192.168.1.80", stop_event=None, status_label=None, shutdown_event=None, timer_duration=0, ip_port_label=None, submit_button=None, user_response_textbox=None):

    # Generate HTML content dynamically, based on the question, timer, and other parameters.

    # Define the HTTP request handler that serves the HTML content.

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

    

    # Create and run the HTTP server.

    server = HTTPServer((host, port), normUserHTTP)

    print(f"Server running at {host}:{port}")

    # Update the status label to show the server is running

    if status_label:

        status_label.configure(text=f"Server running at {host}:{port}")

    # Start the countdown timer thread

    countdown_thread = threading.Thread(target=update_timer, args=(timer_duration, status_label, shutdown_event, ip_port_label))

    countdown_thread.daemon = True

    countdown_thread.start()

    while not stop_event.is_set():

        try:

            server.handle_request()  # Handle a single HTTP request

        except Exception as e:

            print(f"Error occurred: {e}")

            break

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
3. update_timer():
This function runs in its own thread to handle the countdown timer. It decreases the time by 1 second every second and updates the GUI with the remaining time. If the timer runs out, it triggers the shutdown event (shutdown_event.set()), which signals the server to stop.

def update_timer(timer_duration, status_label, shutdown_event, ip_port_label):

    while timer_duration > 0 and not shutdown_event.is_set():

        time.sleep(1)

        timer_duration -= 1

        status_label.configure(text=f"Time remaining: {timer_duration} seconds")

    

    if timer_duration <= 0:

        shutdown_event.set()  # Trigger shutdown when timer expires

        status_label.configure(text="Server shutting down automatically...")
4. start_gui():
This function creates the GUI using CustomTkinter. It includes several GUI components:

Question Input: A text entry for the question to be asked.
Host Input: An optional input for the server's host address.
Timer Input: A field to set the duration for the server to run.
Start/Stop Buttons: To control the server's lifecycle.
Status Labels: To display the current status of the server, like "Server running at 192.168.1.80:8000" or "Server stopped."

This function handles the user interaction, including starting and stopping the server. The on_start_button_click() and on_stop_button_click() methods are called when the corresponding buttons are clicked.

def start_gui():

    stop_event = threading.Event()

    shutdown_event = threading.Event()

    root = ctk.CTk()

    root.title("Democracy Drive Bellwork Server")

    ctk.set_appearance_mode("dark")

    root.geometry("400x475")

    root.resizable(False, False)

    # Labels and Entries for the question, host, and timer

    question_label = ctk.CTkLabel(root, text="Enter today's question:")

    question_label.pack(pady=10)

    question_entry = ctk.CTkEntry(root, width=300)

    question_entry.pack(pady=5)

    host_label = ctk.CTkLabel(root, text="Enter host (optional, default: 192.168.1.80):")

    host_label.pack(pady=10)

    host_entry = ctk.CTkEntry(root, width=300)

    host_entry.pack(pady=5)

    timer_label = ctk.CTkLabel(root, text="Enter timer duration (seconds):")

    timer_label.pack(pady=10)

    timer_entry = ctk.CTkEntry(root, width=300)

    timer_entry.pack(pady=5)

    # Start Button to start the server

    start_button = ctk.CTkButton(root, text="Start Server", command=lambda: on_start_button_click(question_entry, host_entry, timer_entry, start_button, stop_button, status_label, stop_event, shutdown_event, submit_button, user_response_textbox))

    start_button.pack(pady=20)

    # Stop Button to stop the server

    stop_button = ctk.CTkButton(root, text="Stop Server", command=lambda: on_stop_button_click(stop_event, start_button, stop_button, status_label), state=ctk.DISABLED)

    stop_button.pack(pady=10)

    # Status and IP/Port Labels

    status_label = ctk.CTkLabel(root, text="Server status: Not running", anchor="w", wraplength=350)

    status_label.pack(pady=10, padx=20, fill="x", anchor="w")

    ip_port_label = ctk.CTkLabel(root, text="IP:Port: Not set yet", anchor="w", wraplength=350)

    ip_port_label.pack(pady=5, padx=20, fill="x", anchor="w")

    # Response Textbox and Submit Button

    user_response_textbox = ctk.CTkEntry(root, width=300, placeholder_text="Enter your answer here")

    user_response_textbox.pack(pady=5)

    submit_button = ctk.CTkButton(root, text="Submit", state=ctk.DISABLED)

    submit_button.pack(pady=10)
5. Button Handlers (on_start_button_click() and on_stop_button_click()):
These functions manage the actions of the Start and Stop buttons:

Start Button: When clicked, it starts the server in a new thread.
Stop Button: When clicked, it stops the server

.


Execution:
When the script is run, the start_gui() function is invoked to create and display the GUI. From the GUI, the user can:

Enter a question and timer duration.
Start the server with a randomly generated port.
View the status and IP/Port information.
Submit responses before the server shuts down automatically.

This is all controlled via the GUI with server actions running in the background using threading.


Conclusion:
This code creates an interactive web server that serves an HTML form to collect responses to a given question. The server is controlled via a GUI that allows the user to start/stop the server, set a timer for how long it should run, and submit responses before the timer expires.

"guy who made this" notes Made by “EndToEndDev” 
Total Updates (so far) : 206
Last Update Time : 8:39 P.m. 11/12/2024
