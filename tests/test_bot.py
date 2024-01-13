import pytest
from unittest.mock import AsyncMock
from app.handlers import start, game, end
from config import CROSS, ZERO, FREE_SPACE, FINISH_GAME, CONTINUE_GAME


class MockChat:
    def __init__(self, id):
        self.id = id

    async def send_message(self, text):
        self.text = text


class MockMessage:
    def __init__(self, text):
        self.text = text

    async def reply_text(self, text):
        self.reply_text = text


class MockMessageCallBackQuery:
    def __init__(self):
        pass

    async def edit_text(self, text):
        self.text = text

    async def edit_reply_markup(self, reply_markup):
        self.reply_markup = reply_markup


class MockBot:
    async def send_message(self, chat_id, text, reply_markup):
        self.text = text


@pytest.mark.asyncio
async def test_start():
    """test command /start"""
    update_mock = AsyncMock()
    context_mock = AsyncMock()
    context_mock.bot = MockBot()
    update_mock.effective_chat = MockChat(123)
    update_mock.callback_query.message = MockMessageCallBackQuery()
    update_mock.message = MockMessage("/start")
    state = await start(update_mock, context_mock)
    assert state == CONTINUE_GAME
    assert update_mock.message.reply_text == 'Start new game!'
    assert context_mock.bot.text == \
        'X (your) turn! Please, put X to the free place'


@pytest.mark.asyncio
async def test_end():
    """test command /end"""
    update_mock = AsyncMock()
    context_mock = AsyncMock()
    context_mock.bot = MockBot()
    update_mock.effective_chat = MockChat(123)
    update_mock.message = MockMessage("/end")
    state = await end(update_mock, context_mock)
    assert state == -1


@pytest.mark.asyncio
async def test_win_USER1():
    """test case when user win"""
    update_mock = AsyncMock()
    context_mock = AsyncMock()
    context_mock.bot = AsyncMock()
    update_mock.effective_chat = MockChat(123)
    update_mock.callback_query.message = MockMessageCallBackQuery()
    update_mock.callback_query.data = '22'
    context_mock.user_data = {
        'keyboard_state': [
            [CROSS, ZERO, CROSS],
            [ZERO, CROSS, ZERO],
            [FREE_SPACE, FREE_SPACE, FREE_SPACE]
        ]
    }
    state = await game(update_mock, context_mock)
    assert state == FINISH_GAME
    assert update_mock.effective_chat.text == \
        "You win! Use /start to play again"


@pytest.mark.asyncio
async def test_win_USER2():
    """test case when user win"""
    update_mock = AsyncMock()
    context_mock = AsyncMock()
    context_mock.bot = AsyncMock()
    update_mock.effective_chat = MockChat(123)
    update_mock.callback_query.data = '20'
    update_mock.callback_query.message = MockMessageCallBackQuery()
    context_mock.user_data = {
        'keyboard_state': [
            [ZERO, ZERO, CROSS],
            [ZERO, CROSS, ZERO],
            [FREE_SPACE, CROSS, CROSS]
        ]
    }
    state = await game(update_mock, context_mock)
    assert state == FINISH_GAME
    assert update_mock.effective_chat.text == \
        "You win! Use /start to play again"


@pytest.mark.asyncio
async def test_win_AI():
    """test case when ai win"""
    update_mock = AsyncMock()
    context_mock = AsyncMock()
    context_mock.bot = AsyncMock()
    update_mock.effective_chat = MockChat(123)
    update_mock.callback_query.data = '21'
    update_mock.callback_query.message = MockMessageCallBackQuery()
    context_mock.user_data = {
        'keyboard_state': [
            [ZERO, ZERO, CROSS],
            [ZERO, CROSS, ZERO],
            [FREE_SPACE, FREE_SPACE, CROSS]
        ]
    }
    state = await game(update_mock, context_mock)
    assert state == FINISH_GAME
    assert update_mock.effective_chat.text == \
        "AI win! Use /start to play again"


@pytest.mark.asyncio
async def test_bad_user_request():
    """test user wron input"""
    update_mock = AsyncMock()
    context_mock = AsyncMock()
    context_mock.bot = AsyncMock()
    update_mock.effective_chat = MockChat(123)
    update_mock.callback_query.data = '22'
    update_mock.callback_query.message = MockMessageCallBackQuery()
    context_mock.user_data = {
        'keyboard_state': [
            [ZERO, ZERO, CROSS],
            [ZERO, CROSS, ZERO],
            [FREE_SPACE, FREE_SPACE, CROSS]
        ]
    }
    state = await game(update_mock, context_mock)
    assert state == CONTINUE_GAME
    assert update_mock.callback_query.message.text == \
        'You need to select an empty cell'


@pytest.mark.asyncio
async def test_win_DRAW():
    """test draw"""
    update_mock = AsyncMock()
    context_mock = AsyncMock()
    context_mock.bot = AsyncMock()
    update_mock.effective_chat = MockChat(123)
    update_mock.callback_query.data = '21'
    context_mock.user_data = {
        'keyboard_state': [
            [CROSS, ZERO, CROSS],
            [ZERO, CROSS, ZERO],
            [ZERO, FREE_SPACE, ZERO]
        ]
    }
    state = await game(update_mock, context_mock)
    assert state == FINISH_GAME
    assert update_mock.effective_chat.text == "Draw! Use /start to play again"
