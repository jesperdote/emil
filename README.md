# Gmail Email Monitor

A simple, containerized web application that monitors unread emails from your Gmail account and displays their subject and age in a clean web UI.

## Features

- Fetches unread emails from a specified Gmail account.
- Displays the email subject and its age (e.g., "5m ago", "2h 10m ago").
- Web interface automatically refreshes every 60 seconds.
- Fully containerized with Docker and Docker Compose for easy setup and portability.
- Securely handles authentication using the official Google API client.

## Prerequisites

Before you begin, you will need the following:

1.  **Docker and Docker Compose:** Ensure they are installed on your system.
2.  **Google Cloud Project:** You need to set up a project to get API credentials.
    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - Create a new project.
    - Enable the **Gmail API** for your project.
    - Create an **OAuth 2.0 Client ID** for a **Desktop app**.
    - Download the credentials JSON file.

## Setup

1.  **Clone the Repository:**
    ```bash
    git clone <your-repo-url>
    cd emil
    ```

2.  **Add Credentials:**
    - Rename the credentials file you downloaded from Google to `credentials.json`.
    - Place this `credentials.json` file in the root of the project directory (i.e., inside the `emil/` folder you just cloned).

## How to Run

The entire application is managed by a simple shell script.

1.  **Make the script executable (only needs to be done once):**
    ```bash
    chmod +x run.sh
    ```

2.  **Start the application:**
    ```bash
    ./run.sh
    ```
    This command will build the Docker image and start the container in the background.

3.  **First-Time Authentication:**
    The very first time you run the app, you must authorize it to access your Gmail account.
    - View the application logs: `docker-compose logs -f`
    - Copy the URL that starts with `https://accounts.google.com/o/oauth2/auth...`
    - Paste this URL into your web browser, sign in, and grant the requested permissions.
    - Once authorized, a `token.json` file will be created in your project directory, and the application will start fetching emails.

4.  **View the Monitor:**
    Open your browser and navigate to **http://127.0.0.1:5001**.

## How to Stop

To stop the application and remove the container, run:

```bash
docker-compose down
```# emil
# emil
