import sys
import os
import webbrowser
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

def start_http_server(directory=".", port=8000):
    """Starts an HTTP server in the specified directory on the given port, accessible over LAN."""
    if not os.path.isdir(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        sys.exit(1)

    os.chdir(directory)

    # Bind to all interfaces (LAN access)
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

    # Get local IP for LAN access
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    # Open browser to localhost, and also print LAN IP
    threading.Timer(1, lambda: webbrowser.open(f"http://localhost:{port}/")).start()

    print(f"\nServing '{directory}' at:")
    print(f"  → Localhost: http://localhost:{port}/")
    print(f"  → LAN:       http://{local_ip}:{port}/")
    print("Press Ctrl+C to stop the server.\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
        httpd.server_close()

if __name__ == "__main__":
    directory = input("Enter the directory to serve (start at C: or your drive name): ").strip() or "."
    
    try:
        port = int(input("Enter port number (default is 8000): ").strip() or 8000)
    except ValueError:
        print("Invalid port number. Using default port 8000.")
        port = 8000

    start_http_server(directory, port)