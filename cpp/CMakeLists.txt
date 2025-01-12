# CMakeLists.txt

cmake_minimum_required(VERSION 3.10) 

project("VtoC" C CXX)
project("VtoC" VERSION 1.7.3)

set(CMAKE_CXX_STANDARD 17)       

# Ajout du fichier source à la cible
add_executable(main src/main.cpp)
add_executable(record src/record.cpp)

# Trouver la bibliothèque PortAudio
add_subdirectory("C:\\Users\\mihai\\Desktop\\VtoC\\lib\\portaudio" "C:\\Users\\mihai\\Desktop\\VtoC\\binPA" EXCLUDE_FROM_ALL)
