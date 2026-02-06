# Load the debug and release variables
file(GLOB DATA_FILES "${CMAKE_CURRENT_LIST_DIR}/xml_parser-*-data.cmake")

foreach(f ${DATA_FILES})
    include(${f})
endforeach()

# Create the targets for all the components
foreach(_COMPONENT ${xml_parser_COMPONENT_NAMES} )
    if(NOT TARGET ${_COMPONENT})
        add_library(${_COMPONENT} INTERFACE IMPORTED)
        message(${xml_parser_MESSAGE_MODE} "Conan: Component target declared '${_COMPONENT}'")
    endif()
endforeach()

if(NOT TARGET xml_parser::xml_parser)
    add_library(xml_parser::xml_parser INTERFACE IMPORTED)
    message(${xml_parser_MESSAGE_MODE} "Conan: Target declared 'xml_parser::xml_parser'")
endif()
# Load the debug and release library finders
file(GLOB CONFIG_FILES "${CMAKE_CURRENT_LIST_DIR}/xml_parser-Target-*.cmake")

foreach(f ${CONFIG_FILES})
    include(${f})
endforeach()