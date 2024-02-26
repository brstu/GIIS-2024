cmake_minimum_required (VERSION 3.15)
project (GIIS) 

option(PY_LANGUAGE OFF)
option(CXX_LANGUAGE OFF)

if(PY_LANGUAGE)
file(GLOB python_dirs RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "trunk/ii0*/*/src/main.py")
file(GLOB depend_dirs RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "trunk/ii0*/*/src/requirements.txt")
file(WRITE depend_path.txt "")
file(WRITE python_path.txt "")
foreach(r_dir ${depend_dirs})
    
        file(GLOB r_dirs ${depend_dir})
		file(APPEND depend_path.txt "${r_dir}\n")	

endforeach()
foreach(dir ${python_dirs})
    
        file(GLOB python_scripts ${dir})
		file(APPEND python_path.txt "${dir}\n")	

endforeach()
endif()

if(CXX_LANGUAGE)
file(GLOB V_GLOB RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "trunk/ii0*/*/src/")
foreach(item ${V_GLOB})	
	message( "Find \"${item}\"" )
	add_subdirectory(${item})
endforeach()
endif()