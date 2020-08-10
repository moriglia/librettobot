from davtelepot.bot import Bot
import re
#  import dataset
import datetime
import sys
import asyncio
from utils import getmarks, displaymarks

token = input()
db_path = input()
local_host = input()
port = int(input())
laude_plus = 0  # TODO: make this customizable

librettobot = Bot(token=token, database_url=db_path)

markregex = re.compile(
    '\/[a-z]+\s+([a-zA-Zàèéìòù ]+)\s+([0-9]{2})\s*([Ll]?)\s+\
([0-9]+)\s+([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})'
)
deleteregex = re.compile(
    '\/cancella\s+([0-9]+)'
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
        return "Voto non inserito: ricontrolla la data."

    student_exam_id = bot.db['marks'].count(student=student)

    bot.db['marks'].insert(
        dict(
            student_exam_id=student_exam_id,
            student=student,
            exam=exam,
            mark=mark,
            laude=laude,
            credits=credits,
            date=date
        )
    )

    return "Voto inserito!"


@librettobot.command('/lista')
async def vote_list(bot, update, user_record):
    student = user_record['id']

    if not bot.db['marks'].count(student=student):
        return "Non hai ancora registrato nessun esame"

    return await displaymarks(getmarks(bot, student))


@librettobot.command('/cancella')
async def delete_vote(bot, update, user_record):
    if not bot.db['marks'].count(student=user_record['id']):
        return "Non hai nessun esame da cancellare"

    delvote = deleteregex.match(update['text'])

    if delvote is None:
        exam_list = await displaymarks(getmarks(bot, user_record['id']), True)
        return "Quale esame vuoi cancellare?\n" + exam_list + \
            "\n\"/cancella n\" per cancellare l'n-esimo esame della tua lista"

    student_exam_id = int(delvote.group(1)) - 1
    result = bot.db['marks'].delete(
        student=user_record['id'],
        student_exam_id=student_exam_id
    )
    if not result:
        return f"Numero esame non corretto: {int(delvote.group(1))}"

    # Rearrange exam numbering
    for mark in bot.db.query(f"select * from marks \
    where student={user_record['id']} \
    and student_exam_id > {student_exam_id}"):
        bot.db.query(
            f"update marks \
            set student_exam_id = {mark['student_exam_id'] - 1}\
            where id = {mark['id']}"
        )

    exam_list = await displaymarks(getmarks(bot, user_record['id']), True)
    return "Esame cancellato. Nuovo elenco esami:\n" + exam_list


@librettobot.command('/media')
async def media(bot, update, user_record):
    student = user_record['id']
    marks = bot.db['marks'].find(student=student)

    s = 0
    c = 0
    for mark in marks:
        c += mark['credits']
        s += mark['credits'] * (mark['mark'] + mark['laude'] * laude_plus)
        await asyncio.sleep(0)

    if c == 0:
        return "Non hai ancora registrato nessun esame!"

    return f"La tua media è {s/c}"


@librettobot.command('/help')
async def help(bot, update, user_record):
    message = "Comandi disponibili\n"
    message += "/voto\n"
    message += "/media\n"
    message += "/lista\n"
    message += "/cancella\n"
    message += "Chiama un comando senza parametri per sapere come usarlo"

    return message


@librettobot.command('/start')
async def start(bot, update, user_record):
    message = """<b>Benvenuto su Libretto Bot</b>

Breve nota sulla <b>privacy</b>
Utilizzando questo bot accetti che i voti dei tuoi esami \
siano registrati su un server gestito dallo sviluppatore del bot. \
<i>Lo sviluppatore del bot non si assume nessuna responsabilità \
sulla protezione dei dati inseriti</i>, tuttavia si impegna a non pubblicare \
nessun dato se non anonimizzato o aggregato.

In ogni caso puoi mettere su il tuo bot con \
<a href="https://github.com/moriglia/librettobot">il mio codice</a> \
(modificandolo a tuo piacere) e salvare i tuoi dati sul tuo server.

Scopri come usare il bot usando l'/help"""

    return dict(
        text=message,
        parse_mode='HTML',
        disable_web_page_preview=True
    )


status = librettobot.run(
    local_host=local_host,
    port=port
)

sys.exit(status)
