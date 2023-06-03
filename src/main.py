
# мб сделать кнопки назад
# добавить функцию (возможно вы имели в виду?)
# первый кейборд - рега или ответы на часто задаваемые вопросы?
# доп. продукты (помощь с регой, помощь с аккредитацией и проч.)

# прежде чем что-то сделать, чат-бот должен понять, аккредитован ли пользователь

from vkbottle.bot import Bot, Message

from vkbottle.api import API
from vkbottle import    Keyboard, \
                        KeyboardButtonColor, \
                        Text, OpenLink,      \
                        EMPTY_KEYBOARD, \
                        template_gen, TemplateElement, \
                        BaseStateGroup, CtxStorage

                        
import random
import time

from config import group_token, user_token

api = API(user_token)
bot = Bot(group_token)

# ctx = CtxStorage()

green = KeyboardButtonColor.POSITIVE
red   = KeyboardButtonColor.NEGATIVE
blue  = KeyboardButtonColor.PRIMARY

class RegData(BaseStateGroup):
    SKUS        = 'skus'
    SIZE        = 'size'
    SHIP_DATA   = 'ship_data'
    FINISH      = 'promo'
    PROMO_INPUT = 'promo'
    PROMO_DATA  = 'promocode'


# beginning
greetings = ['Привет', 'привет', 'Начать', 'начать', 'Здравствуйте', 'здравствуйте', 'Здравствуйте!', 'здравствуйте!', 'Здравствуйте! Меня заинтересовал этот товар.', '/start']
@bot.on.private_message(text=greetings)
@bot.on.private_message(payload={'cmd' : 'start'})
async def start(message: Message):
    user = await bot.api.users.get(message.from_id)

    keyboard = Keyboard(one_time=True)

    keyboard.add(Text('Я поставщик/заказчик', {'cmd' : 'postavshik_or_zakazchik'}), color=blue)
    keyboard.row()
    keyboard.add(Text('О нас', {'cmd' : 'about_us'}), color=blue)
    keyboard.row()
    keyboard.add(OpenLink('https://cpp.roseltorg.ru/faq?_ga=2.250862337.649373056.1685777316-324402738.1685777316', 'Рубрика вопрос-ответ'), color=blue)

    # keyboard.add(Text("/help", {'cmd' : 'help'}), color=blue)

    await message.answer("Приветствую, {}!".format(user[0].first_name))
    await message.answer('Я чат-бот помощник крупнейшей федеральной платформы ведения торгов РОСЭЛТОРГ. Чем могу помочь?')
    await message.answer('Выберите нужное:', keyboard=keyboard)


@bot.on.private_message(payload={'cmd' : 'about_us'})
async def about_us_handler(message: Message):
    keyboard = Keyboard(one_time=True).add(Text('Вернуться назад', {'cmd' : 'start'}), color=red)
    await message.answer("""
Торговая площадка «Росэлторг» (АО «Единая электронная торговая площадка») — это крупнейший федеральный оператор электронных торгов для государственных заказчиков (44-ФЗ), госкомпаний (223-ФЗ) и коммерческих предприятий.

Клиентами «Росэлторг» являются 280 тыс. заказчиков и 680 тыс. поставщиков, а суммарный объем проведенных торгов превышает 38 трлн рублей.

История развития компании началась в 2006 г., когда в России начали проводиться первые электронные аукционы по размещению госзаказов Правительства Москвы, субъектов РФ и межрегиональных компаний группы «Связьинвест» и холдинга АФК «Система».

Официальной датой открытия АО «ЕЭТП» считается 19 мая 2009 г.

Акционеры «Единой электронной торговой площадки»:

• Правительство города Москвы — высший орган исполнительной власти в г. Москве, возглавляемый мэром Москвы (51,82%),

• Банк ВТБ — второй по величине активов банк России и первый по размеру уставного капитала (48,18%).

Генеральный директор — Кашутин Андрей Вячеславович.
   """, keyboard=keyboard) 


@bot.on.private_message(payload={'cmd' : 'postavshik_or_zakazchik'})
async def postavshik_or_pokupatel(message: Message):
    keyboard = Keyboard(one_time=True).add(Text('Заказчик', {'cmd' : 'zakazchik'}), color=blue)
    keyboard.add(Text('Поставщик', {'cmd' : 'postavshik'}), color=blue)

    await message.answer('Кто вы?', keyboard=keyboard)




@bot.on.private_message(payload={'cmd' : 'zakazchik'})
async def client_is_zakazchik(message: Message):
    keyboard_1 = Keyboard().add(Text('Перейти', {'cmd' : 'zakazchik-44-fz'}),   color=blue)
    keyboard_2 = Keyboard().add(Text('Перейти', {'cmd' : 'zakazchik-223-fz'}),  color=blue)
    keyboard_3 = Keyboard().add(Text('Перейти', {'cmd' : 'zakazchik-rb'}),      color=blue)
    keyboard_4 = Keyboard().add(Text('Перейти', {'cmd' : 'zakazchik-fkr'}),     color=blue)
    keyboard_5 = Keyboard().add(Text('Перейти', {'cmd' : 'zakazchik-imtorgi'}), color=blue)

    keyboard = Keyboard(inline=True).add(OpenLink('https://google.com', 'FAQ'), color=blue)
    
    carousel = template_gen(
        TemplateElement(
            title        = '44-ФЗ',
            description  = 'Описание',
            buttons      = keyboard_1.get_json()
        ),
        TemplateElement(
            title        = '223-ФЗ',
            description  = 'Описание',
            buttons      = keyboard_2.get_json()
        ),
        TemplateElement(
            title        = 'РБ',
            description  = 'Описание',
            buttons      = keyboard_3.get_json()
        ),
        TemplateElement(
            title        = 'ФКР',
            description  = 'Описание',
            buttons      = keyboard_4.get_json()
        ),
        TemplateElement(
            title        = 'Имущественные торги',
            description  = 'Описание',
            buttons      = keyboard_5.get_json()
        )
    )

    await message.answer('Отлично!\nВыберите нужный сценарий:', template=carousel)
    await message.answer('Нужна помощь?', keyboard=keyboard)


@bot.on.private_message(payload={'cmd' : 'zakazchik-44-fz'})
async def scenario_44_fz_handler(message: Message):
    await message.answer('работает!')

@bot.on.private_message(payload={'cmd' : 'zakazchik-223-fz'})
async def scenario_223_fz_handler(message: Message):
    await message.answer('работает!')

@bot.on.private_message(payload={'cmd' : 'zakazchik-rb'})
async def scenario_rb_handler(message: Message):
    await message.answer('работает!')

@bot.on.private_message(payload={'cmd' : 'zakazchik-fkr'})
async def scenario_fkr_handler(message: Message):
    await message.answer('работает!')

@bot.on.private_message(payload={'cmd' : 'zakazchik-imtorgi'})
async def scenario_imtorgi_handler(message: Message):
    await message.answer('работает!')

@bot.on.private_message(payload={'cmd' : 'postavshik'})
async def client_is_postavshik(message: Message):
    keyboard_1 = Keyboard().add(Text('Перейти', {'cmd' : 'postavshik-44-fz'}),   color=blue)
    keyboard_2 = Keyboard().add(Text('Перейти', {'cmd' : 'postavshik-223-fz'}),  color=blue)
    keyboard_3 = Keyboard().add(Text('Перейти', {'cmd' : 'postavshik-rb'}),      color=blue)
    keyboard_4 = Keyboard().add(Text('Перейти', {'cmd' : 'postavshik-fkr'}),     color=blue)
    keyboard_5 = Keyboard().add(Text('Перейти', {'cmd' : 'postavshik-imtorgi'}), color=blue)

    keyboard = Keyboard(inline=True).add(OpenLink('https://google.com', 'FAQ'), color=blue)
    
    carousel = template_gen(
        TemplateElement(
            title        = '44-ФЗ',
            description  = 'Описание',
            buttons      = keyboard_1.get_json()
        ),
        TemplateElement(
            title        = '223-ФЗ',
            description  = 'Описание',
            buttons      = keyboard_2.get_json()
        ),
        TemplateElement(
            title        = 'РБ',
            description  = 'Описание',
            buttons      = keyboard_3.get_json()
        ),
        TemplateElement(
            title        = 'ФКР',
            description  = 'Описание',
            buttons      = keyboard_4.get_json()
        ),
        TemplateElement(
            title        = 'Имущественные торги',
            description  = 'Описание',
            buttons      = keyboard_5.get_json()
        )
    )

    await message.answer('Отлично!\nВыберите нужный сценарий:', template=carousel)
    await message.answer('Нужна помощь?', keyboard=keyboard)


@bot.on.private_message(payload={'cmd' : 'postavshik-44-fz'})
async def scenario_44_fz_handler(message: Message):
    await message.answer('работает!')

@bot.on.private_message(payload={'cmd' : 'postavshik-223-fz'})
async def scenario_223_fz_handler(message: Message):
    await message.answer('работает!')

@bot.on.private_message(payload={'cmd' : 'postavshik-rb'})
async def scenario_rb_handler(message: Message):
    await message.answer('работает!')

@bot.on.private_message(payload={'cmd' : 'postavshik-fkr'})
async def scenario_fkr_handler(message: Message):
    await message.answer('работает!')

@bot.on.private_message(payload={'cmd' : 'postavshik-imtorgi'})
async def scenario_imtorgi_handler(message: Message):
    await message.answer('работает!')
bot.run_forever()