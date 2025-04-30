# SysMal: Malware Behavior Analysis with LSTM and CAPEv2
**SysMal** (Systematic Malware Analysis) is a project that aims to analyze and classify malware based on its dynamic behavior using the Long Short-Term Memory (LSTM) algorithm. The dataset is obtained from the CAPEv2 framework, which records malware runtime activities such as API calls. The project also features a website interface to make it easier for users to upload files and view analysis results in real-time.


## 🔍 Key Features
- Malware dynamic behavior extraction using [CAPEv2](https://github.com/kevoreilly/CAPEv2)
- Log preprocessing into numeric sequences for LSTM input
- LSTM model for behavior-based malware classification
- Interactive web interface (built with FastAPI + Streamlit(frontend))
- Classification results visualization 
- File upload support for automated analysis
