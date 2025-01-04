import subprocess
import threading

# Function to read output from the subprocess and print it
def read_output(process):
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output, end='')

# Start the Command Prompt session
process = subprocess.Popen('cmd', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Start a separate thread to handle reading the output
thread = threading.Thread(target=read_output, args=(process,))
thread.daemon = True  # Daemon thread will exit when the main program exits
thread.start()

# Print a welcome message
print("Welcome to the Python CMD terminal! Type 'exit' to quit.")

while True:
    # Get user input (command)
    user_input = input()

    # Check if user wants to exit
    if user_input.lower() == 'exit':
        print("Exiting the CMD terminal.")
        break

    # Send the user input to the CMD process
    process.stdin.write(user_input + '\n')
    process.stdin.flush()

# Close the process when done
process.stdin.close()
process.stdout.close()
process.stderr.close()
process.wait()
