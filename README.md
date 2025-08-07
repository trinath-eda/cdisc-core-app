# CDISC CORE Validator – Web GUI

**A lightweight, Streamlit-based web application for validating SDTM datasets using the official CDISC CORE rules engine.**  


## 🚀 Why This Project?

Validating SDTM datasets using CDISC CORE is critical — but the CLI interface can be a barrier for non-programmers or teams needing a quick review cycle.  
This GUI wrapper eliminates that friction by offering:

- A drag-and-drop upload interface
- Click-to-run validation with selectable SDTMIG version/output format
- One-click cache updates via CDISC Library API
- Clean result downloads
- Seamless integration with the official `cdisc-rules-engine`

## 🔍 Features

- 📤 Upload SDTM datasets (XPT or JSON format)
- 📚 Select SDTMIG standard and version
- 📄 Choose output format: XLSX or JSON
- ✅ Validate against CDISC CORE engine
- 🔄 Update rules cache using your CDISC API key
- 🧹 Auto-cleanup of old files (uploads/results older than 7 days)
- 🖥️ Simple Streamlit UI – run with a single command


## 📦 Project Structure
```
cdisc-core-app/
│
├── app.py # Main Streamlit app
├── .env # Stores CDISC_API_KEY
├── .gitignore # Best practice exclusions
├── requirements.txt # Combined dependencies
├── LICENSE # MIT License
│
├── uploads/ # Temporary uploaded files
├── results/ # Validation result outputs
├── cdisc-rules-engine/ # Official CDISC CORE repo clone
├── venv/ # (Local virtual environment)
```

```yaml
> 📝 Note: `uploads/` and `results/` are ignored via `.gitignore`.
```
---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/trinath-eda/cdisc-core-app.git
cd cdisc-core-app
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
``` bash
pip install -r requirements.txt
```

### 4. Add your .env file
Create a .env file in the root directory:

```
CDISC_API_KEY=your_cdisc_library_api_key
```

## ▶️ Running the App
```
streamlit run app.py
```

Your default browser will open the app at http://localhost:8501.

## 🧪 How It Works
1. Upload a Dataset (XPT or Dataset-JSON).
2. Choose standard (sdtmig), version (3-4, 3-3, etc.), and output format (XLSX or JSON).
3. Click Validate to run the CDISC CORE rules engine.
4. Download the generated report from the app.
5. Use the 🔄 Update Cache button to fetch the latest rules from CDISC Library using your API key.

## 🌱 Planned Enhancements
1. ✅ Multi-file dataset validation
2. 🧬 ADaM rules integration
3. 🐳 Docker container support
4. 🔐 Authentication & user role support
5. 📝 Live validation logs and job queueing
6. 📎 Integration with Define-XML, Dataset-JSON Viewer

## 🛠 Troubleshooting
1. 🔑 Missing API Key: Make sure .env is present with a valid CDISC_API_KEY.
2. 🐍 Python Version: Ensure you're using Python 3.10+.
3. ❌ Validation Fails: Check logs shown in the Streamlit console or inside the app.

## 🧾 License
This project is licensed under the MIT License.

## 📫 Contact
For questions, enhancements, or support, feel free to raise an issue or contact the maintainer.