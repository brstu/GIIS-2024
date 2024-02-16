cmake_minimum_required (VERSION 3.15)
project (GIIS) 



# Найдем пакет Python
find_package(Python3 COMPONENTS Interpreter Development)
if(NOT Python3_FOUND)
    message(FATAL_ERROR "Python 3 not found")
endif()

# Найдем пакет NumPy
find_package(NumPy REQUIRED)
if(NOT NumPy_FOUND)
    message(FATAL_ERROR "NumPy not found")
endif()

# Найдем пакет OpenCV
find_package(OpenCV REQUIRED)
if(NOT OpenCV_FOUND)
    message(FATAL_ERROR "OpenCV not found")
endif()

# Добавим ваш Python-скрипт в качестве исполняемого файла
add_executable(my_python_script main.py)

# Свяжем библиотеки Python, NumPy и OpenCV с вашим исполняемым файлом
target_link_libraries(my_python_script Python3::Python ${NumPy_LIBRARIES} ${OpenCV_LIBS})

