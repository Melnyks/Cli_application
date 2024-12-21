# NewsAPI Command Line Application Project 🗂️

## Overview 🌟

This project is a command-line application built with Python that uses the NewsAPI to fetch and display news articles. It allows users to search for articles using keywords, view trending news, explore articles by category or source. The application is containerized with Docker for ease of deployment.

## Project Structure 📂

```
news_api_command_line_project/
├── AUTHORS                       # 📝 Lists project contributors
├── main.py                       # 🚀 The main CLI script to interact with the NewsAPI 
├── requirements.txt              # 📦 Lists the required Python dependencies
├── compose.yml                   # 🗂️ Configures multi-container Docker setups
├── Dockerfile                    # 🌟 Builds a Docker image to run the application
├── LICENSE                       # ⚙️ Specifies the project's licensing terms
└── README.md                     # 📖 Contains the project overview and usage guide
```

## Command 🛠️

  - **python main.py help** - display all available subcommands/options
  - **python main.py list** - display available types of news data
  - **python main.py trend [OPTIONS]** - Get trending news
  - **python main.py search [OPTIONS]** - Search news articles by keyword
  - **python main.py category [OPTIONS]** - Search news articles by category
  - **python main.py source [OPTIONS]** - Search news articles by source

## Setup ⚙️

1. **Clone the Repository:**
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create and Activate a Virtual Environment:**
   ```sh
   python -m venv venv
   source venv\Scripts\activate  # On Linux use `venv/bin/activate`
   ```

3. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   - View all commands 
   ```sh
   python main.py help
   python main.py --help
   ```
   - Run any of these subcommands 
   ```sh
   python main.py trend [OPTIONS]
   python main.py search [OPTIONS]
   python main.py category [OPTIONS]
   python main.py source [OPTIONS]
   ```
   - Example: Using the `search` Subcommand
   Search for articles about "automated driving systems" and display detailed information
   ```sh
   python main.py search "automated driving systems" -n 1
   ```
   ```sh
   Example Output:
   Title: Emergency Vehicle Lights Can Screw Up a Car's Automated Driving System
   Author: Aarian Marshall
   Description: Newly published research finds that the flashing lights on police cruisers and ambulances can cause “digital epileptic seizures” in image-based automated driving systems, potentially risking wrecks.
   Source: Wired
   Published At: 2024-11-26T12:00:00Z
   URL: https://www.wired.com/story/emergency-vehicle-lights-can-screw-up-a-cars-automated-driving-system/
   ```


## Dependencies 📦

- certifi
- charset-normalizer
- idna
- python-dotenv
- newsapi-python
- requests
- urllib3

## Docker 📝
The command line application is packaged using Docker. You can use Docker Compose to deploy it in a containerized setup. 

1. **Build and Run with Docker Compose:**
   ```sh
   docker-compose up -d
   ```

2. **To enter a Docker container in interactive mode:**
   ```
   docker exec -it <container_name> /bin/bash
   ```   
