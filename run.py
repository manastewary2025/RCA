from app import create_app, socketio

# Create an instance of the application
app = create_app()

if __name__ == '__main__':
    # Run the Flask application with Socket.IO support
    socketio.run(app, debug=True)
