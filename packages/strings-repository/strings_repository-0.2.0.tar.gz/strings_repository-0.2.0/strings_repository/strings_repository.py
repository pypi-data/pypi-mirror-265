import os
import requests
import yaml
import zipfile
import tempfile

__app_name__ = "strings_repository"
__version__ = "0.1.0"

CONFIG_FILE = 'strings_repository.yaml'

HOST_KEY = "host"
API_KEY = "api_key"
API_KEY_ENV_VAR = "env_variable"
TYPE_KEY = "type"
LANGUAGES_KEY = "languages"
TAGS_KEY = "tags"
PATH_KEY = "path"

REPO_KEY = "STRINGS_REPOSITORY_KEY"


class App:

    @classmethod
    def init_config(cls, host, token, env_var, type, languages, tags, path):
        working_dir = os.getcwd()
        config_path = os.path.join(working_dir, CONFIG_FILE)

        configuration = {
            HOST_KEY: host,
            TYPE_KEY: type,
            LANGUAGES_KEY: languages.split(','),
            TAGS_KEY: tags.split(','),
            PATH_KEY: path
        }

        if env_var:
            configuration[API_KEY_ENV_VAR] = env_var

        if token:
            configuration[API_KEY] = token

        with open(config_path, 'w') as file:
            yaml.dump(configuration, file)

    @classmethod
    def pull(cls):
        working_dir = os.getcwd()
        config_path = os.path.join(working_dir, CONFIG_FILE)
        with open(config_path, 'r') as file:
            config_data = yaml.safe_load(file)

        env_var = config_data.get(API_KEY_ENV_VAR)
        if env_var:
            api_key = os.environ[env_var]
        else:
            api_key = config_data[API_KEY]

        data = {
            'type': config_data[TYPE_KEY],
        }

        tags = config_data.get(TAGS_KEY)
        if tags:
            data['tags'] = tags

        langs = config_data.get(LANGUAGES_KEY)
        if langs:
            data['codes'] = langs

        print('Fetching data...')

        url = config_data[HOST_KEY] + '/api/plugin/export'
        response = requests.post(
            url=url,
            data=data,
            headers={
                'Access-Token': api_key
            },
        )

        print('Unpacking...')

        with tempfile.NamedTemporaryFile(delete=True) as tmp:
            tmp.write(response.content)
            tmp.seek(0)

            config_path = config_data[PATH_KEY]
            working_dir = os.getcwd()
            path = os.path.join(working_dir, config_path)

            unzip = zipfile.ZipFile(tmp)
            unzip.extractall(path)
            print('Completed...')


if __name__ == "__main__":
    App.pull()
