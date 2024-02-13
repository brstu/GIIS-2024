cmake_minimum_required(VERSION 3.15)
project(MyCSharpProject)

# Проверка наличия компилятора C#
find_program(CSHARP_COMPILER csc)

if(NOT CSHARP_COMPILER)
    message(FATAL_ERROR "C# compiler not found. C# is only supported with Microsoft Visual Studio 12 2013 and later.")
endif()

# Настройка языка C#
enable_language(CSharp)

# Указание исходных файлов C#
set(CSHARP_SOURCE
    Program.cs
    Form1.cs
    Form1.Designer.cs
    Form1.resx
)

# Создание исполняемого файла
add_executable(MyCSharpExecutable ${CSHARP_SOURCE})

# Добавление зависимости на .NET
set_property(TARGET MyCSharpExecutable PROPERTY VS_DOTNET_REFERENCES
    "Microsoft.CSharp"
    "System"
    "System.Core"
    "System.Data"
    "System.Data.DataSetExtensions"
    "System.Net.Http"
    "System.Xml"
    "System.Xml.Linq"
    "WindowsBase"
    "System.Windows.Forms"
)

# Добавление внешнего проекта для сборки C# проекта
include(ExternalProject)

ExternalProject_Add(MyCSharpProject
    SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}
    CONFIGURE_COMMAND ""
    BUILD_COMMAND ""
    INSTALL_COMMAND ""
    BUILD_BYPRODUCTS ${CMAKE_CURRENT_BINARY_DIR}/MyCSharpExecutable.exe
)

# Добавление зависимости от внешнего проекта
add_dependencies(MyCSharpExecutable MyCSharpProject)
