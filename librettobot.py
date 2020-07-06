from davtelepot.bot import Bot
import re
import dataset
import datetime
import sys

token = input()
db_path = input()
local_host = input()
port = int(input())

librettobot = Bot(token=token, database_url=db_path)
markregex = re.compile(
    '\/[a-z]+ ([a-zA-Z ]+)([0-9]{2})\s*(L?)\s+\
([0-9]+)\s+([0-9]{4})-([0-9]{2})-([0-9]{2})'
)


@librettobot.command("/voto")
async def voto(bot, update, user_record):
    student = user_record['id']

    m = markregex.match(update['text'])
    if m is None:
        return "Command format: `/voto <Nome esame> \
<voto><[L]> <CFU> <yyyy-mm-dd>`"

    exam = m.group(1).strip()

    mark = int(m.group(2))
    if mark < 18 or mark > 30:
        return "Il voto inserito non è valido!"

    laude = m.group(3)
    if laude and mark != 30:
        return "La lode richiede che il voto inserito sia 30"
    laude = laude != ''

    credits = int(m.group(4))
    if credits <= 0:
        return "Il valore inserito per i crediti non è valido"

    year = int(m.group(5))
    month = int(m.group(6))
    day = int(m.group(7))
    try:
        date = datetime.date(year, month, day)
    except ValueError as ve:
        return "Date format is not correct"

    with dataset.connect(f"sqlite:///{db_path}") as db:
        marks_table = db['marks']
        marks_table.insert(
            dict(
                student=student,
                exam=exam,
                mark=mark,
                laude=laude,
                credits=credits,
                date=date
            )
        )

    return "Voto inserito!"

status = librettobot.run(
    local_host=local_host,
    port=port
)

sys.exit(status)
