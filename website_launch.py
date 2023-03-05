# Helper functions and global constants
from website import create_app

app = create_app()
if __name__ == '__main__':
    app.run(debug = True)
    #app.run(debug = True, host='82.211.205.140', port=8080)