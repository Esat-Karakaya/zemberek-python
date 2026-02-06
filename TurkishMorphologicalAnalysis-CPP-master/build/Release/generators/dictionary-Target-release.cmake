# Avoid multiple calls to find_package to append duplicated properties to the targets
include_guard()########### VARIABLES #######################################################################
#############################################################################################
set(dictionary_FRAMEWORKS_FOUND_RELEASE "") # Will be filled later
conan_find_apple_frameworks(dictionary_FRAMEWORKS_FOUND_RELEASE "${dictionary_FRAMEWORKS_RELEASE}" "${dictionary_FRAMEWORK_DIRS_RELEASE}")

set(dictionary_LIBRARIES_TARGETS "") # Will be filled later


######## Create an interface target to contain all the dependencies (frameworks, system and conan deps)
if(NOT TARGET dictionary_DEPS_TARGET)
    add_library(dictionary_DEPS_TARGET INTERFACE IMPORTED)
endif()

set_property(TARGET dictionary_DEPS_TARGET
             APPEND PROPERTY INTERFACE_LINK_LIBRARIES
             $<$<CONFIG:Release>:${dictionary_FRAMEWORKS_FOUND_RELEASE}>
             $<$<CONFIG:Release>:${dictionary_SYSTEM_LIBS_RELEASE}>
             $<$<CONFIG:Release>:math::math;util::util>)

####### Find the libraries declared in cpp_info.libs, create an IMPORTED target for each one and link the
####### dictionary_DEPS_TARGET to all of them
conan_package_library_targets("${dictionary_LIBS_RELEASE}"    # libraries
                              "${dictionary_LIB_DIRS_RELEASE}" # package_libdir
                              "${dictionary_BIN_DIRS_RELEASE}" # package_bindir
                              "${dictionary_LIBRARY_TYPE_RELEASE}"
                              "${dictionary_IS_HOST_WINDOWS_RELEASE}"
                              dictionary_DEPS_TARGET
                              dictionary_LIBRARIES_TARGETS  # out_libraries_targets
                              "_RELEASE"
                              "dictionary"    # package_name
                              "${dictionary_NO_SONAME_MODE_RELEASE}")  # soname

# FIXME: What is the result of this for multi-config? All configs adding themselves to path?
set(CMAKE_MODULE_PATH ${dictionary_BUILD_DIRS_RELEASE} ${CMAKE_MODULE_PATH})

########## GLOBAL TARGET PROPERTIES Release ########################################
    set_property(TARGET dictionary::dictionary
                 APPEND PROPERTY INTERFACE_LINK_LIBRARIES
                 $<$<CONFIG:Release>:${dictionary_OBJECTS_RELEASE}>
                 $<$<CONFIG:Release>:${dictionary_LIBRARIES_TARGETS}>
                 )

    if("${dictionary_LIBS_RELEASE}" STREQUAL "")
        # If the package is not declaring any "cpp_info.libs" the package deps, system libs,
        # frameworks etc are not linked to the imported targets and we need to do it to the
        # global target
        set_property(TARGET dictionary::dictionary
                     APPEND PROPERTY INTERFACE_LINK_LIBRARIES
                     dictionary_DEPS_TARGET)
    endif()

    set_property(TARGET dictionary::dictionary
                 APPEND PROPERTY INTERFACE_LINK_OPTIONS
                 $<$<CONFIG:Release>:${dictionary_LINKER_FLAGS_RELEASE}>)
    set_property(TARGET dictionary::dictionary
                 APPEND PROPERTY INTERFACE_INCLUDE_DIRECTORIES
                 $<$<CONFIG:Release>:${dictionary_INCLUDE_DIRS_RELEASE}>)
    # Necessary to find LINK shared libraries in Linux
    set_property(TARGET dictionary::dictionary
                 APPEND PROPERTY INTERFACE_LINK_DIRECTORIES
                 $<$<CONFIG:Release>:${dictionary_LIB_DIRS_RELEASE}>)
    set_property(TARGET dictionary::dictionary
                 APPEND PROPERTY INTERFACE_COMPILE_DEFINITIONS
                 $<$<CONFIG:Release>:${dictionary_COMPILE_DEFINITIONS_RELEASE}>)
    set_property(TARGET dictionary::dictionary
                 APPEND PROPERTY INTERFACE_COMPILE_OPTIONS
                 $<$<CONFIG:Release>:${dictionary_COMPILE_OPTIONS_RELEASE}>)

########## For the modules (FindXXX)
set(dictionary_LIBRARIES_RELEASE dictionary::dictionary)
