# TOC Project 2017

TOC Project 2017

A telegram bot based on a finite state machine

## Setup

### Prerequisite

* Python 3

#### Install Dependency

use `make` to install dependency

or

```sh
pip3 install -r requirements.txt
```

* pygraphviz (For visualizing Finite State Machine)
    * [Setup pygraphviz on Ubuntu](http://www.jianshu.com/p/a3da7ecc5303)

### Secret Data

`API_TOKEN` and `WEBHOOK_URL` in app.py **MUST** be set to proper values.
Otherwise, you might not be able to run your code.

## Server

use `make run` to start `ngrok` and `app.py`

after run `./ngrok http 5000` in another terminal

the original terminal will `sleep 5` (5 sec) for waiting the connection

if 5 sec is not enough, please increase the sleeping time in `Makefile` 

`app.py` can automatically parse `http://127.0.0.1:4040` and set `WEBHOOK_URL`

## Client

Add @Wesleyi_Talent_bot (https://telegram.me/Wesleyi_Talent_bot)

push `start` to talk with chat bot
<img src="./img/screenshot/a.png" width="432" height="768">

you can lookup 當日匯率, 國際指數, 當日行情 by following the instruction (case insensitive)


### e.g. 1
enter `A` for 當日匯率

<img src="./img/screenshot/b.png" width="432" height="768">


### e.g. 2
enter `Q` for 離開

<img src="./img/screenshot/c.png" width="432" height="768">


### e.g. 3
enter `error`+error message for 錯誤回報

<img src="./img/screenshot/d.png" width="432" height="768">

## Finite State Machine
![fsm](./img/show-fsm.png)

## Author
[Lee-W](https://github.com/Lee-W)
