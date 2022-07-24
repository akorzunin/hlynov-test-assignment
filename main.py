import sys

from src.app import App

app = App()

if __name__ == '__main__':
    if len(sys.argv) == 3:
        # dot move file while testing and debugging
        app.move_file = bool(int(sys.argv[2]))
    else: app.move_file = True
    app.parse_file(
        file_path = sys.argv[1],
    )