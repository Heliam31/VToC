#include <iostream>
#include <vector>
#include "portaudio.h"
//#include <wavefile.h>
#include <stdlib.h>
#include <iostream>
using namespace std;


static void checkErr(PaError err){
    if (err != paNoError){
        cout << "PortAudioError " << Pa_GetErrorText(err) << endl;
        exit(EXIT_FAILURE);
    }
}

int main(){
    PaError err;
    err = Pa_Initialize();
    checkErr(err);

    int numDevices = Pa_GetDeviceCount();
    cout<<"nb of devices : "<<numDevices<<endl;

    err = Pa_Terminate();
    checkErr(err);
    return EXIT_SUCCESS;
}





/*
// Paramètres de l'enregistrement audio
const int SAMPLE_RATE = 16000; // Fréquence d'échantillonnage (44.1 kHz)
const int FRAMES_PER_BUFFER = 256; // Taille du buffer audio
const int NUM_CHANNELS = 1; // Nombre de canaux (Mono)
const int SILENCE_THRESHOLD = 1000;

// Structure pour stocker l'audio
std::vector<float> audioBuffer;
std::atomic<bool> isRecording(true); 

// Fonction de callback pour l'enregistrement audio
int recordCallback(const void* inputBuffer, void* outputBuffer,
                  unsigned long framesPerBuffer, const PaStreamCallbackTimeInfo* timeInfo,
                  PaStreamCallbackFlags statusFlags, void* userData) {
    float* input = (float*)inputBuffer;

    // Calculer le volume moyen du buffer pour détecter si le micro capte quelque chose
    float volume = 0.0f;
    for (unsigned long i = 0; i < framesPerBuffer; ++i) {
        volume += fabs(input[i]);
    }
    volume /= framesPerBuffer;

    // Si le volume dépasse le seuil, on enregistre, sinon on arrête (en fonction de votre logique)
    if (volume > SILENCE_THRESHOLD && isRecording) {
        audioBuffer.insert(audioBuffer.end(), input, input + framesPerBuffer);
    }

    return paContinue;
}

// Fonction pour démarrer l'enregistrement audio
void recordAudio() {
    PaError err;
    err = Pa_Initialize();
    if (err != paNoError) {
        std::cerr << "Erreur lors de l'initialisation de PortAudio: " << Pa_GetErrorText(err) << std::endl;
        return;
    }

    // Ouvrir le flux audio pour capturer le microphone
    PaStream* stream;
    err = Pa_OpenDefaultStream(&stream, NUM_CHANNELS, 0, paFloat32, SAMPLE_RATE, FRAMES_PER_BUFFER, recordCallback, nullptr);
    if (err != paNoError) {
        std::cerr << "Erreur lors de l'ouverture du flux: " << Pa_GetErrorText(err) << std::endl;
        Pa_Terminate();
        return;
    }

    // Démarrer l'enregistrement audio
    err = Pa_StartStream(stream);
    if (err != paNoError) {
        std::cerr << "Erreur lors du démarrage du flux: " << Pa_GetErrorText(err) << std::endl;
        Pa_Terminate();
        return;
    }

    std::cout << "Enregistrement en cours, appuyez sur 'Enter' pour arrêter..." << std::endl;

    // Attendre que l'utilisateur appuie sur 'Enter' pour arrêter l'enregistrement
    std::cin.get();
    isRecording = false;

    // Arrêter l'enregistrement
    err = Pa_StopStream(stream);
    if (err != paNoError) {
        std::cerr << "Erreur lors de l'arrêt du flux: " << Pa_GetErrorText(err) << std::endl;
    }

    err = Pa_CloseStream(stream);
    if (err != paNoError) {
        std::cerr << "Erreur lors de la fermeture du flux: " << Pa_GetErrorText(err) << std::endl;
    }

    Pa_Terminate();

    std::cout << "Enregistrement terminé." << std::endl;
}

// Sauvegarde de l'audio dans un fichier WAV
void saveToWav(const std::string& filename) {
    WaveFile wf(SAMPLE_RATE, NUM_CHANNELS, audioBuffer.size());
    wf.write(filename, audioBuffer.data());
    std::cout << "Fichier audio sauvegardé : " << filename << std::endl;
}

int main() {
    // Lancer l'enregistrement dans un thread séparé
    std::thread recordThread(recordAudio);

    // Attendre que l'enregistrement se termine
    recordThread.join();

    // Sauvegarder le fichier audio
    saveToWav("audio_enregistre.wav");

    return 0;
}

*/