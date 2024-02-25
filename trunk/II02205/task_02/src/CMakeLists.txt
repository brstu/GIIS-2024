cmake_minimum_required(VERSION 3.10)
project(GIIS)

# Найдем необходимые пакеты
find_package(Qt6 COMPONENTS Widgets REQUIRED)
find_package(Python3 COMPONENTS Development Interpreter REQUIRED)

if (NOT Qt6_FOUND)
    message(FATAL_ERROR "Qt6 не найден. Убедитесь, что он установлен и правильно указан путь.")
endif()

if (NOT Python3_FOUND)
    message(FATAL_ERROR "Python3 не найден. Убедитесь, что он установлен и правильно указан путь.")
endif()

# Настройка вашего проекта
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_INCLUDE_CURRENT_DIR ON)

# Добавление исполняемого файла main.py
add_executable(MyAddressBook main.py adress_book.py window.py)

# Связывание необходимых библиотек
target_link_libraries(MyAddressBook PRIVATE Qt6::Widgets Python3::Python)
