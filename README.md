# Private Rooms Bot

A discord bot that makes use of the supposed-to-be deprecated OAuth scope of `gdm.join`. With this scope, you can add approving users to Group DM channels.

## Limitations of the scope

1. The bot **can** edit the name (and icon?) of the Group DM, while users **cannot**.
2. The bot **cannot** send/delete messages in the DM but **can** start the typing indicator (???) and *maybe* fetch messages.
3. The bot **cannot** add users to user created Group DMs and **can only** add users with a valid authenticated token.
4. Users with development mode enabled **cannot** copy the group channel ID.
5. Users **cannot** send attachments.
6. Title is displayed differently compared to regular Group DMs:

>|                   |                                                 |
>| ----------------- | ----------------------------------------------- |
>| Managed Group DMs | ![useful_image](/img/managed-group-dm-name.png) |
>| Regular Group DMs | ![useful_image](/img/regular-group-dm-name.png) |

## The Actual Bot

The bot was meant to run with a Quart webserver for using the OAuth flow. You could split them up and use `discord.ext.ipc` instead.
This could be actually useful with some kind of temporary private rooms which could be interesting, although there wouldn't be much to do without the bot being able to interact with the DM itself.

While writing this, I was running/testing it on [repl.it](https://replit.com), so if you just want to see how it works, you can try it out there.

Bot written with [pycord](https://github.com/Pycord-Development/pycord)

Licensed under MIT
