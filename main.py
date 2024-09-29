import subprocess
import xml.etree.ElementTree as ET

def read_config(xml_file):
    '''
    Считывает конфигурационный файл XML и возвращаем параметры
    '''

    tree = ET.parse(xml_file)         #парсер
    root = tree.getroot()     #корневой элемент xml-файла

    graphviz_path = root.find("graphviz_path").text
    package_path = root.find("package_path").text
    output_image_path = root.find("output_image_path").text

    return graphviz_path, package_path, output_image_path

def get_package_dependencies(package_name):
    """
    получаем зависимости пакета, возвращаем зависимости в виде списка.
    """
    try:
        result = subprocess.run(
            ['apt-cache', 'depends', package_name],
            capture_output=True, text=True, check=True
        )
        output = result.stdout
        dependencies = []

        for line in output.splitlines():
            line = line.strip()
            if line.startswith("Depends:"):
                dep = line.split()[1]
                dependencies.append(dep)
            elif line.startswith("Recommends:"):
                dep = line.split()[1]
                dependencies.append(dep)
        return dependencies
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при получении зависимости для {package_name}: {e}")
        return []

def generate_graphviz(package_name, dependencies):
    """
    Генерируем граф зависимостей в формате Graphviz (DOT).
    """
    dot_output = f'digraph "{package_name}" {{\n'
    dot_output += f'    "{package_name}" [shape=box];\n'

    # Цикл по зависимостям
    for dep in dependencies:
        dot_output += f'    "{package_name}" -> "{dep}";\n'

    dot_output += "}\n"
    return dot_output


def save_graph_to_png(dot_file, output_image, graphviz_path):
    """
    Генерация PNG-изображения графа с помощью Graphviz.
    """
    try:
        subprocess.run(
            [graphviz_path, '-Tpng', dot_file, '-o', output_image],  # Использует команду dot для генерации PNG
            check=True
        )
        print(f"Граф успешно сохранён в {output_image}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании изображения: {e}")

def main():
    # Чтение конфигурационного файла
    config_file = 'config.xml'
    print("Чтение конфигурационного файла...")
    graphviz_path, package_name, output_image = read_config(config_file)
    print(f"Путь к Graphviz: {graphviz_path}")
    print(f"Имя пакета: {package_name}")
    print(f"Путь для сохранения изображения: {output_image}")

    # Получаем зависимости
    print("Получение зависимостей пакета...")
    dependencies = get_package_dependencies(package_name)
    print(f"Зависимости: {dependencies}")

    if dependencies:
        # Генерируем DOT-формат
        dot_graph = generate_graphviz(package_name, dependencies)
        print("Граф зависимостей сгенерирован.")

        # Сохраняем результат в файл .dot
        dot_filename = f"{package_name}_dependencies.dot"
        with open(dot_filename, 'w') as f:
            f.write(dot_graph)

        print(f"Граф сохранён в {dot_filename}")

        # Генерация PNG с помощью Graphviz
        print("Создание PNG изображения...")
        save_graph_to_png(dot_filename, output_image, graphviz_path)
    else:
        print(f"Не удалось получить зависимости для пакета {package_name}.")

if __name__ == "__main__":
    main()