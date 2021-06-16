import telebot
from telebot import types
import pymysql

#koneksi sql
def connect_toko():
    conn = pymysql.connect(
        host='localhost', user='root', password='', db='db_userurdb')
    return conn

db_toko = connect_toko()
database = db_toko.cursor()

#token
token = ("somethingliketokentelegram")
bot = telebot.TeleBot(token)

nama_toko = None
id_toko = None
nama_produk = None
qty = None

@bot.message_handler(commands=['start'])
def greeting(message):
    bot.reply_to(message, "Selamat datang di Bot Admin Toko Kampung Rambutan\nGunakan perintah berikut untuk melakukan akses Admin\n\nToko\n/tambahtoko - Menambah/mendaftarkan toko\n\nProduk\n/tambahproduk - Menambah produk pada toko tertentu\n\nGunakan /about untuk melihat creator bot ini")

@bot.message_handler(commands=['about'])
def greeting(message):
    bot.reply_to(message, "Bot Toko dari User Kampung Durian Runtuh\nNama : I Gede Nyoman Ambara Yasa\nNIM     : 1905551115")
@bot.message_handler(commands=['tambahtoko'])
def toko_message(message):
    teks = "Masukan nama toko..."
    balas = bot.reply_to(message, teks)
    bot.register_next_step_handler(balas, add_toko)

def add_toko(message):
    global nama_toko
    nama_toko = str(message.text)
    sql = "INSERT INTO tb_toko(nama_toko) VALUES (%s)"
    val = (nama_toko)
    database.execute(sql, val)
    db_toko.commit()

    database.execute("SELECT * FROM tb_toko")
    hasil_sql = database.fetchall()
    balas = ""
    for x in hasil_sql:
        balas = balas + x[1] + '\n'
    
    text = '''
Toko Sukses Ditambahkan
List Toko :
{}
    '''.format(balas)
    bot.reply_to(message, text)

@bot.message_handler(commands=['tambahproduk'])
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
Pilih ID toko yang ingin ditambah produk
    '''.format(balas)

    balas = bot.reply_to(message, text, reply_markup=pilih_toko)
    bot.register_next_step_handler(balas, add_produk)

def add_produk(message):
    global id_toko
    id_toko = str(message.text)
    e = types.ReplyKeyboardRemove()
    teks = "Masukan nama produk..."
    balas = bot.reply_to(message, teks, reply_markup=e)
    bot.register_next_step_handler(balas, add_jumlah)

def add_jumlah(message):
    global nama_produk
    nama_produk = str(message.text)
    teks = "Masukan jumlah produk..."
    balas = bot.reply_to(message, teks)
    bot.register_next_step_handler(balas, add_harga)

def add_harga(message):
    global jumlah
    jumlah = str(message.text)
    teks = "Masukan harga produk..."
    balas = bot.reply_to(message, teks)
    bot.register_next_step_handler(balas, input_product)

def input_product(message):
    global nama_produk
    global id_toko
    global jumlah
    harga = str(message.text)
    insert = "INSERT INTO tb_produk(id_toko, nama_produk, jumlah, harga) VALUES (%s, %s, %s, %s)"
    val = (id_toko, nama_produk, jumlah, harga)

    database.execute(insert, val)
    db_toko.commit()
    balas = ""

    database.execute("SELECT * FROM tb_produk JOIN tb_toko ON tb_produk.id_toko = tb_toko.id_toko")
    for x in database.fetchall():
        balas = balas + x[2] + " [" + x[6]+"]\n"

    text = '''
Produk Berhasil Ditambahkan

List Produk :
{}
    '''.format(balas)
    bot.reply_to(message, text)

bot.polling(none_stop=True)
