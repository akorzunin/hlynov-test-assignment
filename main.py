
from src.app import App

app = App()

if __name__ == '__main__':
    app.parse_file(
        file_path = input('Enter path to xml file: \n')
    )