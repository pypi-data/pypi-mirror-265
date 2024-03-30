import os
import toml
from python_project_manager import Config, sanitize_string_for_file, sanitize_string_for_module

SetuptoolsEngineConfig = {
    'username': '',
    'password': '',
    'wheel': ''
}

def init(_method, **_kwargs):
    edit_config()
    create_template_app()
    set_default_scripts()
    create_files()
    return False

def version(_method, **_kwargs):
    _method(**_kwargs)
    toml_file = load_toml()
    toml_file['project']['version'] = Config.get('version')
    save_toml(toml_file)
    return False

def edit_config():
    Config.set('src_dir', sanitize_string_for_file(Config.get('project_name')))
    SetuptoolsEngineConfig['username'] = '__token__'
    SetuptoolsEngineConfig['password'] = 'pypi-<api-key>'
    SetuptoolsEngineConfig['wheel'] = sanitize_string_for_file(Config.get('project_name'))
    Config.set('twine', SetuptoolsEngineConfig)
    Config.save()

def create_template_app():
    os.makedirs(Config.get('src_dir'), exist_ok=True)
    with open(f'{Config.get('src_dir')}/app.py', 'w') as f:
        f.write('import os\n\n')
        f.write('def app():\n')
        f.write('    print(os.getcwd())\n')
        f.write('    print("Hello World.")\n\n')
        f.write('if __name__ == "__main__":\n')
        f.write('    app()')

def set_default_scripts():
    default_scripts = {
        'start': f'py -m %src_dir%.app',
        'build': f'ppm-builtin-setuptools-build',
        'install': f'ppm-builtin-setuptools-install',
        'uninstall': f'ppm-builtin-setuptools-uninstall',
        'publish-major': f'ppm-builtin-setuptools-publish-major',
        'publish-minor': f'ppm-builtin-setuptools-publish-minor',
        'publish-patch': f'ppm-builtin-setuptools-publish-patch'
    }
    Config.set('scripts', default_scripts)
    Config.save()

# Setuptools Engine built-in cli commands
# Allows for shorthand commands to be used in the cli
_publish_command = 'del /S /Q %dist_dir%\\* && python -m build && twine upload -u %twine.username% -p %twine.password% -r pypi %dist_dir%/*'
def _build():
    os.system(Config.parse(f'ppm version inc -t && python -m build', Config._value_config))
def _install():
    os.system(Config.parse(f'pip install %dist_dir%/%twine.wheel%-%version%-py3-none-any.whl --force-reinstall', Config._value_config))
def _uninstall():
    os.system(Config.parse(f'pip uninstall %dist_dir%/%twine.wheel%-%version%-py3-none-any.whl', Config._value_config))
def _publish():
    os.system(Config.parse(f'del /S /Q %dist_dir%\\* && python -m build && twine upload -u %twine.username% -p %twine.password% -r pypi %dist_dir%/*', Config._value_config))
def _publish_patch():
    os.system(Config.parse(f'ppm version inc -p 1 && {_publish_command}', Config._value_config))
def _publish_minor():
    os.system(Config.parse(f'ppm version inc -m 1 && {_publish_command}', Config._value_config))
def _publish_major():
    os.system(Config.parse(f'ppm version inc -M 1 && {_publish_command}', Config._value_config))

def create_files():
    toml_config = {
        'build-system': {
            'requires': ['setuptools', 'wheel'],
            'build-backend': 'setuptools.build_meta'
        },

        'project': {
            'name': sanitize_string_for_module(Config.get('project_name')),
            'version': Config.get('version', '0.0.0'),
            'description': 'A Python package.',
            'authors': [],
            'readme': 'README.md',
            'keywords': [],
            'dynamic': ['dependencies', 'optional-dependencies']
        },
        
        'tool': {
            'setuptools': {
                'dynamic': {
                    'dependencies': {
                        'file': ['requirements.txt']
                    },
                    'optional-dependencies': {
                        'dev': {
                            'file': ['requirements-dev.txt']
                        }
                    }
                }
            }
        }
    }
    with open('pyproject.toml', 'w') as f:
        toml.dump(toml_config, f)
    with open('LICENSE.txt', 'w') as f:
        pass
    with open('README.md', 'w') as f:
        pass
    

def load_toml():
    with open('pyproject.toml', 'r') as f:
        return toml.load(f)
    
def save_toml(toml_config):
    with open('pyproject.toml', 'w') as f:
        toml.dump(toml_config, f)