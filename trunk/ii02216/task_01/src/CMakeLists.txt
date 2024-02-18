cmake_minimum_required(VERSION 3.10)
project(ImageProcessing)

# Добавляем компиляцию для языка Python
enable_language(CXX)

# Находим необходимый пакет
find_package(Boost REQUIRED python)
find_package(PythonInterp REQUIRED)
find_package(PythonLibs REQUIRED)

# Указываем пути для заголовочных файлов Python
include_directories(${PYTHON_INCLUDE_DIRS})

# Устанавливаем пути для файлов библиотек Python
link_directories(${PYTHON_LIBRARIES})

# Добавляем исполняемый файл
add_executable(ImageProcessing main.cpp)

# Линкуем библиотеки
target_link_libraries(ImageProcessing ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})
