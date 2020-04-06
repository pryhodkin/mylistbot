import telebot
import consts
import psycopg2
import classes
import os

bot = telebot.TeleBot(str(os.environ['BOT_TOKEN']))

admins = classes.AdminList()

connect_vars = classes.DatabaseVars(str(os.environ['DATABASE_URL']))

connection = psycopg2.connect(
    host     = connect_vars['host']    ,
    database = connect_vars['database'],
    user     = connect_vars['user']    ,
    password = connect_vars['password']
)

db = classes.Database(connection);

@bot.chosen_inline_handler(lambda result: True)
def handle_answer(result):
    if (result.query == ''):
        pass
    elif (result.query.startswith("del")):
        db.DeleteFromList(classes.GetDelIndex(result.query))
    else:
        db.AddItemToList(result.query, result.from_user.username)


@bot.inline_handler(lambda query: classes.IsAdmin(admins, query.from_user.id) and query.query == '')
def handle_get(query):
    message_text = telebot.types.InputTextMessageContent(db.GetList())
    result = telebot.types.InlineQueryResultArticle(query.id, 'get list', message_text, thumb_url = consts.thumbnail_url)

    bot.answer_inline_query(query.id, [result], cache_time = 0)


@bot.inline_handler(lambda query: classes.IsAdmin(admins, query.from_user.id) and query.query.startswith("del"))
def handle_del(query):
    message_text = telebot.types.InputTextMessageContent(f"item No.{classes.GetDelIndex(query.query)} deleted.")
    title = f'Delete No. {classes.GetDelIndex(query.query)}'
    result = telebot.types.InlineQueryResultArticle(query.id, title, message_text, thumb_url = consts.thumbnail_url)

    bot.answer_inline_query(query.id, [result], cache_time = 0)


@bot.inline_handler(lambda query: classes.IsAdmin(admins, query.from_user.id))
def handle_query(query):
    message_text = telebot.types.InputTextMessageContent("Item: " + query.query + " added.")
    title = "New item: " + query.query
    result = telebot.types.InlineQueryResultArticle(query.id, title, message_text, thumb_url = consts.thumbnail_url)

    bot.answer_inline_query(query.id, [result], cache_time = 0)


@bot.message_handler(commands = ['start', 'help'])
def handle_start_help(message):
    answer = ''
    if(message.text == '/start'):
        answer = consts.start_string
    answer += consts.help_string
    bot.send_message(message.from_user.id, answer)


@bot.message_handler(func = lambda message: True)
def handle_message(message):
    bot.send_message(message.from_user.id, "Only for inline using, start typing @list_helper_bot \n /help")


bot.polling(none_stop = True, interval = 0)