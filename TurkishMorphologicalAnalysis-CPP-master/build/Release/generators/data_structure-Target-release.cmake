# Avoid multiple calls to find_package to append duplicated properties to the targets
include_guard()########### VARIABLES #######################################################################
#############################################################################################
set(data_structure_FRAMEWORKS_FOUND_RELEASE "") # Will be filled later
conan_find_apple_frameworks(data_structure_FRAMEWORKS_FOUND_RELEASE "${data_structure_FRAMEWORKS_RELEASE}" "${data_structure_FRAMEWORK_DIRS_RELEASE}")

set(data_structure_LIBRARIES_TARGETS "") # Will be filled later


######## Create an interface target to contain all the dependencies (frameworks, system and conan deps)
if(NOT TARGET data_structure_DEPS_TARGET)
    add_library(data_structure_DEPS_TARGET INTERFACE IMPORTED)
endif()

set_property(TARGET data_structure_DEPS_TARGET
             APPEND PROPERTY INTERFACE_LINK_LIBRARIES
             $<$<CONFIG:Release>:${data_structure_FRAMEWORKS_FOUND_RELEASE}>
             $<$<CONFIG:Release>:${data_structure_SYSTEM_LIBS_RELEASE}>
             $<$<CONFIG:Release>:>)

####### Find the libraries declared in cpp_info.libs, create an IMPORTED target for each one and link the
####### data_structure_DEPS_TARGET to all of them
conan_package_library_targets("${data_structure_LIBS_RELEASE}"    # libraries
                              "${data_structure_LIB_DIRS_RELEASE}" # package_libdir
                              "${data_structure_BIN_DIRS_RELEASE}" # package_bindir
                              "${data_structure_LIBRARY_TYPE_RELEASE}"
                              "${data_structure_IS_HOST_WINDOWS_RELEASE}"
                              data_structure_DEPS_TARGET
                              data_structure_LIBRARIES_TARGETS  # out_libraries_targets
                              "_RELEASE"
                              "data_structure"    # package_name
                              "${data_structure_NO_SONAME_MODE_RELEASE}")  # soname

# FIXME: What is the result of this for multi-config? All configs adding themselves to path?
set(CMAKE_MODULE_PATH ${data_structure_BUILD_DIRS_RELEASE} ${CMAKE_MODULE_PATH})

########## GLOBAL TARGET PROPERTIES Release ########################################
    set_property(TARGET data_structure::data_structure
                 APPEND PROPERTY INTERFACE_LINK_LIBRARIES
                 $<$<CONFIG:Release>:${data_structure_OBJECTS_RELEASE}>
                 $<$<CONFIG:Release>:${data_structure_LIBRARIES_TARGETS}>
                 )

    if("${data_structure_LIBS_RELEASE}" STREQUAL "")
        # If the package is not declaring any "cpp_info.libs" the package deps, system libs,
        # frameworks etc are not linked to the imported targets and we need to do it to the
        # global target
        set_property(TARGET data_structure::data_structure
                     APPEND PROPERTY INTERFACE_LINK_LIBRARIES
                     data_structure_DEPS_TARGET)
    endif()

    set_property(TARGET data_structure::data_structure
                 APPEND PROPERTY INTERFACE_LINK_OPTIONS
                 $<$<CONFIG:Release>:${data_structure_LINKER_FLAGS_RELEASE}>)
    set_property(TARGET data_structure::data_structure
                 APPEND PROPERTY INTERFACE_INCLUDE_DIRECTORIES
                 $<$<CONFIG:Release>:${data_structure_INCLUDE_DIRS_RELEASE}>)
    # Necessary to find LINK shared libraries in Linux
    set_property(TARGET data_structure::data_structure
                 APPEND PROPERTY INTERFACE_LINK_DIRECTORIES
                 $<$<CONFIG:Release>:${data_structure_LIB_DIRS_RELEASE}>)
    set_property(TARGET data_structure::data_structure
                 APPEND PROPERTY INTERFACE_COMPILE_DEFINITIONS
                 $<$<CONFIG:Release>:${data_structure_COMPILE_DEFINITIONS_RELEASE}>)
    set_property(TARGET data_structure::data_structure
                 APPEND PROPERTY INTERFACE_COMPILE_OPTIONS
                 $<$<CONFIG:Release>:${data_structure_COMPILE_OPTIONS_RELEASE}>)

########## For the modules (FindXXX)
set(data_structure_LIBRARIES_RELEASE data_structure::data_structure)
