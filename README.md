# 📍 IoT-Based AirTag Tracker

This project presents a simplified **IoT-based tracking system** inspired by Apple’s AirTag. It uses the **ESP8266**, **SIM800L GSM module**, a **buzzer**, and a **breadboard** for rapid prototyping. The objective is to build a compact and affordable device that helps users locate lost items via **automatic alerts** and **GSM-based location tracking**.

---

## 🚀 Features

- 📡 **GSM-Based Location Tracking** – Uses cellular tower triangulation to determine approximate location.
- 🔊 **Buzzer Alert System** – Emits a loud sound when triggered for easy item location.
- 🌐 **Cloud Integration (ThingSpeak)** – Sends GPS coordinates to ThingSpeak for real-time monitoring.
- ⚙️ **Automated Triggers** – Buzzer is activated automatically on motion detection or power-up.
- ❌ **No SMS or Relay Required** – Simplified design, eliminating need for manual commands.
- 🌍 **Works Without Wi-Fi** – GSM connectivity ensures tracking in remote areas.

---

## 🧰 Hardware Requirements

- ✅ ESP8266 NodeMCU
- ✅ SIM800L GSM Module
- ✅ Active Buzzer
- ✅ Breadboard & Jumper Wires
- ✅ Power Supply (Lithium-ion battery recommended)

---

## 🛠️ Circuit Diagram

> 📌 *Coming Soon* – You can include a Fritzing diagram or schematic image here to visually explain wiring.

---

## ⚙️ How It Works

1. On power-up or motion detection, the ESP8266 communicates with the SIM800L module.
2. The GSM module fetches approximate location using nearby cell tower data.
3. Location data is uploaded to **ThingSpeak** for real-time cloud-based tracking.
4. Simultaneously, the ESP triggers the buzzer using a GPIO pin to emit a sound for nearby locating.
5. No user intervention (e.g., SMS) is required for operation.

---

## 📈 ThingSpeak Integration

1. Create a [ThingSpeak](https://thingspeak.com) account.
2. Create a new channel and note the **Write API Key**.
3. Update your ESP8266 firmware code with the ThingSpeak credentials.
4. Monitor the location data and alerts via the ThingSpeak dashboard.

---

## 📦 Project Folder Structure

