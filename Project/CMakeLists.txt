# Setup Project
cmake_minimum_required(VERSION 2.8.12 FATAL_ERROR)
project(Simulation)

# Setup Geant4 package
option(WITH_GEANT4_UIVIS "Build example with Geant4 UI and Vis drivers" ON)
if(WITH_GEANT4_UIVIS)
  find_package(Geant4 REQUIRED ui_all vis_all)
else()
  find_package(Geant4 REQUIRED)
endif()

# Setup geant4 include dirs
include(${Geant4_USE_FILE})
include_directories(${PROJECT_SOURCE_DIR}/include)

# find sources and headers
file(GLOB sources ${PROJECT_SOURCE_DIR}/src/*.cc)
file(GLOB headers ${PROJECT_SOURCE_DIR}/include/*.hh)

file(GLOB MACRO_FILES *.mac)
file(COPY ${MACRO_FILES} DESTINATION ${PROJECT_BINARY_DIR})

add_executable(simulation simulation.cc ${sources} ${headers})
target_link_libraries(simulation ${Geant4_LIBRARIES})

# add target
add_custom_target(Simulation DEPENDS simulation)