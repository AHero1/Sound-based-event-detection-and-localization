# Sound-based-event-detection-and-localization
## 1. Introduction
Sound-based event detection and localization play significant roles in various applications such as surveillance, robotics, and threat detection. In this project, we aimed to develop a system using signal processing methods to accurately detect and localize whistle sounds. We utilized a microphone array setup along with a Raspberry Pi for real-time processing.

## 2. Methodology

### 2.1 Microphone Array Setup:
- We designed a microphone array consisting of multiple microphones positioned in a circular configuration to capture audio signals from different directions.
- Spatial resolution was considered by adjusting the distance between microphones to ensure accurate localization of sound sources.
- Frequency range was accounted for by ensuring that the inter-microphone distance was smaller than the wavelength of the highest frequency of interest.

### 2.2 Raspberry Pi Integration:
- A Raspberry Pi 4 Model B served as the main processing unit due to its sufficient processing power and memory capabilities.
- USB ports or a USB hub were used to install different microphones at a distance from the Raspberry Pi.


### 2.3 Audio Signal Preprocessing:
- Frequency selective filtering was employed to localize whistle sounds in captured signals from microphones.
- Echo removal techniques were implemented to eliminate echoes, especially in indoor environments.

### 2.4 Direction Estimation:
- Time delay estimation (TDE) techniques such as cross-correlation were utilized to estimate the arrival time differences of the whistle signal at different microphones.
- Triangulation algorithms were implemented to estimate the direction of arrival (DOA) based on the TDEs.

### 2.5 Real-Time Operation:
- The system was designed to operate in real-time with minimal latency between audio capture, processing, and output.
- Efficient buffering mechanisms were developed to handle audio streams without dropping frames or introducing significant delays.

## 3.Implementation

- Developed software interfaces to interact with hardware components, including GPIO pins for controlling peripherals and SPI/I2C for communication with external devices.
- Utilized Python libraries such as RPi.GPIO for GPIO interfacing and PyAudio for audio processing.
- Optimized algorithms and computations to fit the resource constraints of the Raspberry Pi.

## 4. Results

- Achieved accurate detection and localization of whistle sounds in both indoor and outdoor environments.
- Real-time operation was successfully demonstrated with minimal latency.
- The system showed robustness against noise and echoes, providing reliable performance.

## 5. Conclusion

In conclusion, the developed system effectively detects and localizes whistle sounds using a microphone array and Raspberry Pi. The project demonstrates the potential of signal processing techniques in various practical applications such as surveillance and robotics. Future work may involve further optimization for resource-constrained platforms and expansion to detect and localize other types of sound events.
