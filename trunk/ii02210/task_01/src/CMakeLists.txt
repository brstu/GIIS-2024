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

# Поиск компилятора C#
find_program(CSHARP_COMPILER csc)

if(NOT CSHARP_COMPILER)
    message(FATAL_ERROR "C# compiler not found. Please make sure you have Mono or .NET SDK installed.")
endif()

# Создание исполняемого файла
add_executable(MyCSharpExecutable ${SOURCES})

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
