# Load the debug and release variables
file(GLOB DATA_FILES "${CMAKE_CURRENT_LIST_DIR}/corpus-*-data.cmake")

foreach(f ${DATA_FILES})
    include(${f})
endforeach()

# Create the targets for all the components
foreach(_COMPONENT ${corpus_COMPONENT_NAMES} )
    if(NOT TARGET ${_COMPONENT})
        add_library(${_COMPONENT} INTERFACE IMPORTED)
        message(${corpus_MESSAGE_MODE} "Conan: Component target declared '${_COMPONENT}'")
    endif()
endforeach()

if(NOT TARGET corpus::corpus)
    add_library(corpus::corpus INTERFACE IMPORTED)
    message(${corpus_MESSAGE_MODE} "Conan: Target declared 'corpus::corpus'")
endif()
# Load the debug and release library finders
file(GLOB CONFIG_FILES "${CMAKE_CURRENT_LIST_DIR}/corpus-Target-*.cmake")

foreach(f ${CONFIG_FILES})
    include(${f})
endforeach()