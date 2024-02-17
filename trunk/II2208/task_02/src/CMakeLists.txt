cmake_minimum_required(VERSION 3.10)

project(contacts)

# Find PyQt6 library
find_package(Qt6 REQUIRED COMPONENTS Widgets Gui)

# Find Python libraries
find_package(PythonLibs REQUIRED)

# Add Python include path
include_directories(${PYTHON_INCLUDE_DIRS})

# Add source files
add_executable(contacts main.py contacts.py)

# Link libraries
target_link_libraries(contacts Qt6::Widgets Qt6::Gui ${PYTHON_LIBRARIES})

