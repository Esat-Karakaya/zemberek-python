########### AGGREGATED COMPONENTS AND DEPENDENCIES FOR THE MULTI CONFIG #####################
#############################################################################################

set(math_COMPONENT_NAMES "")
if(DEFINED math_FIND_DEPENDENCY_NAMES)
  list(APPEND math_FIND_DEPENDENCY_NAMES )
  list(REMOVE_DUPLICATES math_FIND_DEPENDENCY_NAMES)
else()
  set(math_FIND_DEPENDENCY_NAMES )
endif()

########### VARIABLES #######################################################################
#############################################################################################
set(math_PACKAGE_FOLDER_RELEASE "/home/esat/.conan2/p/b/math811b26346eaaa/p")
set(math_BUILD_MODULES_PATHS_RELEASE )


set(math_INCLUDE_DIRS_RELEASE )
set(math_RES_DIRS_RELEASE )
set(math_DEFINITIONS_RELEASE )
set(math_SHARED_LINK_FLAGS_RELEASE )
set(math_EXE_LINK_FLAGS_RELEASE )
set(math_OBJECTS_RELEASE )
set(math_COMPILE_DEFINITIONS_RELEASE )
set(math_COMPILE_OPTIONS_C_RELEASE )
set(math_COMPILE_OPTIONS_CXX_RELEASE )
set(math_LIB_DIRS_RELEASE "${math_PACKAGE_FOLDER_RELEASE}/lib")
set(math_BIN_DIRS_RELEASE )
set(math_LIBRARY_TYPE_RELEASE STATIC)
set(math_IS_HOST_WINDOWS_RELEASE 0)
set(math_LIBS_RELEASE Math)
set(math_SYSTEM_LIBS_RELEASE )
set(math_FRAMEWORK_DIRS_RELEASE )
set(math_FRAMEWORKS_RELEASE )
set(math_BUILD_DIRS_RELEASE )
set(math_NO_SONAME_MODE_RELEASE FALSE)


# COMPOUND VARIABLES
set(math_COMPILE_OPTIONS_RELEASE
    "$<$<COMPILE_LANGUAGE:CXX>:${math_COMPILE_OPTIONS_CXX_RELEASE}>"
    "$<$<COMPILE_LANGUAGE:C>:${math_COMPILE_OPTIONS_C_RELEASE}>")
set(math_LINKER_FLAGS_RELEASE
    "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,SHARED_LIBRARY>:${math_SHARED_LINK_FLAGS_RELEASE}>"
    "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,MODULE_LIBRARY>:${math_SHARED_LINK_FLAGS_RELEASE}>"
    "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,EXECUTABLE>:${math_EXE_LINK_FLAGS_RELEASE}>")


set(math_COMPONENTS_RELEASE )