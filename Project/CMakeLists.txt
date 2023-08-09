# File: CMakeLists.txt
# Author: Dean Ciarniello
# Date: 2023-07-28

# Setup Project
# ===========================================
cmake_minimum_required(VERSION 2.8.12 FATAL_ERROR)
project(Simulation)

# Setup Geant4 package
# ===========================================
option(WITH_GEANT4_UIVIS "Build example with Geant4 UI and Vis drivers" ON)
if(WITH_GEANT4_UIVIS)
  find_package(Geant4 REQUIRED ui_all vis_all)
else()
  find_package(Geant4 REQUIRED)
endif()

# Setup geant4 include dirs
# ===========================================
include(${Geant4_USE_FILE})
include_directories(${PROJECT_SOURCE_DIR}/include)

# Find sources and headers
# ===========================================
file(GLOB sources ${PROJECT_SOURCE_DIR}/src/*.cc)
file(GLOB headers ${PROJECT_SOURCE_DIR}/include/*.hh)

# Find and copy .mac files
# ===========================================
file(GLOB macro_files  ${PROJECT_SOURCE_DIR}/mac/*.mac)
file(COPY ${macro_files} DESTINATION ${PROJECT_BINARY_DIR})

# Add exec and link libraries to target
# ===========================================
add_executable(simulation simulation.cc ${sources} ${headers})
target_link_libraries(simulation ${Geant4_LIBRARIES})

# Add target simulation
# ===========================================
add_custom_target(Simulation DEPENDS simulation)