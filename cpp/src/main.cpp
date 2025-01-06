//whisper.cpp\build\bin\Release\whisper-cli -f whisper.cpp/samples/jfk.wav

#include <iostream>
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <string>
#include <filesystem>

namespace fs = std::filesystem;

std::string transcribeAudio(const std::string& audioPath, const std::string& modelPath) {
    std::string command = "..\\whisper.cpp\\build\\bin\\Release\\whisper-cli -m "+ modelPath + " -f " + audioPath + " -otxt";
    int result = std::system(command.c_str());
    if (result != 0) {
        std::cerr << "Erreur : La transcription a échoué." << std::endl;
        return "";
    }
    
    std::string transcriptFile = audioPath + ".txt";
    std::ifstream transcriptStream(transcriptFile);
    if (!transcriptStream.is_open()) {
        std::cerr << "Erreur : Impossible de lire le fichier de transcription." << std::endl;
        return "";
    }

    std::ostringstream transcription;
    transcription << transcriptStream.rdbuf();
    transcriptStream.close();

    return transcription.str();
}

int main() {
    std::string audioPath = "../ans/jfk.wav";
    
    std::string modelPath = "../whisper.cpp/models/ggml-base.en.bin"; 

    if (!fs::exists(audioPath)) {
        std::cerr << "Erreur : Le fichier audio " << audioPath << " n'existe pas." << std::endl;
        return 1;
    }
    if (!fs::exists(modelPath)) {
        std::cerr << "Erreur : Le modèle Whisper " << modelPath << " n'existe pas." << std::endl;
        return 1;
    }

    while (1){

        // Étape 1 : Transcrire l'audio
        std::string transcription = transcribeAudio(audioPath, modelPath);
        if (transcription.empty()) {
            std::cerr << "Erreur : La transcription a échoué." << std::endl;
            return 1;
        }
        std::cout << "message decoded : " << transcription << std::endl;

    }

    return 0;
}