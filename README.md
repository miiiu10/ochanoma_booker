# Ochanoma Booker
![kirin](https://user-images.githubusercontent.com/98066319/197503841-260f7b0f-f6e1-45f8-9e44-e05778bf8ac3.gif)


# Setup & Usage

1. Create and activate your virtual environment
    ```bash
    conda create -n [yourenvname] python=3.9
    source activate [yourenvname]
    ```

2. Clone the repository
    ```bash
    git clone https://github.com/Kitsuya0828/Ochanoma-Booker.git
    cd Ochanoma-Booker
    ```

3. Install Python packages
    ```bash
    pip install -r requirements.txt
    ```

4. Place the following files in the project root
    |  file name  |  contents  |
    | ---- | ---- |
    |  `.env.dev`  |  Slack app tokens for the development environment  |
    |  `.env.qa`  |  Slack app tokens for the staging environment (optional)  |
    |  `.env.prod`  |  Slack app tokens for the production environment  |
    |  `.env`  |  scopes and ID for Google Calendar API  |
    |  `google_calendar_key.json`  |  keys for Google Calendar API  |
    |  `iiclab_member.csv`  |  List of Slack members' names and IDs  |

5. Configure the Slack app
    > ### [App Manifest](https://api.slack.com/reference/manifests)
    >
    > The manifest below captures your app as it’s currently configured. You can make any changes to your basic info, settings, or feature configurations right here.

    Create a new slack app at [Slack API](https://api.slack.com/) and configure it like in `app_manifest.json`. Then, install the app to your workspace.

6. Run the app
    ```bash
    env=dev python3 app.py  # development
    # env=qa python3 app.py # staging
    # env=prod python3 app.py # production
    ```