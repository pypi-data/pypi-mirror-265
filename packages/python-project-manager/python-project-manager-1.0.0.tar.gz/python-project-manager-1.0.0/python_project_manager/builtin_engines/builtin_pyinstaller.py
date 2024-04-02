import os

from python_project_manager.config import Config


def init(_method, **kwargs) -> bool:
    os.system('ppm install pyinstaller==6.5.0 --dev')
    set_default_scripts()
    create_template_app()
    return False

def create_template_app() -> None:
    os.makedirs(Config.get('src_dir'), exist_ok=True)
    with open(f'{Config.get('src_dir')}/app.py', 'w') as f:
        f.write(
'''
import os
import sys

try: # PyInstaller creates a temp folder and stores path in _MEIPASS
    resource_dir = sys._MEIPASS
except AttributeError: # If not running as a PyInstaller created executable
    resource_dir = 'src/resources'

# Example: os.path.join(resource_dir, 'file.ext')

def app(): # This function is the entry point of the application.
    print("Hello World.")

if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        print(e)
    # This line is used to prevent the console from closing immediately after the program finishes execution.
    input("Press Enter to continue...")
''')
    
    os.makedirs(Config.get('src_dir') + '/resources', exist_ok=True)

def set_default_scripts() -> None:
    Config.set('scripts.build', f'pyinstaller %src_dir%/app.py' +
        f' --noconfirm --clean --onefile --name %project_name%_v%version%' +
        f' --add-data %src_dir%/resources:.')
    Config.set('scripts.start', f'python -m %src_dir%.app')
    Config.save()