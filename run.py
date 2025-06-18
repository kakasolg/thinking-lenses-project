from app import create_app

# Create the Flask app instance using the application factory
app = create_app()

if __name__ == '__main__':
    # Run the Flask development server
    # Debug mode should be true for development, allowing auto-reload and debugger.
    # Host '0.0.0.0' makes the server accessible externally (e.g., within a local network).
    # Port 5000 is a common port for Flask development.
    app.run(debug=True, host='0.0.0.0', port=5000)
