# LLAMA 2 AI Unofficial API

* This API uses Playwright and Chromium to automate a browser and parse responses automatically.
* It is an unofficial API and is intended for development and educational purposes only.

# How to install

* Install the requirements

```
pip install -r requirements.txt
```

* If you are installing Playwright for the first time, please run the below command as well.

```
python -m playwright install
```

* Now run the server

```
python server.py
```

* The server runs at port `5041`. If you want to change, you can change it in server.py


# API Documentation

* There is a single end-point only. It is available at `/chat`

```sh
curl -XGET http://localhost:5041/chat?q=What%20is%20the%20scientific%20name%20for%20llamas?
```

# Quick Start

* There is a `runner.py` provided which will automate the asking of any questions you have in `questions.json`.
* It will automatically propagate `answers.json` with your question answer combination.
* Simply ensure that `server.py` is running and active at port `5041`, then execute `runner.py`.


# Updates

* [September 5, 2023]: Initial release


# Credit

This project is by Sean Henry Lewis.
