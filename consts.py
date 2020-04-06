import os

thumbnail_url = str(os.environ['THUMBNAIL_URL'])

help_string = 'This bot works only in inline mode,\n' \
              'How to use? Easy!\n' \
              '\n' \
              '@list_helper_bot  - get the list;\n' \
              '@list_helper_bot <new item> - add <new item> to list;\n' \
              '@list_helper_bot del <n> - delete n`th item from from list.\n' \
              '\n' \
              'That\'s all! Start typing @list_helper_bot and you\'ll get the tip!\n'
start_string = 'Hi, this is the bot summoned to make easy creating & editing lists.\n\n\n'