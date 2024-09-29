# **Dependency Graph Visualizer**

**Dependency Graph Visualizer** — это инструмент для визуализации графов зависимостей пакетов Ubuntu. Он использует `apt-cache` для получения информации о зависимостях пакета и `Graphviz` для построения графа в формате PNG.

## **Установка и использование**

### **1. Использование с WSL (Windows Subsystem for Linux)**

* **Шаг 1**: Установите WSL и необходимые зависимости:
* **Шаг 3**: Создайте XML-конфигурацию config.xml:
* **Шаг 4**: Запустите скрипт:
* **Шаг 5**: Проверьте наличие файла output_image.png в папке.

**Использование на Google Colab**
* **Шаг 1**: Установите зависимости !apt-get install graphviz:
* **Шаг 2**: Загрузите конфигурацию config.xml:
  
<config>
    <graphviz_path>dot</graphviz_path>
    <package_path>requests</package_path> <!-- Укажите пакет, для которого нужно построить граф -->
    <output_image_path>output_image.png</output_image_path>
</config>

* **Шаг 5**: У вас должен будет скачать пнг файл со схемой зависимостей Python 3, apt-utils, Graphviz
