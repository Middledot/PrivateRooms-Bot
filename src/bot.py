from quart import Quart, redirect, request
import discord, os, dotenv, aiohttp

dotenv.load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CLIENT_TOKEN = os.environ.get('CLIENT_TOKEN')
CLIENT_ID = os.environ.get('CLIENT_ID')
BASE_URL = os.environ.get('BASE_URL')

client = discord.Bot()
client.match = {}

@client.event
async def on_ready():
    client.session = aiohttp.ClientSession()

app = Quart(__name__)

class ClassicView(discord.ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = 0
        self.msg = None

    @discord.ui.button(label="Join Room")
    async def callback(self, button, interaction):
        self.count += 1
        user_id = interaction.user.id
        if self.msg.id in client.match:
            client.match[self.msg.id]["pending"].append(user_id)
        else:
            client.match[self.msg.id] = {
                "group_id": None,
                "users": [],
                "pending": [user_id]
            }
            await interaction.response.send_message(f"Click [here](<{BASE_URL}/join>)", ephemeral=True)

@client.slash_command()
async def room_it(ctx):
    view = ClassicView(timeout=120)
    view.msg = await (await ctx.respond("here", view=view)).original_message()

@app.route('/')
async def home():
    return 'Private Rooms Website, how did you find this?'

@app.route('/join')
async def join():
    token = request.args.get('code', None)
    if token is None:
        return redirect(f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri=https%3A%2F%2Fprivate-rooms.middledot.repl.co%2Fjoin&response_type=code&scope=gdm.join%20identify")

    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_TOKEN,
        "grant_type": "authorization_code",
        "code": token,
        "redirect_uri": BASE_URL + "/join",
        "scope": "gdm.join%20identify"
    }
    access_token_data = await (await client.session.post(url="https://discord.com/api/oauth2/token", data=payload)).json()
    access_token = access_token_data["access_token"]
    identify = await (await client.session.get(url="https://discord.com/api/users/@me", headers={"authorization":f"Bearer "+access_token})).json()
    for msg_id, data in client.match.items():
        if int(identify["id"]) in data["pending"]:
            if data["group_id"] is None:
                group_dm = await (await client.session.post(url="https://discord.com/api/users/@me/channels", headers={"authorization":f"Bot "+BOT_TOKEN}, json={"access_tokens":[access_token]})).json()
                client.match[msg_id]["group_id"] = group_dm["id"]
                client.match[msg_id]["users"].append(int(identify["id"]))
                client.match[msg_id]["pending"].remove(int(identify["id"]))
                _id = group_dm["id"]
            else:
                _id = data["group_id"]
                client.match[msg_id]["users"].append(int(identify["id"]))
                client.match[msg_id]["pending"].remove(int(identify["id"]))
                await client.session.put(url=f"https://discord.com/api/channels/{data['group_id']}/recipients/{identify['id']}", headers={"authorization":f"Bot "+BOT_TOKEN}, json={"access_token":access_token})
        else:
            print(client.match)
    
    return redirect(f"https://discord.com/channels/@me/{_id}")

client.loop.create_task(app.run_task(host='0.0.0.0', port=4206))
client.run(BOT_TOKEN)
