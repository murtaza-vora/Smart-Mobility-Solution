# Smart Mobility Solution

A research-driven smart traffic system that uses Vehicle-to-Everything (V2X) communication, computer vision, and reinforcement learning to reduce transit delays and optimize traffic flow in urban environments.

---

## 🚀 Project Summary

Cities are growing, roads are getting busier, and buses often run late due to congestion. This project aims to solve that problem by building an intelligent traffic coordination system that:

- Detects vehicles using computer vision (YOLO + CNN)
- Communicates with roadside units through V2X technology
- Simulates real traffic scenarios using SUMO
- Uses reinforcement learning (D3QN) to optimize traffic light timing

The end goal is a scalable solution that helps municipalities reduce delays and improve traffic efficiency using AI-driven control systems.

---

## ✨ Key Features

- ✅ Real-time data processing from transit vehicles and sensors  
- ✅ Object detection using YOLO and CNN models  
- ✅ SUMO-based smart mobility simulation  
- ✅ Reinforcement learning for intersection control  
- ▶️ Video demonstrations included

---

## 📂 Repository Structure

Smart-Mobility-Solution/
│── videos/ # Demo output clips
│── simulation_files/ # SUMO-related files (if applicable)
│── models/ # Detection and RL models (if shared)
│── experiment_outputs/ # Test logs / images
│── README.md
└── other project files...


> *Note: Additional files and datasets may be linked via Google Drive due to size.*

---

## 🛠 Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/murtaza-vora/Smart-Mobility-Solution.git
cd Smart-Mobility-Solution

```
Create enviroment 

```
conda create --name smartmobility python=3.10
conda activate smartmobility
```

Install dependencies 

```
pip install -r requirements.txt

```

Current status

| Stage                                        | Status         |
| -------------------------------------------- | -------------- |
| Data Collection & Pipeline Setup             | ✅ Completed    |
| YOLO + CNN Object Detection                  | ✅ Completed    |
| SUMO Simulation Integration                  | ✅ Completed    |
| Reinforcement Learning (Single Intersection) | 🔄 In Progress |
| Multi-Intersection Deployment                | 🔜 Upcoming    |
| Real-World Pilot + Municipal Integration     | 🎯 Future Goal |



🧭 Future Enhancements

Multi-intersection traffic optimization

Integration with edge devices for real-time deployment

Richer dashboard for traffic analytics

Pilot testing with traffic-authority stakeholders

More advanced RL frameworks beyond D3QN

👥 Ideal Users

Smart-city researchers

Transportation engineers

AI and ML developers

Students working on mobility + IoT + RL projects

📬 Contact

For collaboration or questions, feel free to connect or open an issue here on GitHub.
