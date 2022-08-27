# !/usr/bin/env python3.10
# -*- coding: utf-8 -*-
import conf
from command_handler import command_handler
from slack_bolt.async_app import AsyncApp


app = AsyncApp()


@app.command(conf.Routes.COMMAND)
async def command(ack, body, respond):
    await ack()
    msg = await command_handler(body)
    await respond(f"Hi <@{body['user_id']}>,\n{msg}")

if __name__ == "__main__":
    app.start(conf.PORT)
