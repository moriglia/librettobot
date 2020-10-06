# librettobot

# Usage
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
