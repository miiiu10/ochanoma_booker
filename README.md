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

5. Create Slack app using manifest
    > ## What are manifests? 
    > 
    > Manifests are YAML or JSON-formatted configurations bundles for Slack apps. With a manifest, you can use a UI or an API to create an app with a pre-defined configuration, or adjust the configuration of existing apps.
    > 
    > [Create and configure apps with manifests \| Slack](https://api.slack.com/reference/manifests)

    You can create an app from a manifest (`app_manifest.json`), and it requires only [a few steps](https://api.slack.com/reference/manifests#creating_apps)

6. Run the app
    ```bash
    env=dev python3 app.py  # development
    # env=qa python3 app.py # staging
    # env=prod python3 app.py # production
    ```