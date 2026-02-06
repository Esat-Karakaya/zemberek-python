# Load the debug and release variables
file(GLOB DATA_FILES "${CMAKE_CURRENT_LIST_DIR}/data_structure-*-data.cmake")

foreach(f ${DATA_FILES})
    include(${f})
endforeach()

# Create the targets for all the components
foreach(_COMPONENT ${data_structure_COMPONENT_NAMES} )
    if(NOT TARGET ${_COMPONENT})
        add_library(${_COMPONENT} INTERFACE IMPORTED)
        message(${data_structure_MESSAGE_MODE} "Conan: Component target declared '${_COMPONENT}'")
    endif()
endforeach()

if(NOT TARGET data_structure::data_structure)
    add_library(data_structure::data_structure INTERFACE IMPORTED)
    message(${data_structure_MESSAGE_MODE} "Conan: Target declared 'data_structure::data_structure'")
endif()
# Load the debug and release library finders
file(GLOB CONFIG_FILES "${CMAKE_CURRENT_LIST_DIR}/data_structure-Target-*.cmake")

foreach(f ${CONFIG_FILES})
    include(${f})
endforeach()