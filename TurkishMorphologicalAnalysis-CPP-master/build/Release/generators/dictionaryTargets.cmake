# Load the debug and release variables
file(GLOB DATA_FILES "${CMAKE_CURRENT_LIST_DIR}/dictionary-*-data.cmake")

foreach(f ${DATA_FILES})
    include(${f})
endforeach()

# Create the targets for all the components
foreach(_COMPONENT ${dictionary_COMPONENT_NAMES} )
    if(NOT TARGET ${_COMPONENT})
        add_library(${_COMPONENT} INTERFACE IMPORTED)
        message(${dictionary_MESSAGE_MODE} "Conan: Component target declared '${_COMPONENT}'")
    endif()
endforeach()

if(NOT TARGET dictionary::dictionary)
    add_library(dictionary::dictionary INTERFACE IMPORTED)
    message(${dictionary_MESSAGE_MODE} "Conan: Target declared 'dictionary::dictionary'")
endif()
# Load the debug and release library finders
file(GLOB CONFIG_FILES "${CMAKE_CURRENT_LIST_DIR}/dictionary-Target-*.cmake")

foreach(f ${CONFIG_FILES})
    include(${f})
endforeach()