# librettobot

## Simple usage
1. Make a `config.txt` file (it is recommendable in a `data` folder),
with the following content, one item per line:
  - the token of the bot
  - the sqlite database path
  - the address to bind
  - the port

  ```
  123456789:abcdefghi...helloworld
  data/botdatabase.db
  127.0.0.1
  5555
  ```
  Remember not to track the configuration file or folder.
  Since every programmer may choose a different name or location, I suggest
  to add it to `.git/info/exclude` rather than to `.gitignore`.

2. Install required modules

  ```bash
  make install
  ```

3. Run the bot
  - Specify `config=...` if the configuration file is not `data/config.txt`.
  - Specify the `run` target if you added further targets before `run`
  in the `makefile`

  ```bash
  make [config=path/to/config.txt] [run]
  ```

## Usage with docker
1. Create a `.env` file with the same content as above, but with
the following format:
```
TELEGRAM_BOT_TOKEN=123456789:abcdefghi...helloworld
DB_PATH=data/botdatabase.db
LOCALHOST_IP=127.0.0.1
PORT=5555
```
If different from the default `.env`, add the filename to `.git/info/exclude`.

2. Build the docker container
```
docker build -t librettobot:myversion librettobot
```
3. Run the container specifying the environment file:
```
docker run --env-file <path/to/.env> librettobot:myversion
```
