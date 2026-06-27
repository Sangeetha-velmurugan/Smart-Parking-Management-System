**Smart Parking Management System**

A web-based parking system built with Python & Flask that automates slot allocation, tracks vehicle entry/exit, and generates bills automaticall

**Live Demo** https://smart-parking-management-system-bhn6.onrender.com

**Features**

 · Auto slot allocation using Min Heap — always assigns the nearest available slot in O(log n)

 · Records entry & exit times automatically

 · Calculates parking duration and generates a bill

 · Real-time parking status view

**Setup**

    git clone https://github.com/hariharanm30/Smart-Parking-Management-System.git
    cd Smart-Parking-Management-System
    pip install -r requirements.txt
    python app.py

Visit http://127.0.0.1:5000

 · User parks a vehicle → system picks the lowest-numbered free slot via min-heap

 · Entry time is recorded

 · On exit → duration is calculated, bill is generated, slot is freed

**Future Enhancements**

Database integration  · User auth · QR code entry · Online payments · Admin dashboard

