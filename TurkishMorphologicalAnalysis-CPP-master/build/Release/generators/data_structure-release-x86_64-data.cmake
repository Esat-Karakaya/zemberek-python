########### AGGREGATED COMPONENTS AND DEPENDENCIES FOR THE MULTI CONFIG #####################
#############################################################################################

set(data_structure_COMPONENT_NAMES "")
if(DEFINED data_structure_FIND_DEPENDENCY_NAMES)
  list(APPEND data_structure_FIND_DEPENDENCY_NAMES )
  list(REMOVE_DUPLICATES data_structure_FIND_DEPENDENCY_NAMES)
else()
  set(data_structure_FIND_DEPENDENCY_NAMES )
endif()

########### VARIABLES #######################################################################
#############################################################################################
set(data_structure_PACKAGE_FOLDER_RELEASE "/home/esat/.conan2/p/b/data_e974885eb2ed0/p")
set(data_structure_BUILD_MODULES_PATHS_RELEASE )


set(data_structure_INCLUDE_DIRS_RELEASE "${data_structure_PACKAGE_FOLDER_RELEASE}/include")
set(data_structure_RES_DIRS_RELEASE )
set(data_structure_DEFINITIONS_RELEASE )
set(data_structure_SHARED_LINK_FLAGS_RELEASE )
set(data_structure_EXE_LINK_FLAGS_RELEASE )
set(data_structure_OBJECTS_RELEASE )
set(data_structure_COMPILE_DEFINITIONS_RELEASE )
set(data_structure_COMPILE_OPTIONS_C_RELEASE )
set(data_structure_COMPILE_OPTIONS_CXX_RELEASE )
set(data_structure_LIB_DIRS_RELEASE "${data_structure_PACKAGE_FOLDER_RELEASE}/lib")
set(data_structure_BIN_DIRS_RELEASE )
set(data_structure_LIBRARY_TYPE_RELEASE UNKNOWN)
set(data_structure_IS_HOST_WINDOWS_RELEASE 0)
set(data_structure_LIBS_RELEASE )
set(data_structure_SYSTEM_LIBS_RELEASE )
set(data_structure_FRAMEWORK_DIRS_RELEASE )
set(data_structure_FRAMEWORKS_RELEASE )
set(data_structure_BUILD_DIRS_RELEASE )
set(data_structure_NO_SONAME_MODE_RELEASE FALSE)


# COMPOUND VARIABLES
set(data_structure_COMPILE_OPTIONS_RELEASE
    "$<$<COMPILE_LANGUAGE:CXX>:${data_structure_COMPILE_OPTIONS_CXX_RELEASE}>"
    "$<$<COMPILE_LANGUAGE:C>:${data_structure_COMPILE_OPTIONS_C_RELEASE}>")
set(data_structure_LINKER_FLAGS_RELEASE
    "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,SHARED_LIBRARY>:${data_structure_SHARED_LINK_FLAGS_RELEASE}>"
    "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,MODULE_LIBRARY>:${data_structure_SHARED_LINK_FLAGS_RELEASE}>"
    "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,EXECUTABLE>:${data_structure_EXE_LINK_FLAGS_RELEASE}>")


set(data_structure_COMPONENTS_RELEASE )