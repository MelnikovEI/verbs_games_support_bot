# echobot-example

Простой бот, который отвечает вам вашими же фразами.

## Установка

[Установите Python](https://www.python.org/), если этого ещё не сделали. Требуется Python 3.8. Код может запуститься на других версиях питона от 3.1 и старше, но на них не тестировался.

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```
**Важно!** Версия Python должна быть 3.8

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`. Зависит это от операционной системы и от того, установлен ли у вас Python старой второй версии. 

Скачайте код:
```sh
git clone https://github.com/devmanorg/echobot-example.git
```

Перейдите в каталог проекта:
```sh
cd echobot-example
```

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:

- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`


Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```

Определите переменные окружения. Создайте файл `.env` в каталоге `echobot-example/` и положите туда такой код:
```sh
TELEGRAM_BOT_TOKEN=52...215:AAHv...FwbbCZ4
```

Данные выше приведены для примера. `DVMN_API_TOKEN` нужно заменить на токен от сайта Devman, его можно получить [на этой странице](https://dvmn.org/api/docs/). `TELEGRAM_API_TOKEN` замените на токен он чатбота в Telegram. Вот [туториал](https://spark.ru/startup/it-agenstvo-index/blog/47364/kak-poluchit-tokeni-dlya-sozdaniya-chat-bota-v-telegrame-vajbere-i-v-vkontakte), как это сделать. `TELEGRAM_CHAT_ID` замените на свой chat_id в Telegram. Его можно получить у [@userinfobot](https://telegram.me/userinfobot).

Используется в [туториле по systemd](https://dvmn.org/encyclopedia/deploy/systemd-tutorial/)
