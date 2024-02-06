from asyncio import run
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from aiogram.utils.formatting import (Bold, as_list, as_marked_section, as_key_value, HashTag, as_marked_list, Text)
from BD import Base
from Tokens import Tokens


tokens = Tokens()
dp = Dispatcher()
base = Base()

try:
    base.load_test_data()
except:
    pass

print('Start')


async def Codes(message: types.Message, command: CommandObject):
    if message.chat.type == 'group' and message.chat.id == tokens.chat_id and command.args is not None:
        no, *_ = command.args.split(' ')
        if base.exist_error(no):
            er = base.getError(no)
            content = as_list(
                Text(Bold("Код: "), er.no),
                Bold("Описание: ")
            ).as_html() + '\n' + er.description + '\n'
            content += Bold('Возможные решения: ').as_html()+'\n'
            for pr, d in sorted(er.solutions, key=lambda s: s[0]):
                content += f'✅ {d}\n'

        else:
            content = as_marked_list(
                    Text("Не существующий код ошибки: ", Bold(no)),
                    marker="❌ ",
                ).as_html()
        await message.reply(content, parse_mode='HTML')


async def main():
    bot = Bot(token=tokens.Telegram)
    try:
        dp.message.register(Codes, Command('Code'))
        await dp.start_polling(bot)
    finally:
        await bot.close()


if __name__ == "__main__":
    run(main())
