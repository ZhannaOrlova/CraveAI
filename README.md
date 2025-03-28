# CraveAI Content Finder

CraveAI Content Finder is a Streamlit-based application that generates AI-driven search suggestions and YouTube video recommendations based on your input. Save your liked content in a sidebar for quick access.

## Features

- **AI Search Suggestions:**  
  Generate specific search queries with the help of the DeepSeek API.

- **Video Recommendations:**  
  Get recommended YouTube videos based on your search query.

- **Content Management:**  
  Like or dislike suggestions and videos. Liked content appears in the sidebar, and you can remove items as needed.

![Application Screenshot](Application.png)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure enviromental variables**
```bash
[api_keys]
DEEPSEEK_API_KEY = "your_deepseek_api_key"
YOUTUBE_API_KEY = "your_youtube_api_key"
```

5. **Run the app**
```bash
streamlit run app.py
```


