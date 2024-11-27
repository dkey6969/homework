from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot_config import database

dialog_router = Router()

class HomeworkFSM(StatesGroup):
    name = State()
    group = State()
    homework_number = State()
    github_link = State()

@dialog_router.message(Command("stop"))
@dialog_router.message(F.text == "стоп")
async def stop_process(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Процесс остановлен.")

@dialog_router.message(Command("send"))
async def start_homework(message: types.Message, state: FSMContext):
    await state.set_state(HomeworkFSM.name)
    await message.answer("Введите ваше имя:")

@dialog_router.message(HomeworkFSM.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Python 47-01"), types.KeyboardButton(text="Python 47-02")],
            [types.KeyboardButton(text="Python 48-01"), types.KeyboardButton(text="Python 48-02")]
        ],
        resize_keyboard=True
    )
    await state.set_state(HomeworkFSM.group)
    await message.answer("Выберите вашу группу:", reply_markup=kb)

@dialog_router.message(HomeworkFSM.group)
async def process_group(message: types.Message, state: FSMContext):
    await state.update_data(group=message.text)
    await state.set_state(HomeworkFSM.homework_number)
    await message.answer("Введите номер домашнего задания (от 1 до 8):", reply_markup=types.ReplyKeyboardRemove())

@dialog_router.message(HomeworkFSM.homework_number)
async def process_homework_number(message: types.Message, state: FSMContext):
    homework_number = message.text
    if not homework_number.isdigit():
        await message.answer("Введите номер задания в виде числа от 1 до 8!")
        return

    homework_number = int(homework_number)
    if homework_number < 1 or homework_number > 8:
        await message.answer("Введите номер задания от 1 до 8!")
        return

    await state.update_data(homework_number=homework_number)
    await state.set_state(HomeworkFSM.github_link)
    await message.answer("Введите ссылку на ваш репозиторий (должна начинаться с https://github.com):")

@dialog_router.message(HomeworkFSM.github_link)
async def process_github_link(message: types.Message, state: FSMContext):
    github_link = message.text
    if not github_link.startswith("https://github.com"):
        await message.answer("Ссылка должна начинаться с https://github.com. Попробуйте снова.")
        return

    await state.update_data(github_link=github_link)
    data = await state.get_data()

    database.execute(
        query="""
        INSERT INTO homeworks (name, group, homework_number, github_link)
        VALUES (?, ?, ?, ?)
        """,
        params=(data["name"], data["group"], data["homework_number"], data["github_link"])
    )

    await message.answer(
        f"✅ Домашнее задание отправлено!\n\n"
        f"Имя: {data['name']}\n"
        f"Группа: {data['group']}\n"
        f"Номер задания: {data['homework_number']}\n"
        f"Ссылка: {data['github_link']}"
    )
    await state.clear()