import asyncio


def getmarks(bot, uid):
    student = uid
    return bot.db['marks'].find(student=student)


async def displaymarks(marks, numbering=False):
    message = "<pre>"

    for mark in marks:
        if numbering:
            message += f"{mark['student_exam_id'] + 1})\t"
        L = 'L' if mark['laude'] else ''
        message += f"{mark['mark']}{L}\t{mark['exam']} ({mark['credits']})\n"
        await asyncio.sleep(0)

    message += "</pre>"

    return message
