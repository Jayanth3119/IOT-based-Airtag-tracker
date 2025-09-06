# 📍 ESP32 UWB AirTag Clone  

This project replicates the **core features of Apple AirTag** — precision tracking and sound-based locating — using an **ESP32 UWB board**. It demonstrates how Ultra-Wideband (UWB) can be leveraged for short-range, centimeter-level tracking in a DIY setup.  

---

## 🚀 Project Overview  
- **Goal:** Recreate AirTag’s primary functions:  
  - Precision distance measurement between two devices.  
  - Sound playback for item locating.  
- **Hardware Used:**  
  - ESP32 UWB board with integrated UWB chip  
  - OLED display  
  - Push button (transmitter side)  
  - Buzzer (receiver side)  

---

## ⚙️ Feature Implementation  

- **📡 Precision Tracking**  
  - UWB technology measures distance between transmitter and receiver.  
  - Distance values are displayed in real-time on the OLED.  

- **🔊 Sound Playback**  
  - Pressing the transmitter button triggers a buzzer at the receiver.  
  - Implemented via **ESP-NOW**, a lightweight Wi-Fi protocol that enables peer-to-peer communication without a router.  

- **🔄 Loop Execution**  
  - Both tasks (distance measurement + buzzer control) run in the `loop()` function.  
  - Updates occur every **2 seconds** using a timer library.  

---

## 🖥️ Code and Circuit Details  

- **Libraries Used:** OLED, UWB functions, ESP-NOW, Timer.  
- **Configuration:**  
  - Each ESP32 board is assigned a unique MAC address for ESP-NOW broadcasting.  
  - Button and buzzer pins are defined separately for transmitter and receiver roles.  
- **Workflow:**  
  - Input setup → wireless communication → callback functions → handlers for UWB + sound tasks.  

---

## 🧪 Live Testing and Results  

- **Distance Measurement**  
  - OLED displayed values like **20 cm, 60–70 cm**, scaling accurately with receiver movement.  
- **Sound Playback**  
  - Pressing the transmitter button reliably triggered the buzzer on the receiver.  
- **Demo Test**  
  - Receiver was hidden indoors; using **OLED distance feedback + buzzer sound**, the device was successfully located.  

---

## ⚠️ Limitations  

- Unlike Apple’s AirTag, **global tracking is not supported**.  
- Apple leverages its **iPhone ecosystem** for worldwide location reporting — this DIY build works only for **close-range, peer-to-peer tracking**.  
