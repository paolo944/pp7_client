# Web client for ProPresenter

Web client for ProPresenter 7 with important informations like clock and Stage live messages.

To run the web app, the server (this app) must be running on the same network as the ProPresenter app.
The server is not required to be on the same machin as the ProPresenter app.

## ⚠️ **IMPORTANT: PLEASE READ CAREFULLY** ⚠️
This app is still under developpement and can very likely crash.
Please don't use it in critical situations. Only in training and
just for testing for now.
If you have any question ou improvemnts, feel free to sumbit
an issue on github or a pull request and i will to try to
answer fastly or review your pull requests.

## Requirements
- python3
- pip3
- git

## Installation
Open a terminal and run the following commands
```bash
git clone https://github.com/paolo944/pp7_client.git
cd pp7_client
pip3 install -r requirements.txt
```
## Configuration
You have to first enable network on ProPresenter by going into Settings->Network then Enable Network.
The ip adress should appear should under. Write down also the port number of the ProPresenter app.
Make sure that your machine is visible on your local network, so that other clients like your phone or the server
if it's not on the same machine as the ProPresenter app could communicate with it's API.

After you have written down the ip adress and made sure the ProPresenter computer is visible on the local 
network, go in the file pp7_client/info.json and add this line
```json
{
  "url": "http://{ip adress}:{port}/v1/"
}
```
Replace  {ip adress} by the ip adress of the machine on which ProPresenter is running and {port} by the port number 
of ProPresenter.

If the server runs on the same machien as the ProPresenter app, just replace {ip adress} by 127.0.0.1 .

## Running the app
To run the app, launch the script app.py.

On Mac-GNU/Linux:
```bash
# Make sure to be located in the project directory
python3 app.py
```

On Windows PowerShell:
```
python app.py
```

A url wil appear in the terminal, go to it on any client which is on the same network to get the main client.

If you want the subtitles page which updates automaticly, go to the url/subtitles .

The subtitles are well suited for OBS if you create a scene using a web brower.

## ⚠️ **DISCLAIMER** ⚠️
The subtitles format is suited for my church's specific formats, so will very probably have to adapt it to your format.
