
# 🎵 YoutubeAudioWeb

A lightweight, local web-based control center built with **Flask** and optimized for **Raspberry Pi 3** running **Raspberry Pi OS Lite**. This project allows you to stream audio directly from YouTube links and manage playback in real-time (Play, Pause, Mute, and Volume Control) using a mobile-friendly web interface hosted on your local network.

It leverages `mpv` media player background execution and inter-process communication (IPC) via `socat` sockets for low-latency responses.

---

## ✨ Features

* **🌐 Web Control Panel:** Modern Spotify-like UI optimized for smartphones and desktop browsers alike.
* **⚡ Low Latency Controls:** Background control via `mpv` IPC sockets (`/tmp/mpv-socket`), enabling immediate Pause, Mute, and Volume Adjustments without reloading pages.
* **🚀 Tailored for OS Lite:** Runs strictly in a headless CLI environment without any graphical desktop interface dependencies.
* **🛡️ Smart Collision Handling:** Automatically terminates existing `mpv` streaming processes when a new video link is triggered to prevent overlapping audio channels.

---

## 🛠️ System Dependencies & Hardware

* **Hardware:** Raspberry Pi 3 (Model B / B+).
* **OS:** Raspberry Pi OS Lite (Bullseye/Bookworm).
* **Core Requirements:** Audio Output configured (3.5mm Jack, HDMI, or USB/I2S Speaker Card).

---

## 🚀 Installation & Setup

### 1. Install System Media Libraries
Since this project routes commands via a Unix socket, you must install `mpv` and the network utility `socat` along with standard audio utilities:

```bash
sudo apt-get update
sudo apt-get install -y mpv socat alsa-utils ffmpeg
```


### 2. Clone the Repository
```bash
git clone [https://github.com/mohamed4hanon/YoutubeAudioWeb.git](https://github.com/mohamed4hanon/YoutubeAudioWeb.git)
cd YoutubeAudioWeb
````

### 3. Install Python Dependencies
Install Flask, which powers the backend routing server:

```bash
pip install Flask
```

💡 Note for Debian Bookworm (Newer OS Lite): If you encounter an externally-managed-environment error, set up a virtual environment before installing packages:

```bash
python3 -m venv venv
source venv/bin/activate
pip install Flask
```

## 💻 Usage
### 1. Launch the Server
Execute the main application script (assumed to be named app.py or the script containing the Flask initialization):
```bash
python app.py
```
Note: The application binds to 0.0.0.0:5000, making it accessible across your entire local network.

### 2. Accessing the Dashboard
Open a browser on any device (Phone, Tablet, or PC) connected to the same local network and visit:



```Plaintext
http://<your-raspberry-pi-ip>:5000
````
(You can find your Pi's IP address on OS Lite by running hostname -I).




## 🎮 Interface Directives:
- Play: Paste any valid YouTube URL inside the text bar and press ▶ تشغيل مقطع جديد.

- Pause/Resume: Instantly toggle media playback states.

- Volume (+ / -): Adjust internal script playback values incrementally by 10%.

- Stop: Safely kills background player routines.

## 📜 License
This project is open-source and licensed under the MIT License.






