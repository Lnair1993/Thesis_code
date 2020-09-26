# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "rail_segmentation: 0 messages, 1 services")

set(MSG_I_FLAGS "")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(rail_segmentation_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/lnair3/Nimbus_ws/src/rail_segmentation/srv/RemoveObject.srv" NAME_WE)
add_custom_target(_rail_segmentation_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "rail_segmentation" "/home/lnair3/Nimbus_ws/src/rail_segmentation/srv/RemoveObject.srv" ""
)

#
#  langs = gencpp;geneus;genlisp;genpy
#

### Section generating for lang: gencpp
### Generating Messages

### Generating Services
_generate_srv_cpp(rail_segmentation
  "/home/lnair3/Nimbus_ws/src/rail_segmentation/srv/RemoveObject.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rail_segmentation
)

### Generating Module File
_generate_module_cpp(rail_segmentation
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rail_segmentation
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(rail_segmentation_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(rail_segmentation_generate_messages rail_segmentation_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/lnair3/Nimbus_ws/src/rail_segmentation/srv/RemoveObject.srv" NAME_WE)
add_dependencies(rail_segmentation_generate_messages_cpp _rail_segmentation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rail_segmentation_gencpp)
add_dependencies(rail_segmentation_gencpp rail_segmentation_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rail_segmentation_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages

### Generating Services
_generate_srv_eus(rail_segmentation
  "/home/lnair3/Nimbus_ws/src/rail_segmentation/srv/RemoveObject.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rail_segmentation
)

### Generating Module File
_generate_module_eus(rail_segmentation
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rail_segmentation
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(rail_segmentation_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(rail_segmentation_generate_messages rail_segmentation_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/lnair3/Nimbus_ws/src/rail_segmentation/srv/RemoveObject.srv" NAME_WE)
add_dependencies(rail_segmentation_generate_messages_eus _rail_segmentation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rail_segmentation_geneus)
add_dependencies(rail_segmentation_geneus rail_segmentation_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rail_segmentation_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages

### Generating Services
_generate_srv_lisp(rail_segmentation
  "/home/lnair3/Nimbus_ws/src/rail_segmentation/srv/RemoveObject.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rail_segmentation
)

### Generating Module File
_generate_module_lisp(rail_segmentation
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rail_segmentation
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(rail_segmentation_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(rail_segmentation_generate_messages rail_segmentation_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/lnair3/Nimbus_ws/src/rail_segmentation/srv/RemoveObject.srv" NAME_WE)
add_dependencies(rail_segmentation_generate_messages_lisp _rail_segmentation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rail_segmentation_genlisp)
add_dependencies(rail_segmentation_genlisp rail_segmentation_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rail_segmentation_generate_messages_lisp)

### Section generating for lang: genpy
### Generating Messages

### Generating Services
_generate_srv_py(rail_segmentation
  "/home/lnair3/Nimbus_ws/src/rail_segmentation/srv/RemoveObject.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rail_segmentation
)

### Generating Module File
_generate_module_py(rail_segmentation
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rail_segmentation
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(rail_segmentation_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(rail_segmentation_generate_messages rail_segmentation_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/lnair3/Nimbus_ws/src/rail_segmentation/srv/RemoveObject.srv" NAME_WE)
add_dependencies(rail_segmentation_generate_messages_py _rail_segmentation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rail_segmentation_genpy)
add_dependencies(rail_segmentation_genpy rail_segmentation_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rail_segmentation_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rail_segmentation)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rail_segmentation
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rail_segmentation)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rail_segmentation
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rail_segmentation)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rail_segmentation
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rail_segmentation)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rail_segmentation\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rail_segmentation
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
