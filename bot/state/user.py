from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    language = State()
    fullname = State()
    position = State()
    phone = State()


class ApplicationState(StatesGroup):
    category = State()
    comment = State()
    document = State()


class UserState(StatesGroup):
    settings = State()
    waiting_for_message = State()
