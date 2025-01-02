import tkinter as tk
import threading
import time
from twitterBot import run_bot  # Import the `run_bot` function from your backend file

# Global variable to control the bot loop
bot_running = False

# Function to start the bot
def start_bot():
    global bot_running
    if bot_running:
        print("Bot is already running!")
        return

    bot_running = True
    print("Starting the bot...")

    # Run the bot in a separate thread to avoid blocking the GUI
    bot_thread = threading.Thread(target=run_bot_wrapper)
    bot_thread.daemon = True  # Ensure the thread stops when the main program exits
    bot_thread.start()

# Wrapper function to safely run the bot
def run_bot_wrapper():
    global bot_running
    while bot_running:
        try:
            run_bot()
        except Exception as e:
            print(f"Error in bot loop: {e}")
            time.sleep(120)

# Function to stop the bot
def stop_bot():
    global bot_running
    if not bot_running:
        print("Bot is not running!")
        return

    print("Stopping the bot...")
    bot_running = False

# Function to create the Tkinter GUI
def create_gui():
    # Initialize the main window
    window = tk.Tk()
    window.title("AI Twitter Bot Control")
    window.geometry("300x150")  # Set the window size

    # Create Start button
    start_button = tk.Button(window, text="Start", font=("Arial", 14), bg="green", fg="white", command=start_bot)
    start_button.pack(pady=20)  # Add padding around the button

    # Create Stop button
    stop_button = tk.Button(window, text="Stop", font=("Arial", 14), bg="red", fg="white", command=stop_bot)
    stop_button.pack(pady=10)

    # Run the GUI event loop
    window.mainloop()

# Start the GUI
if __name__ == "__main__":
    create_gui()
import tkinter as tk
import threading
import time
from telegramBot import run_bot  # Import the `run_bot` function from your backend file

# Global variable to control the bot loop
bot_running = False

# Function to start the bot
def start_bot():
    global bot_running
    if bot_running:
        print("Bot is already running!")
        return

    bot_running = True
    print("Starting the bot...")

    # Run the bot in a separate thread to avoid blocking the GUI
    bot_thread = threading.Thread(target=run_bot_wrapper)
    bot_thread.daemon = True  # Ensure the thread stops when the main program exits
    bot_thread.start()

# Wrapper function to safely run the bot
def run_bot_wrapper():
    global bot_running
    while bot_running:
        try:
            run_bot()
        except Exception as e:
            print(f"Error in bot loop: {e}")
            time.sleep(120)

# Function to stop the bot
def stop_bot():
    global bot_running
    if not bot_running:
        print("Bot is not running!")
        return

    print("Stopping the bot...")
    bot_running = False

# Function to create the Tkinter GUI
def create_gui():
    # Initialize the main window
    window = tk.Tk()
    window.title("AI Twitter Bot Control")
    window.geometry("300x150")  # Set the window size

    # Create Start button
    start_button = tk.Button(window, text="Start", font=("Arial", 14), bg="green", fg="white", command=start_bot)
    start_button.pack(pady=20)  # Add padding around the button

    # Create Stop button
    stop_button = tk.Button(window, text="Stop", font=("Arial", 14), bg="red", fg="white", command=stop_bot)
    stop_button.pack(pady=10)

    # Run the GUI event loop
    window.mainloop()

# Start the GUI
if __name__ == "__main__":
    create_gui()
