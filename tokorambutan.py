import telebot
from telebot import types
import pymysql

#koneksi sql
def connect_toko():
    conn = pymysql.connect(
        host='localhost', user='root', password='', db='db_posttest_ims')
    return conn

db_toko = connect_toko()
database = db_toko.cursor()

#token
token = ("1805402296:AAHWPVNLZjWp_Z_9goofg2efKRrkaatQ83A")
bot = telebot.TeleBot(token)

nama_toko = None
id_toko = None
nama_produk = None
qty = None

@bot.message_handler(commands=['start'])
def greeting(message):
    bot.reply_to(message, "Selamat datang di Bot Toko Kampung Rambutan\nGunakan perintah berikut untuk melakukan aksi pada Bot ini\n\nToko\n/cektoko - Melihat toko yang tersedia\n\nProduk\n/cekproduk - Melihat produk yang tersedia di toko yang anda pilih\n\nGunakan /about untuk melihat creator bot ini")

@bot.message_handler(commands=['about'])
def greeting(message):
    bot.reply_to(message, "Bot Toko dari User Kampung Durian Runtuh\nNama : I Gede Nyoman Ambara Yasa\nNIM     : 1905551115")


@bot.message_handler(commands=['cektoko'])
def toko_message(message):
    database.execute("SELECT * FROM tb_toko")
    hasil_sql = database.fetchall()
    balas = ""
    for x in hasil_sql:
        balas = balas + x[1] + '\n'
    
    text = '''
List Toko Yang Tersedia :
{}
    '''.format(balas)
    bot.reply_to(message, text)

@bot.message_handler(commands=['cekproduk'])
def produk_message(message):
    balas = ""

    pilih_toko = types.ReplyKeyboardMarkup()

    database.execute("SELECT * FROM tb_toko")
    for data in database.fetchall():
        toko_type = types.KeyboardButton(data[0])
        pilih_toko.row(toko_type)
        balas = balas+str(data[0])+". "+data[1]+"\n"

    text = '''
List Toko (ID. Nama Toko):
{}
Pilih ID toko untuk melihat produk toko tersebut
    '''.format(balas)

    reply = bot.reply_to(message, text, reply_markup=pilih_toko)
    bot.register_next_step_handler(reply, cek_toko)

def cek_toko(message):
    global id_toko
    id_toko = str(message.text)
    e = types.ReplyKeyboardRemove()
    balas = ""

    database.execute("SELECT * FROM tb_produk JOIN tb_toko ON tb_produk.id_toko = tb_toko.id_toko WHERE tb_produk.id_toko={}".format(id_toko))
    for x in database.fetchall():
        balas = balas + x[2] + " [" + x[6]+"]\n"

    text = '''
List Produk:
{}
    '''.format(balas)
    bot.reply_to(message, text, reply_markup=e)

bot.polling(none_stop=True)