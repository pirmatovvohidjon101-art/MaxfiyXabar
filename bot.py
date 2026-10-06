import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# ========== SOZLAMALAR ==========
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
# ================================

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class Form(StatesGroup):
    step = State()

TEXTS = {
    1: (
        "Salom…\n"
        "Ba’zan taqdir odamlarni uzoq yillarga ajratib, keyin yana bir lahzaga bir-biriga yaqinlashtiradi.\n"
        "Men bugun shunday bir his haqida gapirmoqchiman."
    ),
    2: (
        "Salom Mubina!  Biz qachonlardir birga o‘qiganmiz.\n"
        "Lekin hech qachon dildan suhbatlashmaganmiz.\n"
        "Shunga qaramay, siz mening xotiramda nima uchundir o‘chmagan ekansiz —\n"
        "xuddi eski kitobning sahifalarida saqlanib qolgan bir jumla kabi."
    ),
    3: (
        "Yillar o‘tdi.\n"
        "Hayot o‘z yo‘liga ketdi.\n"
        "Va 2–3 oy oldin avtobusda sizni bir marta ko‘rib qoldim.Deyarli o'zgarmagansiz, o'sha o'sha chiroylisz.\n"
        "Siz esa deyarli meni ko‘rmadingiz.\n"
        "Lekin o‘sha qisqa lahzaning o‘zi yetarli edi —\n"
        "yuragimda g‘alati, ammo tanish bir issiqlik uyg‘ondi,\n"
        "xuddi uzoq vaqtdan keyin eshitilgan eski qo‘shiq kabi."
    ),
    4: (
        "Bu hisni yashirishga urindim.\n"
        "O‘zimga “balki shunchaki eskilik hasrati” dedim.\n"
        "Lekin u kun sayin kuchayib bordi.\n"
        "Sizni ko‘rgan har bir lahzada ichimda tinchlik o‘rniga taranglik,\n"
        "tinchlik o‘rniga esa… umid paydo bo‘ldi.\n"
        "Xuddi bahor shamoli derazani ochib yuborgandek."
    ),
    5: (
        "Ba’zi hislar so‘zga sig‘maydi.\n"
        "Ular yurakning eng chuqur joyida saqlanadi\n"
        "va faqat vaqt o‘tishi bilan o‘ziga yo‘l topadi.\n"
        "Men bugun shunday hisni ochiq aytishga jur’at etmoqdaman.\n"
      "Men yaxshi niyyat ila szga ushbu gaplarni aytyabman.\n"
      "Qalbimda sizga nisbatan hech qanday yomonlik yo'q.\n"
      "Uchrashishga chaqirganim boisi ham szni yana bir bor ko'rish holos.\n"
      "Hoh bu uchrashuv 1 soat, hoh bir lahza bolsa ham mayli.\n"
    ),
    6: (
        "Agar bu xabar sizga og‘ir kelgan bo‘lsa — kechirasiz.\n"
        "men shu ( t.me/thePirmatov ) yerda javobingizni kutaman.\n\n"
        "Yozishingizni yoki jimligingizni hurmat qilaman.\n"
        "Lekin bilishingizni xohlardim:\n"
        "Mubina siz mening yuragimda maxsus o‘rin egalladingiz.\n"
      "Bu gaplarni o'zim szga ayta olmadim va shunday qilib sizga bolgan hislarimni yetkazmoqchi boldim holos!"
    )
}

def get_keyboard(step: int):
    if step < 6:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Davom et →", callback_data=f"next_{step+1}")]
        ])
    return None

@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    user = message.from_user
    await state.set_state(Form.step)
    await state.update_data(step=1)

    await bot.send_message(
        ADMIN_ID,
        f"🌸 Bot ishga tushirildi!\n"
        f"Ism: {user.full_name}\n"
        f"Username: @{user.username if user.username else 'yo‘q'}\n"
        f"ID: {user.id}"
    )

    await message.answer(TEXTS[1], reply_markup=get_keyboard(1))

@dp.callback_query(F.data.startswith("next_"))
async def next_step(callback: types.CallbackQuery, state: FSMContext):
    step = int(callback.data.split("_")[1])
    user = callback.from_user

    await state.update_data(step=step)

    await bot.send_message(
        ADMIN_ID,
        f"📌 U {step}-bosqichni ochdi\n"
        f"Ism: {user.full_name} | @{user.username if user.username else 'yo‘q'}"
    )

    if step == 6:
        await callback.message.edit_text(TEXTS[6], parse_mode="HTML")
        await callback.answer()
    else:
        await callback.message.edit_text(TEXTS[step], reply_markup=get_keyboard(step))
        await callback.answer()

@dp.message(Form.step)
async def forward_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_step = data.get("step", 1)

    if current_step >= 6:
        user = message.from_user
        text = (
            f"💬 U javob yozdi!\n"
            f"Ism: {user.full_name}\n"
            f"Username: @{user.username if user.username else 'yo‘q'}\n"
            f"ID: {user.id}\n\n"
            f"Xabar:\n{message.text}"
        )
        await bot.send_message(ADMIN_ID, text)
        await message.answer("Xabaring yetkazildi ✅")
    else:
        await message.answer("Iltimos, tugmalardan foydalaning 😊")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
