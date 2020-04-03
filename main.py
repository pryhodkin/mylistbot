import telebot
import consts
import psycopg2
import classes
import os


def GenerateId():
    consts.iden += 1
    return consts.iden


bot = telebot.TeleBot("1215734535:AAFj1YBR8FIDJMIp2tpIhBvqLuv_EYX15uA")

connect_vars = classes.DatabaseVars(str(os.environ['DATABASE_URL']))

connection = psycopg2.connect(
    host = connect_vars['host'],
    database = connect_vars['database'],
    user = connect_vars['user'],
    password = connect_vars['password']
)

db = classes.Database(connection);


@bot.chosen_inline_handler(lambda result: True)
def handle_answer(result):
    if (result.query == 'get'):
        pass
    elif (result.query.startswith("del")):
        db.DeleteFromList(classes.GetDelIndex(result.query))
    else:
        db.AddItemToList(result.query, result.from_user.username)


@bot.inline_handler(lambda query: (query.from_user.id == 371404061 or query.from_user.id == 391960442) and query.query == 'get')
def handle_get(query):
    text = db.GetList()
    if text == "":
        text = "list is empty"
    result = telebot.types.InlineQueryResultArticle(int(query.id) + GenerateId(), 'get list',
                                                    telebot.types.InputTextMessageContent(text))
    bot.answer_inline_query(query.id, [result], cache_time = 0)


@bot.inline_handler(lambda query: (query.from_user.id == 371404061 or query.from_user.id == 391960442) and query.query.startswith("del"))
def handle_get(query):
    result = telebot.types.InlineQueryResultArticle(query.id, f'del No. {classes.GetDelIndex(query.query)}',
                                                    telebot.types.InputTextMessageContent(
                                                        f"item No.{classes.GetDelIndex(query.query)} deleted"))
    bot.answer_inline_query(query.id, [result], cache_time = 0)


@bot.inline_handler(lambda query: (query.from_user.id == 371404061 or query.from_user.id == 391960442))
def handle_query(query):
    result = telebot.types.InlineQueryResultArticle(query.id, "new item: " + query.query,
                                                    telebot.types.InputTextMessageContent(
                                                        "item: " + query.query + " added"))
    bot.answer_inline_query(query.id, [result], cache_time = 0)


@bot.message_handler(func = lambda message: True)
def handle_start(message):
    bot.send_message(message.from_user.id, "only for inline using, start type @list_helper_bot")


bot.polling(none_stop = True, interval = 0)