########### AGGREGATED COMPONENTS AND DEPENDENCIES FOR THE MULTI CONFIG #####################
#############################################################################################

set(xml_parser_COMPONENT_NAMES "")
if(DEFINED xml_parser_FIND_DEPENDENCY_NAMES)
  list(APPEND xml_parser_FIND_DEPENDENCY_NAMES )
  list(REMOVE_DUPLICATES xml_parser_FIND_DEPENDENCY_NAMES)
else()
  set(xml_parser_FIND_DEPENDENCY_NAMES )
endif()

########### VARIABLES #######################################################################
#############################################################################################
set(xml_parser_PACKAGE_FOLDER_RELEASE "/home/esat/.conan2/p/b/xml_p0019b0ea8d7bb/p")
set(xml_parser_BUILD_MODULES_PATHS_RELEASE )


set(xml_parser_INCLUDE_DIRS_RELEASE "${xml_parser_PACKAGE_FOLDER_RELEASE}/include")
set(xml_parser_RES_DIRS_RELEASE )
set(xml_parser_DEFINITIONS_RELEASE )
set(xml_parser_SHARED_LINK_FLAGS_RELEASE )
set(xml_parser_EXE_LINK_FLAGS_RELEASE )
set(xml_parser_OBJECTS_RELEASE )
set(xml_parser_COMPILE_DEFINITIONS_RELEASE )
set(xml_parser_COMPILE_OPTIONS_C_RELEASE )
set(xml_parser_COMPILE_OPTIONS_CXX_RELEASE )
set(xml_parser_LIB_DIRS_RELEASE "${xml_parser_PACKAGE_FOLDER_RELEASE}/lib")
set(xml_parser_BIN_DIRS_RELEASE )
set(xml_parser_LIBRARY_TYPE_RELEASE STATIC)
set(xml_parser_IS_HOST_WINDOWS_RELEASE 0)
set(xml_parser_LIBS_RELEASE XmlParser)
set(xml_parser_SYSTEM_LIBS_RELEASE )
set(xml_parser_FRAMEWORK_DIRS_RELEASE )
set(xml_parser_FRAMEWORKS_RELEASE )
set(xml_parser_BUILD_DIRS_RELEASE )
set(xml_parser_NO_SONAME_MODE_RELEASE FALSE)


# COMPOUND VARIABLES
set(xml_parser_COMPILE_OPTIONS_RELEASE
    "$<$<COMPILE_LANGUAGE:CXX>:${xml_parser_COMPILE_OPTIONS_CXX_RELEASE}>"
    "$<$<COMPILE_LANGUAGE:C>:${xml_parser_COMPILE_OPTIONS_C_RELEASE}>")
set(xml_parser_LINKER_FLAGS_RELEASE
    "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,SHARED_LIBRARY>:${xml_parser_SHARED_LINK_FLAGS_RELEASE}>"
    "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,MODULE_LIBRARY>:${xml_parser_SHARED_LINK_FLAGS_RELEASE}>"
    "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,EXECUTABLE>:${xml_parser_EXE_LINK_FLAGS_RELEASE}>")


set(xml_parser_COMPONENTS_RELEASE )