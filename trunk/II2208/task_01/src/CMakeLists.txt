cmake_minimum_required(VERSION 3.10)

project(image_viewer)

# Find OpenCV library
find_package(OpenCV REQUIRED)

# Find Python libraries
find_package(PythonLibs REQUIRED)

# Add Python include path
include_directories(${PYTHON_INCLUDE_DIRS})

# Add source files
add_executable(image_viewer main.py image_viewer_app.py)

# Link libraries
target_link_libraries(image_viewer ${OpenCV_LIBS} ${PYTHON_LIBRARIES})
