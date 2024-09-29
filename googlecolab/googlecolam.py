import subprocess
import xml.etree.ElementTree as ET
import pkg_resources

# Создаем файл config.xml
xml_content = """<config>
    <graphviz_path>dot</graphviz_path>
    <package_path>requests</package_path>
    <output_image_path>output_image.png</output_image_path>
</config>"""

with open('config.xml', 'w') as f:
    f.write(xml_content)

# Проверка создания файла
!cat config.xml

def read_config(xml_file):
    '''
    Считывает конфигурационный файл XML и возвращает параметры
    '''
    tree = ET.parse(xml_file)
    root = tree.getroot()

    graphviz_path = root.find("graphviz_path").text
    package_name = root.find("package_path").text
    output_image_path = root.find("output_image_path").text

    return graphviz_path, package_name, output_image_path

def get_package_dependencies(package_name):
    """
    Получаем зависимости пакета, возвращаем зависимости в виде списка.
    """
    dependencies = []
    try:
        dist = pkg_resources.get_distribution(package_name)
        for dep in dist.requires():
            dependencies.append(str(dep))
        return dependencies
    except pkg_resources.DistributionNotFound:
        print(f"Пакет '{package_name}' не найден.")
        return []

def generate_graphviz(package_name, dependencies):
    dot_output = f'digraph "{package_name}" {{\n'
    dot_output += f'    "{package_name}" [shape=box];\n'
    for dep in dependencies:
        dot_output += f'    "{package_name}" -> "{dep}";\n'
    dot_output += "}\n"
    return dot_output

def save_graph_to_png(dot_file, output_image, graphviz_path):
    try:
        subprocess.run(
            [graphviz_path, '-Tpng', dot_file, '-o', output_image],
            check=True
        )
        print(f"Граф успешно сохранён в {output_image}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании изображения: {e}")

def main():
    config_file = 'config.xml'
    graphviz_path, package_name, output_image = read_config(config_file)

    print("Чтение конфигурационного файла...")
    print(f"Путь к Graphviz: {graphviz_path}")
    print(f"Имя пакета: {package_name}")
    print(f"Путь для сохранения изображения: {output_image}")

    print("Получение зависимостей пакета...")
    dependencies = get_package_dependencies(package_name)

    if dependencies:
        dot_graph = generate_graphviz(package_name, dependencies)

        dot_filename = f"{package_name}_dependencies.dot"
        with open(dot_filename, 'w') as f:
            f.write(dot_graph)

        save_graph_to_png(dot_filename, output_image, graphviz_path)

        from google.colab import files
        files.download(output_image)
    else:
        print(f"Не удалось получить зависимости для пакета {package_name}.")

if __name__ == "__main__":
    main()