cmake_minimum_required(VERSION 3.16)

project(Tetris CSharp)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_STANDARD 17)

set(SOURCE_FILES
    App.xaml.cs
    AssemblyInfo.cs
    Block.cs
    BlockQueue.cs
    GameGrid.cs
    GameState.cs
    IBlock1.cs
    JBlock.cs
    LBlock.cs
    MainWindow.xaml.cs
    OBlock.cs
    Position.cs
    SBlock.cs
    TBlock.cs
    ZBlock.cs
)

set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} /SUBSYSTEM:WINDOWS")

add_executable(Tetris ${SOURCE_FILES})

target_link_libraries(Tetris
    kernel32
    user32
    gdi32
    comdlg32
    ole32
    oleaut32
    uuid
    shlwapi
)

set_target_properties(Tetris PROPERTIES
    WIN32_ICON "${CMAKE_SOURCE_DIR}/Assets/Tetris.ico"
)

install(TARGETS Tetris DESTINATION ${CMAKE_INSTALL_PREFIX}/bin)