import os

if __name__ == '__main__':
    # Путь к текущему файлу
    current_file_path = os.path.abspath(__file__)

    # Путь к папке scripts
    scripts_folder = os.path.dirname(current_file_path)

    # Путь к папке data (одного уровня со scripts)
    data_folder = os.path.join(os.path.dirname(scripts_folder), 'data')

    from config.settings import INSTALLED_APPS

    installed_apps = INSTALLED_APPS[-2:]

    for app in installed_apps:
        json_file_name = f'{app}_data.json'
        print(f'{json_file_name = }')

        app_name = f'{app}'
        print(f'{app_name = }')

        # Полный путь к json файлу в папке data
        json_file_path = os.path.join(data_folder, json_file_name)

        try:
            os.system(f'python3 ../manage.py dumpdata {app_name} > {json_file_path}')
            print(f'{app.upper()} dumped to {json_file_path}')
        except OSError as e:
            print(f'{OSError = }')
