cmake_minimum_required(VERSION 3.15)

project(giis_1LAB)

# Настройка языка C#
enable_language(CSharp)

# Указание исходных файлов C#
set(SOURCES
    Program.cs
    Form1.cs
    Form1.Designer.cs
    Form1.resx
)

# Создание исполняемого файла
add_executable(MyCSharpExecutable ${SOURCES})
