from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from pytube import YouTube
import config
import logging

bot = Bot(token=config.tokin)
dp = Dispatcher(bot, storage=MemoryStorage())
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f"""Здраствуйте, {message.from_user.full_name} Я вам помогу скачать аудио или же видио с юутубе""")

class DowloadAudio(StatesGroup):
    dowload = State()

class DownloadVideo(StatesGroup):
    download = State()

def download(url,type):
    yt = YouTube(url)
    if type == "audio":
        yt.streams.filter(only_audio=True).first().download("audio", f"{yt.title}.mp3")
        return f"{yt.title}.mp3"
    elif type =="video":
        yt.streams.filter(progressive=True,file_extension="mp4").first().download("video", f"{yt.title}.mp4")
        return f"{yt.title}.mp4"

@dp.message_handler(text = ["Аудио", "аудио"])
async def audio(message: types.Message):
    await message.answer("Отправит сылку на видо и я вам атпировит его в видо mp3")
    await DowloadAudio.dowload.set()

@dp.message_handler(text = ["Видио", "video", "video"])
async def video(message: types.Message):
    await message.answer("Отпровит ссылку на видио в юутибе и я вам его отпровлаю")
    await DowloadAudio.dowload.set()

@dp.message_handler(state=DowloadAudio.dowload)
async def dowload_audio(message:types.Message, state : FSMContext):
    try:
        title = download(message.text, "audio")
        audio = open(f"audio/{title}", "rb")
        await message.answer("скачат файыл ожидайте....")
        try:
            await message.answer("Все скачалсь вот держи")
            await bot.send_audio(message.chat.id, audio)
        except:
            await message.answer("Произошла ошибка,попробуйте позже")
        await state.finish()
    except:
        await message.answer("Празашол ошибка,пробит патом")
        await start.finish()
    
    
@dp.message_handler(state=DownloadVideo.download)
async def download_video(message :types.Message,state : FSMContext):
    try:
        title = download(message.text,"video")
        audio = open(f"video/{title}", "rb")
        await message.answer("Скачиваем файл ожидание...")
        try:
            await message.answer("Все скачалось вот держи")
            await bot.send_video(message.chat.id,video)
        except:
            await message.answer("Произошла ошибка,попробуйте позже")
        await state.finish()
    except:
        await message.answer("Неверная ссылка на видео")
        await state.finish()

@dp.message_handler()
async def not_found(message: types.Message):
    await message.reply("Я вас не понял")

executor.start_polling(dp)