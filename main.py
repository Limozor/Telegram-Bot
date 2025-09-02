from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio

bot = Bot(token="")
dp = Dispatcher()


menu_items = {
    "напитки": {
        "Горячий шоколад": "Густой и ароматный напиток на основе какао с молоком, подается горячим",
        "Апельсиновый сок": "Натуральный свежевыжатый сок апельсина, охлажденный",
        "Мохито": "Освежающий газированный коктейль с лаймом, мятой и льдом",
        "Чай": "Ароматный черный или зеленый чай на выбор, подается с лимоном или медом",
        "Кофе": "Насыщенный кофе из зерен арабики, с возможностью добавления молока или сиропа"
    },
    "горячие блюда": {
    "Пицца": "Настоящая итальянская пицца 30см на тонком тесте с хрустящей корочкой. На выбор: классическая Маргарита, острая Диабло, сырная Четыре сезона или авторская с трюфелями",
    "Паста": "Идеально приготовленные спагетти аль денте с соусами: сливочный карбонара с панчеттой, нежный том-ям с морепродуктами, вегетарианское примавера",
    "Стейк": "Премиальная мраморная говядина рибай (прожарка на выбор) с соусом демиглас, запечёнными молодыми овощами и картофельным гратеном",
    "Запечённые роллы": "Горячие рулетины с хрустящей сырной корочкой: с лососем и сливочным сыром, острые с тунцом и спайс-соусом, вегетарианские с авокадо",
    "Рамен": "Аутентичный японский суп с насыщенным костным бульоном, свиной грудинкой чашу, лапшой, яйцом пашот и ростками бамбука. Варианты: мисо, шио или острый танцумен",
    "Суп-пюре": "Нежные крем-супы на выбор: грибной с трюфельным маслом, тыквенный с кокосовым молоком, томатный с базиликом. Подаются с гренками из чиабатты"
    },
    "закуски": {
    "Картофель фри": "Золотистая картошка с двойной обжаркой в масле фритюра, подаётся с тремя видами соусов на выбор: фирменный кетчуп, сливочно-чесночный и острый барбекю",
    "Наггетсы": "Отборное куриное филе в воздушной хрустящей панировке, обжаренное до золотистой корочки. Подаются с пикантным соусом ранч и свежим сельдереем",
    "Сырные нарезки": "Ассорти из премиальных сыров: выдержанный чеддер, нежная гауда и сливочная моцарелла. Дополнены грецкими орехами, мёдом и виноградом",
    "Мясные нарезки": "Ароматное ассорти из вяленой говядины, нежной брезаолы и пикантного прошутто. Подаётся с оливками, корнишонами и горчицей",
    "Тарталетки с курицей": "Хрустящие корзиночки из песочного теста с начинкой из нежной куриной грудки, сливочного сыра, шпината и пряных трав"
    },
"салаты": {
        "Легкий салат": "Свежая смесь рукколы, шпината и латука с помидорами черри, огурцами и лёгкой заправкой из оливкового масла с лимонным соком",
        "Цезарь": "Классический салат с хрустящими листьями айсберга, куриной грудкой-гриль, черри, пармезаном, домашними гренками и фирменным соусом Цезарь",
        "Греческий": "Ароматный микс из свежих огурцов, помидоров, сладкого перца, красного лука, маслин и кусочков феты с оливковым маслом и орегано",
        "Оливье": "Нежный салат с отварным картофелем, морковью, яйцами, зелёным горошком, хрустящими огурчиками и сливочным майонезом"}}


class OrderMenu(StatesGroup):
    category = State()
    food = State()

@dp.message(Command("start"))
async  def start_message(message: Message):
    await  message.answer("""....(⊙_⊙;)
    Добро пожаловать
    выберите команду для использования нужного сервиса""")
    await message.answer("""Доступные команды:
    /start - выбор другого сервиса
    /menu - меню кафе
    /ts - техническая поддержка
    /id - id
    """)

@dp.message(Command("id"))
async def any_message(message:Message):
    await message.answer(message.from_user.full_name)
    await message.answer(str(message.from_user.id))


@dp.message(Command("ts"))
async def ts_message(message: Message):
    await message.answer("""Для получения технической поддержки обратитесь сюда:
    @Limozor""")

@dp.message(Command("menu"))
async def cmd_menu(message: types.Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    for category in menu_items:
        builder.add(types.KeyboardButton(text=category))
    builder.adjust(2)
    await message.answer("Добро пожаловать в наше мини кафе ниже вы можете посмотреть наше меню выберите категорию:",
                         reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(OrderMenu.category)

@dp.message(OrderMenu.category)
async def select_category(message: types.Message, state: FSMContext):
    if message.text not in menu_items:
        return

    builder = ReplyKeyboardBuilder()
    for item in menu_items[message.text]:
        builder.add(types.KeyboardButton(text=item))
    builder.adjust(2)

    await message.answer("Выберите блюдо:", reply_markup=builder.as_markup(resize_keyboard=True))
    await state.update_data(category=message.text)
    await state.set_state(OrderMenu.food)


@dp.message(OrderMenu.food)
async def select_food(message: types.Message, state: FSMContext):
    data = await state.get_data()
    category = data["category"]

    if message.text in menu_items[category]:
        description = menu_items[category][message.text]
        await message.answer(
            f"{message.text}\n{description}",
            reply_markup=types.ReplyKeyboardRemove()
        )

    await state.clear()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        print("Бот завершил работу")
