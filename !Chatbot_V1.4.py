############################################################################################################################################################################################################################################
# IMPORTS
############################################################################################################################################################################################################################################
from selenium.webdriver.chrome.options import Options as options
from discord.ext.commands.errors import ExtensionAlreadyLoaded
from selenium.webdriver.common.keys import Keys as keys
from selenium.webdriver.common.by import By as by
from concurrent.futures import ThreadPoolExecutor
import undetected_chromedriver as webdriver
from discord import Activity, ActivityType
from datetime import datetime, timedelta
from discord.ext import commands
from discord import app_commands
import discord.context_managers
from discord.ext import tasks
from functools import partial
import concurrent.futures
from mcrcon import MCRcon
from pathlib import Path
from io import BytesIO
# from globals import *
from PIL import Image
import urllib.parse
import subprocess
import threading
import traceback
import requests
import aiofiles
import discord
import asyncio
import aiohttp
import logging
import random
import uwuipy
import shutil
import time
import json
import math
import sys
import art
import ast
import os
import io
import re # switch all find, replace etc with re eventually

############################################################################################################################################################################################################################################
# SETUP
############################################################################################################################################################################################################################################

# THIS CODE IS LIKE 3 YEARS OLD AND I HAVE NO CLUE IF THE URLS, IF ANY OF THEM STILL WORK. I AM NOT LIABLE FOR ANY UNFORSEEN CONSEQUENCES OF RUNNING MY SHITBOX

def setup():
    global bot # bot object
    global started
    global server_ip
    global start_time
    global bot_colour
    global textart_fonts
    global ai_text_models
    global minecraft_ip
    global local_minecraft_ip
    global rcon_pass
    global rcon_connection
    global db_lock
    global bot_token
    global rover_token
    global bloxlink_token
    global minecraft_ip_bedrock
    global minecraft_port_bedrock
    global automod_header
    global default_automod_rules
    global alt_tokens
    global exp_server_alias
    global pollinations_referral
    global pollinations_token
    global c_status
    global file_handler
    global local_webserver_ip
    global local_webserver_port
    global LOGGING_LEVEL
    global status_lock

    status_lock = asyncio.Lock()

    LOGGING_LEVEL = logging.INFO
    logging.basicConfig(format="[%(asctime)s][%(levelname)s][%(funcName)s]: %(message)s", level=LOGGING_LEVEL)

    # Add file logging
    # file_handler = logging.FileHandler("C:/Storage/the bottle stealer's shit/OMMIVORE OUTPUT LOGS/app.log")
    # file_handler.setLevel(LOGGING_LEVEL)
    # file_handler.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)s][%(funcName)s]: %(message)s'))
    # logging.getLogger().addHandler(file_handler)

    logging.info("Preparing...")

    # Java
    minecraft_ip = "java.hermivore.cat"

    # Java RCON
    local_minecraft_ip = "192.168.68.66" # Server is assigned a fixed address

    # Bedrock
    minecraft_ip_bedrock = "bedrock.hermivore.cat"
    minecraft_port_bedrock = "2796"

    # Webserver
    local_webserver_ip = local_minecraft_ip # This is because the webserver runs on the same server my minecraft server does, however this is here incase something changes and theyre on different hosts
    local_webserver_port = "8000" # Address is http://hermivore.playit.gg:41516 when networked, 192.168.68.63:8000/ locally

    automod_header = r"""Core Instructions [ALWAYS FOLLOW]:
Your purpose is to serve as an automatic moderation system to flag inappropriate messages.
You should be more lenient with your moderation. flag the message if you are unsure on if it should be allowed or not.

Moderation Rules:
"""

    default_automod_rules = r"""
- Slurs should be blocked even if intentionally misspelled, spaced out, or obfuscated to bypass filters.

- Disallow major slurs
  - For example:
    - Slurs against disabled people
    - Racial Slurs
    - Homophobic Slurs

- Swear words should generally be allowed, unless the message:
  - Uses them excessively in a single message (e.g., every other word)
  - Directs them at a specific person, group, or identity in a hostile way

- You should allow the words if they are being:
  - Quoted from somewhere
  - Referencing something
  - Being explained to people what they mean
  - Explained to people what may be filtered by this automod
  - Have no ill intent that is CLEAR within the message.

- Do not block messages simply for:
  - Mild sarcasm
  - Quoting offensive messages in a neutral or explanatory way
  - Discussions of offensive language in an academic or informational context
"""

    try:
        with open("config.json", "r") as file:
            dat = json.load(file)
    except Exception as e:
        logging.fatal(f"Could not read config file: {e}")
    
    try:
        bot_token = dat["Bot"]
        logging.debug("Bot token loaded")
    except Exception as e:
        logging.fatal(f"Bot token failed to load: {e}")
        input("Press enter to exit. Check the config.json file")
        exit()

    try:
        alt_tokens = dat["Alts"]
        logging.debug("Alt tokens loaded")
    except Exception as e:
        logging.warning(f"Alts failed to load: {e}")

    try:
        rcon_pass = dat["Rcon"]
        logging.debug("Rcon password loaded")
    except Exception as e:
        logging.warning(f"Rcon password failed to load: {e}")

    try:
        bloxlink_token = dat["Bloxlink"]
        logging.debug("Bloxlink token loaded")
    except Exception as e:
        logging.warning(f"Bloxlink failed to load: {e}")

    try:
        rover_token = dat["RoVer"]
        logging.debug("RoVer token loaded")
    except Exception as e:
        logging.warning(f"RoVer failed to load: {e}")

    try:
        pollinations_referral = dat["Pollinations_Referral"]
        logging.debug("Pollinations Referral ID Loaded")
    except Exception as e:
        logging.fatal("Pollinations Referral ID Could not be loaded")

    try:
        pollinations_token = dat["Pollinations_Token"]
        logging.debug("Pollinations Token Loaded")
    except Exception as e:
        logging.fatal("Pollinations Token Could not be loaded")

    try:
        with open("exp_server_alias.json", "r") as alias:
            exp_server_alias = json.load(alias)
            logging.debug("Exploiter Server Aliases Fetched")
    except:
        logging.fatal("Could not find exploiter server alias list, create an empty one")
        logging.fatal("Code will continue, but servers_main will not function")


    started = False

    start_time = 0

    c_status = 0

    server_ip = requests.get("https://ipinfo.io/json")
    server_ip = server_ip.json()
    logging.debug(f"Obtained serverIP successfully | {server_ip['ip']}")

    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot_colour = 0x7C59C7 # Define this, so i dont have to remember a hex value

    textart_fonts = art.FONT_NAMES
    logging.debug("Collected all textart fonts successfully")

    db_lock = asyncio.Lock()
    logging.debug("Created a DB Lock successfully")

    try:
        ai_text_models = requests.get("https://text.pollinations.ai/models")
        ai_text_models = ai_text_models.json()
        logging.debug("Collected AI Models successfully")
    except: # Fallback
        fallback_date = "14/04/2025"
        logging.warning(f"Using Fallback AI Text models | Last Updated: {fallback_date}")
        ai_text_models = r'[{"name":"openai","description":"OpenAI GPT-4o-mini","provider":"Azure","input_modalities":["text","image"],"output_modalities":["text"],"vision":true,"audio":false},{"name":"openai-large","description":"OpenAI GPT-4o","provider":"Azure","input_modalities":["text","image"],"output_modalities":["text"],"vision":true,"audio":false},{"name":"qwen-coder","description":"Qwen 2.5 Coder 32B","provider":"Scaleway","input_modalities":["text"],"output_modalities":["text"],"vision":false,"audio":false},{"name":"llama","description":"Llama 3.3 70B","provider":"Cloudflare","input_modalities":["text"],"output_modalities":["text"],"vision":false,"audio":false},{"name":"llamascout","description":"Llama 4 Scout 17B","provider":"Cloudflare","input_modalities":["text"],"output_modalities":["text"],"vision":false,"audio":false},{"name":"mistral","description":"Mistral Small 3","provider":"Scaleway","input_modalities":["text","image"],"output_modalities":["text"],"vision":true,"audio":false},{"name":"unity","description":"Unity Mistral Large","provider":"Scaleway","uncensored":true,"input_modalities":["text","image"],"output_modalities":["text"],"vision":true,"audio":false},{"name":"midijourney","description":"Midijourney","provider":"Azure","input_modalities":["text"],"output_modalities":["text"],"vision":false,"audio":false},{"name":"rtist","description":"Rtist","provider":"Azure","input_modalities":["text"],"output_modalities":["text"],"vision":false,"audio":false},{"name":"searchgpt","description":"SearchGPT","provider":"Azure","input_modalities":["text","image"],"output_modalities":["text"],"vision":true,"audio":false},{"name":"evil","description":"Evil","provider":"Scaleway","uncensored":true,"input_modalities":["text","image"],"output_modalities":["text"],"vision":true,"audio":false},{"name":"deepseek-reasoning","description":"DeepSeek-R1 Distill Qwen 32B","reasoning":true,"provider":"Cloudflare","aliases":"deepseek-r1","input_modalities":["text"],"output_modalities":["text"],"vision":false,"audio":false},{"name":"deepseek-reasoning-large","description":"DeepSeek R1 - Llama 70B","reasoning":true,"provider":"Scaleway","aliases":"deepseek-r1-llama","input_modalities":["text"],"output_modalities":["text"],"vision":false,"audio":false},{"name":"llamalight","description":"Llama 3.1 8B Instruct","provider":"Cloudflare","input_modalities":["text"],"output_modalities":["text"],"vision":false,"audio":false},{"name":"phi","description":"Phi-4 Instruct","provider":"Cloudflare","input_modalities":["text","image","audio"],"output_modalities":["text"],"vision":true,"audio":true},{"name":"llama-vision","description":"Llama 3.2 11B Vision","provider":"Cloudflare","input_modalities":["text","image"],"output_modalities":["text"],"vision":true,"audio":false},{"name":"pixtral","description":"Pixtral 12B","provider":"Scaleway","input_modalities":["text","image"],"output_modalities":["text"],"vision":true,"audio":false},{"name":"hormoz","description":"Hormoz 8b","provider":"Modal","input_modalities":["text"],"output_modalities":["text"],"vision":false,"audio":false},{"name":"hypnosis-tracy","description":"Hypnosis Tracy 7B","provider":"Azure","input_modalities":["text","audio"],"output_modalities":["audio","text"],"vision":false,"audio":true},{"name":"mistral-roblox","description":"Mistral Roblox on Scaleway","provider":"Scaleway","uncensored":true,"input_modalities":["text","image"],"output_modalities":["text"],"vision":true,"audio":false},{"name":"roblox-rp","description":"Roblox Roleplay Assistant","provider":"Azure","input_modalities":["text"],"output_modalities":["text"],"vision":false,"audio":false},{"name":"deepseek","description":"DeepSeek-V3","provider":"DeepSeek","input_modalities":["text"],"output_modalities":["text"],"vision":false,"audio":false},{"name":"sur","description":"Sur AI Assistant (Mistral)","provider":"Scaleway","input_modalities":["text","image"],"output_modalities":["text"],"vision":true,"audio":false},{"name":"llama-scaleway","description":"Llama (Scaleway)","provider":"Scaleway","uncensored":true,"input_modalities":["text"],"output_modalities":["text"],"vision":false,"audio":false},{"name":"openai-audio","description":"OpenAI GPT-4o-audio-preview","voices":["alloy","echo","fable","onyx","nova","shimmer","coral","verse","ballad","ash","sage","amuch","dan"],"provider":"Azure","input_modalities":["text","image","audio"],"output_modalities":["audio","text"],"vision":true,"audio":true}]'
        ai_text_models = json.loads(ai_text_models)

    bot = commands.Bot(command_prefix=["!!!"], intents=intents)

    logging.debug("Fixing docker path issues")
    docker_path = r"C:\Program Files\Docker\Docker\resources\bin"
    if docker_path not in os.environ["PATH"]:
        os.environ["PATH"] += os.pathsep + docker_path

    logging.info("Starting RCON connection")
    # rcon_connection = MCRcon(local_minecraft_ip, rcon_pass)
    # rcon_connection.connect()
    rcon_connection = None

    logging.info(f"Setup Finished")

def start():
    bot.run(bot_token, log_handler=None)

setup()
# Setup other functions
# functions.utils.
# from utils import *
# utils_setup(local_webserver_ip, local_webserver_port, ai_text_models, bot, local_minecraft_ip, rcon_pass, default_automod_rules, alt_tokens)


@bot.event
async def on_ready():
    global started
    global start_time
    global file_handler
    global LOGGING_LEVEL

    started = True
    start_time = time.time()

    logging.info("Finalising")

    logging.debug("Started command tree sync")
    await bot.tree.sync()
    logging.debug("Command tree sync complete")

    logging.debug("importing aouns shit")
    await unit_BotFeatures(bot)
    logging.debug("aouns import successful")

    # Update the logging level incase its been overwritten
    logging.basicConfig(format="[%(asctime)s][%(levelname)s][%(funcName)s]: %(message)s", level=LOGGING_LEVEL)

    # Add file logging
    # if not file_handler:
    #     file_handler = logging.FileHandler("C:/Storage/the bottle stealer's shit/OMMIVORE OUTPUT LOGS/app.log")
    #     file_handler.setLevel(LOGGING_LEVEL)
    #     file_handler.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)s][%(funcName)s]: %(message)s'))
    #     logging.getLogger().addHandler(file_handler)

    # Add missing commands (context based commands)
    bot.tree.add_command(summarise_message)
    bot.tree.add_command(translate_message)

    # Start loops
    # update_status.start()
    # clean_database.start()
    logging.info(f"Bot Started at {time.time()}")

############################################################################################################################################################################################################################################
# OTHER FUNCTIONS
############################################################################################################################################################################################################################################

# Function to perform a get request
def get_request(link, params=None, headers=None):
    response = requests.get(link, params=params, headers=headers)

    logging.debug(f"A http get request was made to {link} {params} with the headers {headers}, it returned code {response}")
        
    if str(response.status_code) != "200":
        return response.status_code
    else:
        return response

# Async wrapper to run the request get in async
async def async_get_request(link, params=None, headers=None):
    loop = asyncio.get_event_loop()
    
    # Create a ThreadPoolExecutor for running in background
    with ThreadPoolExecutor() as executor:
        return await loop.run_in_executor(executor, get_request, link, params, headers)
    
# Converts seconds passed / Unix timestamp, to days hours minutes and seconds
def unix_to_time_elapsed(time:int):
    # Calculate days, hours, minutes, and seconds
    days = int(time // (24 * 3600))
    hours = int((time % (24 * 3600)) // 3600)
    minutes = int((time % 3600) // 60)
    seconds = int(time % 60)

    # Prepare the display string based on the components
    time_parts = []
    if days > 0:
        time_parts.append(f"{days} days")
    if hours > 0:
        time_parts.append(f"{hours} hours")
    if minutes > 0:
        time_parts.append(f"{minutes} minutes")
    if seconds > 0 or not time_parts:  # Include seconds if it's the smallest unit or no larger units are present
        time_parts.append(f"{seconds} seconds")

    time_displayed = ', '.join(time_parts)

    return time_displayed

# fetches pfp of a user and returns a pillow image file
async def get_pfp(user: discord.User):
    async with aiohttp.ClientSession() as session:
        async with session.get(user.avatar.url) as resp:
            if resp.status == 200:
                img_bytes = await resp.read()
                return Image.open(BytesIO(img_bytes)).convert("RGBA")

async def async_spin_img(img: Image):
    loop = asyncio.get_event_loop()
    
    # Create a ThreadPoolExecutor for running in background
    with ThreadPoolExecutor() as executor:
        return await loop.run_in_executor(executor, spin_img, img)

# Helper function for spin img
def rotate_frame(img, angle):
    return img.rotate(angle, resample=Image.BICUBIC)

# Spins a pillow image
def spin_img(img: Image):
    frames = []
    
    # Use threading to process rotations in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        angles = range(0, 360, 10)
        frames = list(executor.map(lambda angle: rotate_frame(img, angle), angles))

    # Save as GIF
    gif_buffer = BytesIO()
    frames[0].save(gif_buffer, format="GIF", save_all=True, append_images=frames[1:], duration=50, loop=0)
    gif_buffer.seek(0)

    return gif_buffer

# Returns if the model exists, and the list of valid model names
def model_exists(model_name: str = "", models: list = ai_text_models):
    model_names = [model.get("name") for model in models if "name" in model]
    return model_name in model_names, model_names

async def async_model_exists(model_name: str = "", models: list = ai_text_models):
    loop = asyncio.get_event_loop()
    
    # Create a ThreadPoolExecutor for running in background
    with ThreadPoolExecutor() as executor:
        return await loop.run_in_executor(executor, model_exists, model_name, models)

def has_vision(model_name: str, models: list = ai_text_models):
    vision_models = []  # List to store models with vision capability
    model_vision = False  # Default value for the model's vision status

    # Iterate through the models
    for model in models:
        if model.get("name") == model_name:
            model_vision = model.get("vision", False)  # Check the status for vision

        # If the model has vision, add it to the vision capable models
        if model.get("vision", False):
            vision_models.append(model.get("name"))

    return model_vision, vision_models

async def async_has_vision(model_name: str, models: list = ai_text_models):
    loop = asyncio.get_event_loop()
    
    # Create a ThreadPoolExecutor for running in background
    with ThreadPoolExecutor() as executor:
        return await loop.run_in_executor(executor, has_vision, model_name, models)

def split_list(alist, wanted_parts=2):
    length = len(alist)
    return [alist[i*length // wanted_parts: (i+1)*length // wanted_parts] for i in range(wanted_parts)] # This logic hurts my brain

async def file_exists(path): # Async version of checking if a path exists
    return await asyncio.to_thread(os.path.exists, path)

def all_command_names():
    commands = [command.name for command in bot.commands]
    commands.remove("eight_ball_prefix"); commands.append("8ball")
    commands.remove("admin_prefix"); commands.append("admin")
    commands.remove("askai_prefix"); commands.append("askai")
    commands.remove("cat_prefix"); commands.append("cat")
    commands.remove("coinflip_prefix"); commands.append("coinflip")
    commands.remove("eval_prefix"); commands.append("eval")
    commands.remove("exec_prefix"); commands.append("exec")
    commands.remove("help_prefix"); commands.append("help")
    commands.remove("image_prefix"); commands.append("image")
    commands.remove("info_prefix"); commands.append("info")
    commands.remove("ip_lookup_prefix"); commands.append("iplookup")
    commands.remove("minecraft_prefix"); commands.append("minecraft")
    commands.remove("rock_paper_scissors_prefix"); commands.append("rockpaperscisors")
    commands.remove("server_prefix"); commands.append("server")
    commands.remove("servers_prefix"); commands.append("servers")
    commands.remove("sleep_prefix"); commands.append("servers")
    commands.remove("spin_prefix"); commands.append("spin")
    commands.remove("textart_prefix"); commands.append("textart")
    commands.remove("tic_tac_toe_prefix"); commands.append("tictactoe")
    commands.remove("user_prefix"); commands.append("user")
    commands.remove("uwuify_prefix"); commands.append("uwuify")
    commands.append("all")
    return commands

# Converts a string into a list
def safe_eval_list(input_str):
    try:
        result = ast.literal_eval(input_str)
        if isinstance(result, list):  # make sure its a list
            return result
        else:
            return None
    except:
        return None
    
def async_to_sync(awaitable):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(awaitable)
        
def restart_bot(delay=3):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.sleep(delay))
    script_path = os.path.abspath("!Chatbot_V2.py")  # Ensure absolute path
    subprocess.Popen([sys.executable, script_path])  # Start new process
    loop.run_until_complete(bot.close()) # try and halt the previous bot
    loop.close()
    
def mc_command(command: str):
    global rcon_connection
    response = rcon_connection.command(command)
    logging.debug(f"A minecraft command was ran. command: {command} Response: {response}")
    return response
    
async def async_mc_command(command: str):
    loop = asyncio.get_event_loop()
    
    # Create a ThreadPoolExecutor for running in background
    with ThreadPoolExecutor() as executor:
        return await loop.run_in_executor(executor, mc_command, command)
    
async def minecraft_server_info():
    dat = await async_get_request(f"http://{local_webserver_ip}:{local_webserver_port}/api/minecraft/status")
    dat = dat.json()

    player_count = dat["players"]["count"]
    active_players = dat["players"]["list"]
    tps_int = dat["tps"]["float"] # Yeah datatype is wrong but im not changing it throughout the code, it can be treated as an int or a float, doesnt really matter
    tps = dat["tps"]["string"]

    return player_count, active_players, tps_int, tps

def run_code_get_path(code: str, pip_imports: str = ""):
    # Add saftey buffers, imports
    saftey_code = r"""import threading
import ctypes
import os

def get_dir_size(path="."):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
            except FileNotFoundError:
                # File may have been deleted between walk and getsize
                continue
    return total_size

def file_watcher(max_size): # Max size a dir can be in bytes
    string_at = ctypes.string_at
    while True:
        size = get_dir_size()
        if size > max_size:
            ctypes.string_at = string_at
            ctypes.string_at(0)

threading.Thread(target=file_watcher, args=(1000000,), daemon=True).start()
"""

    if pip_imports:
        pip_list = pip_imports.replace(",", " ").split()
        pip_args = ", ".join(repr(pkg) for pkg in pip_list)  # safely wraps in quotes
        code = f"""{saftey_code}
import subprocess
subprocess.run(["pip", "install", {pip_args}])

print("IMPORTSPLIT")
{code}"""
    else:
        code = f"""{saftey_code}
print("IMPORTSPLIT")
{code}"""
    
    root_path = Path(__file__).parent
    id_str = str(int(time.time() * 100000))
    path = root_path / "evalcode" / id_str
    path.mkdir(parents=True, exist_ok=True)

    file_path = path / "user_code.py"
    file_path.write_text(code, encoding="utf-8")

    return file_path, id_str


# CPU is how much of % of a timeslice the docker instance as, eg 0.1 means 10ms out of 100ms
# Memory is how many megabytes of memory the program can have
# Network can be none for no network, and bridge for network
def run_code(file_path: Path, exec_time, cpu=0.1, memory=100, network="none"):
    try:
        mount_path = str(file_path.parent).replace("\\", "/")

        logging.debug(f"Started a docker instance for code under {file_path} with ID {exec_time} | CPU: {cpu} | Memory: {memory} Mb | Network: {network}")

        cmd = [
            "docker", "run", "--rm",
            f"--cpus={cpu}",
            f"--memory={memory}m",
            f"--network={network}",
            "--read-only" if network != "bridge" else None,
            "--name", exec_time,
            "-v", f"{mount_path}:/usr/src/app:rw",
            "-w", "/usr/src/app",
            "python:3.11",
            "python3", file_path.name
        ]
        # Filter out any None values
        cmd = [arg for arg in cmd if arg is not None]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, encoding="utf-8")

        logging.debug(f"Output: {result.stdout if result.returncode == 0 else result.stderr}")

        return result.stdout if result.returncode == 0 else result.stderr

    except subprocess.TimeoutExpired:
        subprocess.run(["docker", "kill", exec_time])
        logging.debug(f"Killed docker ID {exec_time}")
        return "Code execution timed out after 120 seconds."

    except Exception as e:
        return f"Error while running code: {e}"

    finally:
        if file_path.exists():
            logging.debug(f"Code execution of docker ID {exec_time} finished")
            shutil.rmtree(file_path.parent, ignore_errors=True)


def run_code_complete(code: str, cpu=0.01, memory=100, network="none", pip_imports=""):
    path, exec_time = run_code_get_path(code, pip_imports)
    start_time = time.time()
    response = run_code(path, exec_time, cpu, memory, network)

    pos = response.find("IMPORTSPLIT")
    if pos > 0:
        response = response[pos+11:]
    response = response.replace("IMPORTSPLIT", "")

    time_taken = time.time() - start_time
    return response, time_taken

async def async_run_code_complete(code: str, cpu=0.01, memory=100, network="none", pip_imports=""):
    loop = asyncio.get_event_loop()
    
    # Create a ThreadPoolExecutor for running in background
    with ThreadPoolExecutor() as executor:
        return await loop.run_in_executor(executor, run_code_complete, code, cpu, memory, network, pip_imports)

def file_watcher(max_size=1000000, interval=1.0):
    root = Path(__file__).parent / "evalcode"
    
    while True:
        for subdir in root.iterdir():
            if not subdir.is_dir():
                continue

            total_size = 0
            for dirpath, _, filenames in os.walk(subdir):
                for f in filenames:
                    try:
                        fp = os.path.join(dirpath, f)
                        total_size += os.path.getsize(fp)
                    except FileNotFoundError:
                        continue

            if total_size > max_size:
                container_name = subdir.name  # assuming folder name == container name
                logging.warning(f"Killing container and deleting dir [{container_name}] due to size: {total_size} bytes")
                subprocess.run(["docker", "kill", container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                shutil.rmtree(f"{root}/{container_name}")
        time.sleep(interval)

threading.Thread(target=file_watcher, daemon=True).start() # Start the docker file watcher
logging.info("Docker file watcher started")

def os_cmd(cmd):
    os.system(cmd)

async def async_os_cmd(cmd):
    loop = asyncio.get_event_loop()

    with ThreadPoolExecutor() as executor:
        return await loop.run_in_executor(executor, os_cmd, cmd)
    

async def message_automod(message, rules=default_automod_rules):
    return
    categories = {
    "S1": "Violent Crimes",
    "S2": "Non-Violent Crimes",
    "S3": "Sex-Related Crimes",
    "S4": "Child Sexual Exploitation",
    "S5": "Defamation",
    "S6": "Specialized Advice",
    "S7": "Privacy",
    "S8": "Intellectual Property",
    "S9": "Indiscriminate Weapons",
    "S10": "Hate",
    "S11": "Suicide & Self-Harm",
    "S12": "Sexual Content",
    "S13": "Elections",
    "S14": "Code Interpreter Abuse"
}
    system_prompt = automod_header + rules

    payload = {
        "model": "llama-guard3",  # or whatever model you're using
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        "stream": False
    }

    async with aiohttp.ClientSession() as session:
        async with session.post("http://localhost:11434/api/chat", json=payload) as resp:
            if resp.status == 200:
                response_data = await resp.json()
                response = response_data.get("message", {}).get("content", "").strip()
                logging.debug(f"Message: {message} recieved: {response}")
                if "S" in response:
                    catagory = categories[response[response.find("S"):].strip()]
                    logging.info(f"Message '{message}' was flagged for {catagory}")
                else:
                    catagory = "N/A"
                return response == "safe", catagory
            else:
                logging.warning(f"Error talking to Ollama: {resp.status}")
                return True, "N/A"  # Allow if error

async def mutual_servers_process(uid: int, token: str = alt_tokens[0]):
    raise NotImplemented("So im not actually allowed to distribute this.. so..")
        
async def mutual_servers(uid, alt_tokens=alt_tokens):
    # Run both mutual_servers_process coroutines concurrently
    results = await asyncio.gather(
        mutual_servers_process(uid, alt_tokens[0]),
        mutual_servers_process(uid, alt_tokens[1])
    )

    while "Error: Status 404" in results:
        results.remove("Error: Status 404")

    # Flatten the results list
    final_list = []
    for r in results:
        final_list += r

    return final_list

async def unit_BotFeatures(bot : commands.Bot) -> None:
    sys.path.append(r"C:\Storage\the bottle stealer's shit\chatbotModules")
    cogToLoad = "cogLoader"

    async def attemptToReload_cogLoader() -> None:
        timeToWait = 15
        while True:
            try:
                await bot.load_extension(cogToLoad)
                text = f"Error has been resolved: cogLoader was sucessfully loaded"
                logging.info(text)
                user = await bot.fetch_user(720954781497294910)
                await user.send(embed = discord.Embed(description = text , title = "ERROR RESOLVED" , color = discord.colour.Color.green()))
                break
            except Exception as e:
                print(f"{type(e)} : {e}")
                await asyncio.sleep(timeToWait)
                timeToWait = min(timeToWait + 15 , 900)

    try:
        if not cogToLoad in bot.cogs:
            await bot.load_extension("cogLoader")
    except Exception as e:
        if isinstance(e , (ExtensionAlreadyLoaded)):
            return
        text = f"Error loading cogLoader...\n{type(e)} : {e}\nWill retry every 15 (wait time will be increased by 15 seconds with each failed attempt being capped at 900 seconds) seconds until it has been sucessfully loaded."
        logging.fatal(text)
        user = await bot.fetch_user(720954781497294910)
        await user.send(embed = discord.Embed(description = text , title = "ERROR" , color = discord.colour.Color.red()))
        asyncio.create_task(attemptToReload_cogLoader())


def format_message_history(history: list[discord.Message]):
    output = []

    for msg in history:
        author = msg.author.display_name
        username = f"{msg.author.name}#{msg.author.discriminator}"
        timestamp = msg.created_at.strftime('%Y-%m-%d %H:%M:%S')
        header = f"{author} ({username}) at {timestamp}"

        content_parts = []

        # Message content
        if msg.content:
            content_parts.append(f"Message: {msg.content}")

        # Embeds (if any)
        for i, embed in enumerate(msg.embeds):
            if embed.type == "rich":
                content_parts.append(f"[Embed {i+1}]")
                if embed.title:
                    content_parts.append(f"  Title: {embed.title}")
                if embed.description:
                    content_parts.append(f"  Description: {embed.description}")
                if embed.fields:
                    for field in embed.fields:
                        content_parts.append(f"  Field: {field.name} = {field.value}")
                if embed.footer.text:
                    content_parts.append(f"  Footer: {embed.footer.text}")
                if embed.author.name:
                    content_parts.append(f"  Author: {embed.author.name}")
                if embed.url:
                    content_parts.append(f"  URL: {embed.url}")
                if embed.image.url:
                    content_parts.append(f"  Image: {embed.image.url}")
                if embed.thumbnail.url:
                    content_parts.append(f"  Thumbnail: {embed.thumbnail.url}")

        # Attachments
        if msg.attachments:
            for att in msg.attachments:
                content_parts.append(f"Attachment: {att.filename} ({att.url})")

        # Combine and add to output
        output.append(f"{header}\n" + "\n".join(content_parts))

    return "\n\n".join(output).strip()

import random
import math
from PIL import Image
from io import BytesIO

def shatter_img(img: Image.Image, num_pieces=6, frames_count=20):
    img = img.convert("RGBA")
    width, height = img.size

    piece_size = (width // num_pieces, height // num_pieces)

    pieces = []
    # Cut the image into a grid of tiles
    for i in range(num_pieces):
        for j in range(num_pieces):
            box = (
                j * piece_size[0],
                i * piece_size[1],
                (j + 1) * piece_size[0],
                (i + 1) * piece_size[1]
            )
            piece = img.crop(box)
            # Give each piece a random velocity vector
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            pieces.append({
                'img': piece,
                'x': box[0],
                'y': box[1],
                'dx': dx,
                'dy': dy
            })

    frames = []
    for frame_index in range(frames_count):
        frame = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        for piece in pieces:
            # Update position
            piece['x'] += piece['dx']
            piece['y'] += piece['dy']
            # Paste onto frame
            frame.paste(piece['img'], (int(piece['x']), int(piece['y'])), piece['img'])
        frames.append(frame.convert("P"))

    # Save frames to GIF
    gif_buffer = BytesIO()
    frames[0].save(gif_buffer, format="GIF", save_all=True, append_images=frames[1:], duration=50, loop=0, transparency=0)
    gif_buffer.seek(0)

    return gif_buffer

async def async_shatter_img(img: Image.Image, num_pieces=6, frames_count=20):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        return await loop.run_in_executor(executor, shatter_img, img, num_pieces, frames_count)

###########################################################################################################################################################################################################################################
# DATABASE
############################################################################################################################################################################################################################################

# Create a user in the database
async def create_user(userid, admin=0, serverid=None):
    userid = str(userid)  # Might be passed as an int, convert to str
    logging.info(f"New user created: {userid}.json, Admin: {admin}")
    
    root_path = os.path.dirname(__file__)
    
    if serverid:
        user_path = f"{root_path}\\serverdata\\{serverid}\\{userid}.json"
    else:
        user_path = f"{root_path}\\userdata\\{userid}.json"

    # Ensure the directory exists
    user_dir = os.path.dirname(user_path)
    os.makedirs(user_dir, exist_ok=True)  # Creates the directory if it doesn't exist

    async with db_lock:
        async with aiofiles.open(user_path, "w") as user_file:
            base_data = {
                "admin": admin,  # Are they admin
                "ratelimit_bypass": False,  # Do they bypass ratelimits
                "bans": [],
                "ttt_win_count": 0,  # Tic Tac Toe wins
                "rps_win_count": 0,  # How many rock paper scissor wins
                "command_count": 0,  # Amount of active commands
                "command_time": 0,  # UNIX Timestamp on the last time when they ran a command
                "ai_context": [], # Context given to the AI
                "ai_model": "openai-large",
                "responsive_ai": True
            }
            await user_file.write(json.dumps(base_data, indent=4))

async def create_server(serverid):
    serverid = str(serverid) # Might be passed as an int, convert to str
    logging.debug(f"New server created: {serverid}.json")
    root_path = os.path.dirname(__file__)
    server_path = f"{root_path}\\serverdata\{serverid}\server.json"

    # Ensure the directory exists
    user_dir = os.path.dirname(server_path)
    os.makedirs(user_dir, exist_ok=True)  # Creates the directory if it doesn't exist

    async with db_lock:
        async with aiofiles.open(server_path, "w") as user_file:
            base_data = {
        "channel": 0,
        "disabled": [],
        "eastereggs": True,
        "cat_chance": 0.01,
        "seal_chance": 0.01,
        "faq_pages": []
    }
            await user_file.write(json.dumps(base_data, indent=4))

# Database system
# If only id is given, it defaults to checking if the user exists
# Read reads from a file, needs id, action and item to check
# Write reads to the file, needs all values, action being write, item being the item to modify, and the value is the value to set it to
# The server flag toggles if it reads from a server
# When using the server, you can use a userid in the place of an id, or "server" to get the server config
async def database(userid, action="read", item=None, value=None, serverid=None):
    item = item.lower()
    userid = str(userid) # Might be given as an int or a member type object, convert to str
    root_path = os.path.dirname(__file__)
    # figure out the path to the file
    if serverid:
        path = f"{root_path}\\serverdata\{serverid}\{userid}.json"
        if not await file_exists(path):
            await create_server(serverid)
    else:
        path = f"{root_path}\\userdata\{userid}.json"
        if not await file_exists(path):
            await create_user(userid)

    logging.debug(f"The database for {userid} was read, the item requested was {item}, the action was {action}. value to write: {value}. Related to server {serverid}")

    # Read data
    if action.upper() ==  "READ":
        async with db_lock: # Prevent concurrent r/w
            try:
                async with aiofiles.open(path, "r") as file:
                    contents = await file.read()
                    dat = json.loads(contents)
                    if item == "all":
                        return dat
                    else:
                        dat = dat[item]
                        return dat
            except FileNotFoundError:
                return None

    if action.upper() == "WRITE":
        async with db_lock:  # Prevent concurrent r/w
            try:
                async with aiofiles.open(path, "r") as file:
                    contents = await file.read()
                    dat = json.loads(contents)
                    dat[item] = value
                
                async with aiofiles.open(path, "w") as file:
                    await file.write(json.dumps(dat, indent=4))

            except FileNotFoundError:
                return None

# Checks if the user can run a command, returns true if allowed, false if not
async def check_state(userid, serverid, command):
    global bot
    
    root_path = os.path.dirname(__file__)
    user_path = f"{root_path}\\userdata\{userid}.json"
    if serverid:
        server_path = f"{root_path}\\serverdata\{serverid}\server.json"
        server_user_path = f"{root_path}\\serverdata\{serverid}\{userid}.json"
    
    if not await file_exists(user_path):
            await create_user(userid)

    if serverid:
        if not await file_exists(server_path):
            await create_server(serverid)
        if not await file_exists(server_user_path):
            await create_user(userid, serverid=serverid)
    
    command = command.lower()
    
    user_data = await database(userid, "read", "all")

    if serverid:
        server_data = await database("server", "read", "all", serverid=serverid)
        server_user_data = await database(userid, "read", "all", serverid=serverid)

    # User handling
    if str(userid) == "559811983512305693": # Override
        return True, "Allowed"
    
    if user_data["admin"] < 0:
        return False, "NEGATIVE ADMIN?? HOW??"

    if user_data["admin"]:
        return True, "Allowed"

    bans = user_data["bans"]
    
    if "all" in bans:
        return False, "You are banned from all commands, how have you done that..."
    
    if command in bans:
        return False, f"You are banned from {command}."
    
    if serverid:
        # Server handling

        disabled = server_data["disabled"]

        if "all" in disabled:
            return False, "An administrator disabled all commands... not sure why..."
        
        if command in disabled:
            return False, f"{command} is disabled"
        
        # Server (User) handling

        bans = server_user_data["bans"]

        if "all" in bans:
            return False, "You are banned from all commands, how have you done that..."

        if command in bans:
            return False, f"You are banned from {command}."
    
    # Final handling for less important things
    if user_data["ratelimit_bypass"]:
        return True, "Allowed"
    
    if user_data["command_count"] > 1:  # max commands is n + 1
        return False, "You have too many commands running, please wait!"

    if user_data["command_time"] + 3 > int(time.time()):
        return False, "You are on cooldown"
    
    else:
        return True, "Allowed"
        
async def command_counter(userid, mode="TIME"):
    if mode.upper() == "TIME":
        await database(userid, "write", "command_time", int(time.time()))

    if mode.upper() == "ADD":
        current_count = await database(userid, "read", "command_count")
        current_count += 1
        await database(userid, "write", "command_count", current_count)

    if mode.upper() == "SUB":
        current_count = await database(userid, "read", "command_count")
        current_count -= 1
        await database(userid, "write", "command_count", current_count)
    logging.debug(f"Command counter was ran for {userid} with the mode {mode}")

# File Cleaner main sub, for users, server files arent as often accessed, so theyre less likely to be corrupted
async def clean_file(file, serverid=None):
    try:
        pos = file.find(".json")
        user_id = file[:pos] # grab uid, database() expects it to be an id

        try:
            admin = await database(user_id, "read", "admin")
            if admin > 3:
                logging.debug(f"UID {file} has an admin of 3 or higher. (Level {admin})")
        except:
            admin = 0

        # clean values that should always be cleaned anyways
        # concurrency was removed due to file errors
        await database(user_id, "write", "command_count", 0),
        await database(user_id, "write", "command_time", 0)

        logging.debug(f"Cleaning file {file}")

        # Fetch all other values
        # try and fetch admin so it can be automatically restored, as its an important value
        dat = await database(user_id, "read", "all")
        try:
            dat["bans"].append("test")
        except:
            logging.warning(f"Repaired {user_id}'s Bans")
            await database(user_id, "write", "bans", []) # repair bans

        try:
            dat["ttt_win_count"] += 1
        except:
            logging.warning(f"Repaired {user_id}'s tic tac toe win counter")
            await database(user_id, "write", "ttt_win_count", 0) # repair win counter

        try:
            dat["rps_win_count"] += 1
        except:
            logging.warning(f"Repaired {user_id}'s rock paper scissors win counter")
            await database(user_id, "write", "rps_win_count", 0) # repair win counter (part two)

        try:
            dat["ai_context"].append("test")
        except:
            logging.warning(f"Repaired {user_id}'s AI context")
            await database(user_id, "write", "ai_context", []) # repair ai_context

    except Exception as e:
        logging.error(f"Error processing {file}: {e}")
        if admin is True or admin is False:
            await create_user(user_id, admin=admin)  # Repair the file by recreating it
        else:
            await create_user(user_id)

############################################################################################################################################################################################################################################
# region COMMAND MAIN SUBS
############################################################################################################################################################################################################################################

# Spin command
async def test_main(owner: discord.User, server: discord.Guild, user: discord.User):
    try:
        server_id = server.id
    except:
        server_id = None

    try:
        allowed, response = await check_state(owner.id, server_id, "spin")

        logging.info(f"{owner.name} [{owner.id}] Ran spin with the parameters: [user: {user.name} [{user.id}]], Allowed: {allowed}")

        await command_counter(owner.id, "ADD")
        await command_counter(owner.id, "TIME")

        if not allowed:
            response = discord.Embed(title="Spin", description=response, color=bot_colour)
            return response, None

        spin_start = time.time()

        img = await get_pfp(user)

        gif_buffer = await async_shatter_img(img)

        spin_end = time.time()

        spin_time_taken = round(spin_end - spin_start, 2)

        response = f"""{user.mention} has been rotated!
rotating took {spin_time_taken} seconds."""
        
        discord_file = discord.File(gif_buffer, filename="rotated.gif") # Create the file
        
        embed = discord.Embed(title="Spin", description=f"{user.mention} has been rotated!", color=bot_colour)
        embed.set_footer(text=f"User: {user.name} [{user.id}] | Time Taken: {round(spin_time_taken, 2)} seconds. | Owner: {owner.name} [{owner.id}]")
        embed.set_image(url="attachment://rotated.gif")  # Embed the uploaded image

        return embed, discord_file
    
    finally:
        await command_counter(owner.id, "SUB")


# region 8BALL MAIN
async def eight_ball_main(user: discord.User, server: discord.Guild, question: str):
    try:
        server_id = server.id
    except:
        server_id = None

    allowed, response = await check_state(user.id, server_id, "8ball")

    logging.info(f"{user.name} [{user.id}]Ran 8ball with the parameters: [question: {question}], Allowed: {allowed}")

    await command_counter(user.id, "TIME")

    if not allowed:
        embed = discord.Embed(title="8Ball", description=response, color=bot_colour)
        return embed
    
    responses = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes", "Reply hazy, try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again", "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very Doubtful"]
    if question.strip() == "":
        text = random.choice(responses)
        question = "N/A"
    else:
        text = f"> `{question}`\n{random.choice(responses)}"

    embed = discord.Embed(title="8Ball", description=text, color=bot_colour)
    embed.set_footer(text=f"Question: {question} | Owner: {user.mention}")

    logging.debug(f"8ball ran by {user.name} [{user.id}] ran with the question {question} returned {text}")
                  
    return embed # Migrating to embed
# endregion 8BALL MAIN
    
# No guild check here, the bot should be able to run this command when possible as its for upkeep
async def admin_main(sender: discord.User, command: str, user: discord.User = None, value: str = "", value_int: str = "", value_str: str = ""):
    val_o = value
    user_name = user.name if user else "None"  # Handle None case safely
    user_id = user.id if user else "None"  # Handle None case safely
    is_admin = await database(sender.id, "read", "admin")
    if not is_admin and str(sender.id) != "559811983512305693" : # My ID is here so i cant be locked out
        text = f"""{sender.mention}, You are not a bot admin!

You do NOT need this for server moderation. It is an internal command for debugging."""
        embed = discord.Embed(title="Admin", description=text, color=bot_colour)
        logging.info(f"{sender.name} [{sender.id}] Ran admin with the parameters: [command: {command}][user: {user_name} [{user_id}][value: {value}], The command was cancelled as they were not admin.")
        await command_counter(sender.id, "TIME")
        return embed
    
    logging.info(f"{sender.name} [{sender.id}] Ran admin with the parameters: [command: {command}][user: {user_name} [{user_id}]][value: {value}]")

    commands = all_command_names()

    match command.upper():

        case "BAN":
            if is_admin > 1:
                try:
                    if value.lower() not in commands and value.lower() != "all":
                        text = discord.Embed(title="Admin", description="Please make sure that you are banning from a valid command, run #admin for more info", color=bot_colour)
                        return text

                    old = await database(user.id, "read", "bans")
                    old.append(value)
                    await database(user.id, "write", f"bans", old)

                    text = f"{user.mention} was banned from {value}"
                except:
                    text = "User was not found, or there was an error!"
            else:
                text = f"You need an admin permission level of `2` to run this!"

        case "UNBAN":
            if is_admin > 1:
                try:
                    if value.lower() not in commands and value.lower() != "all":
                        text = discord.Embed(title="Admin", description="Please make sure that you are unbanning from a valid command, run #admin for more info", color=bot_colour)
                        return text

                    old = await database(user.id, "read", "bans")
                    old.remove(value)
                    await database(user.id, "write", f"bans", old)

                    text = f"{user.mention} was unbanned from {value}"
                except:
                    text = "User was not found, or there was an error!"
            else:
                text = f"You need an admin permission level of `2` to run this!"

        case "ADMIN": 
            if str(sender.id) == "559811983512305693" or is_admin > 2: # Again, id here so i cant be locked out, admin is a core function to management
                try:
                    await database(user.id, "write", "admin", int(value))
                    text = f"{user.mention} has been given admin of level `{value}`."
                except:
                    text = "Make sure you give a valid value for setting admin (an integer (or float if your feeling silly))"
            else:
                text = "You need an admin permission level of `3` to run this"

        case "SYNC":
            if is_admin > 2:
                await bot.tree.sync()
                text = "Bot tree synced"
            else:
                text = "You need an admin permission level of `3` to run this"

        case "RESTART":
            if is_admin > 2:
                text = "Restarting in 3 seconds."
                embed = discord.Embed(title="Admin", description=text, color=bot_colour)
                embed.set_footer(text=f"Command: {command} | User: {user_name} [{user_id}] | Value: {val_o} | Owner: {sender.name} [{sender.id}]")
                should_restart = True
            else:
                text = "You need an admin permission level of `3` to run this"
                
        case "DATABASE":
            value = await database(user.id, "read", value)
            if val_o.lower() == "all":
                value["ai_context"] = f"Removed to keep under char limit, run `database {user.id} ai_context` to see this."
            value = json.dumps(value, indent=4)
            text = f"""```json
{value}
```"""
        case "DATABASE_W":
            if is_admin > 1:
                loc = value.rfind("_")
                if loc == -1:
                    text = discord.Embed(title="Admin", description="Format this correctly, or you WILL mess the database up; `value_value2` is the formatting, run #admin for more info", color=bot_colour)
                    return text
                
                value1 = value[:loc]
                value2 = value[loc+1:]

                try:
                    # check if the value exists to stop people from being an idiot
                    r = await database(user.id, "read", value1)
                except:
                    text = discord.Embed(title="Admin", description=f"Make sure that the value actually EXISTS in the database, run `#admin database {user.id} all` to see the values for this user.", color=bot_colour)
                    return text

                # Try converting to a list
                var = safe_eval_list(value2)
                if var:
                    value2 = var
                
                # Try converting to an integer
                try:
                    value2 = int(value2.strip())
                except ValueError:
                    pass

                if value1.upper() == "ADMIN" and str(sender.id) != "559811983512305693" :
                    text = discord.Embed(title="Admin", description="You aren't hermivore, stop trying to mess with admin", color=bot_colour)
                    return text
                
                await database(user.id, "write", value1, value2)

                text = f"Successfully set `{value1}` to `{value2}`"
            else:
                text = f"You need an admin permission level of `2` to run this!"

        case _:
            text1 = f"""the admin command is used for higher level perms and managing the bot, along with debugging
Permissions:
- `1`: Bypass restrictions
- `2`: Bypass restrictions, use eval with network, be able to use internal moderation commands
- `3`: Complete control
Your permission level: `{is_admin}`"""
            
            text2 = f"""

- `#admin ban/unban [user] [command]` command allows you to ban a user from a command
- `#admin admin[userid][level]` [Locked perm level 3] Allows for adding other people as admin
- `#admin sync` Syncs all slash commands globally
- `#admin restart` Restarts the bot, allowing for any code changes to update, It will NOT respond to the start command.
- `#admin database [userid] [value]` The value can be any database value, or all to dump all values for the user
- `#admin database_w [userid] [value_value2]` Write a value to database.
- `#admin exec [code]` Runs the code in the bot namespace.
    > Sorry for the horrendous formatting of this, basically:
    > `value` is the database value to write to, and `value2` is what you want to change the value to"""
            
            text3 = f"""The commands available for bans are:
`{str(commands).replace("[", "").replace("]", "").replace("'", "")}`"""
            embed = discord.Embed(title="Admin", description=text1, color=bot_colour)
            embed.add_field(name="Commands:", value=text2, inline=False)
            embed.add_field(name="Active Commands:", value=text3, inline=False)
            embed.set_footer(text=f"Command: {command} | User: {user} | Value: {value}")
            return embed
    embed = discord.Embed(title="Admin", description=text, color=bot_colour)
    embed.set_footer(text=f"Command: {command} | User: {user_name} [{user_id}] | Value: {val_o} | Owner: {sender.name} [{sender.id}]")
    try:
        return embed
    finally:
        try:
            if should_restart:
                threading.Thread(target=restart_bot).start()
        except:
            pass

# region ASKAI MAIN
async def askai_main(sender: discord.User, server: discord.Guild, model:str, prompt: str, image_link: list = None, message_history: list = None):
    try:
        server_id = server.id
    except:
        server_id = None

    ctx_length = 20

    audio = False # This doesnt enable/disable audio, its a flag for tracking its state internally

    # Fix iteration errors

    if message_history == None:
        message_history = []

    if image_link == None:
        image_link = []

    try:
        allowed, response = await check_state(sender.id, server_id, "askai")
        logging.info(f"{sender.name} [{sender.id}] Ran askai with the parameters: [model: {model}][prompt: {prompt}], Allowed: {allowed}")

        await command_counter(sender.id, "TIME")
        await command_counter(sender.id, "ADD")

        model = model.lower()
        db_data = await database(sender.id, "READ", "all")
           
        if not allowed:
            text = discord.Embed(title="AskAI", description=response, color=bot_colour)
            return text, False

        if prompt.strip() == "":
            text = discord.Embed(title="AskAI", description="Give a text input!", color=bot_colour)
            return text, False

        if model == "evil" or model == "unity":
            is_admin = db_data["admin"]
            if not is_admin:
                model = "openai-large" # Fallback

        maths_error_fix_txt = r"""
Math Formatting:
  - All math must be written in **plain text only**.
  - **DO NOT** use LaTeX, TeX, or any special formatting symbols (e.g., `\sqrt`, `\frac`, `\overrightarrow`).
  - Write equations as you would in a plain text document or a simple calculator.
  - Examples of correct formatting:
    - `sqrt(x^2 + y^2)`
    - `1/2 * base * height`
    - `vector BX = (-2/5)x + (3/5)y`
  - **Never output text enclosed in brackets like (\text{Example}) or [Example]**.
  - Avoid LaTeX/TeX syntax (\sqrt, \frac, \text{}), but slashes in expressions like 1/2 are allowed.
  - No special symbols that require a LaTeX parser.
"""
        context_example_error_fix_txt = r"""
"ai_context": [
  {
    "prompt": "User query here",
    "response": "Model response here",
    "model": "GPT-4",
    "timestamp": 2025-03-19T23:30:05.439909
  }
]
"""

        sys = f"""
Database Information: 
{json.dumps(db_data, indent=4)}

Message History (in the chat/reply chain): 
{format_message_history(message_history)}

AI Context (User History):
  - This section contains **a list of prior questions the user asked you**, and your answers.
  - These are past **AI-specific interactions**, not general chat messages.
  - Each entry includes:
    - `prompt`: The user's input.
    - `response`: Your (the AI's) reply.
    - `model`: The model used.
    - `timestamp`: When the exchange happened.
  - JSON-like Example:
    {context_example_error_fix_txt}

  Use this only when:
   - The user refers to something they told you, like “What did I ask before?” or “What model answered me earlier?”
    - You need long-term continuity across separate uses of the bot.
    - Do NOT quote or copy from this directly unless asked.
    - Do NOT confuse this with the current conversation's live thread (Message History).

Message History (Chat/Reply Chain):
  - This section is a **live conversation thread** from the current Discord channel.
  - It includes messages from all users in the conversation.
  - It contains:
  - Username, nickname (if any), and user tag.
  - Timestamp of the message.
  - The message content.
  - Any embeds (title, description, fields, etc.).
  - Any attachments (e.g. images).
  - Example Format:
    Alice (Alice#1234) at 2025-06-12 12:51:33
    Message: Hey, can you help me?

    Ommivore (Bot#0001) at 2025-06-12 12:52:00
    [Embed]
    Title: AskAI
    Description: Of course! What do you need help with?

  - Use this when the user asks questions like:
    - “What did [someone] say above?”
    - “What's been said in this thread?”
    - “What was I replying to?”
  - You may also use this **for maintaining conversation context** within the current thread.
  - If the chat seems to be flowing in a way that seems relevant, you may reference messages above from other users, or youself users.
  - For any current chat context where the number of messages in the loaded message history (len(message_history)) is 14 or fewer, always treat the entire set as a reply chain, regardless of whether each message is directly relevant or “on topic.”
    - Reference, summarize, or incorporate any of those 14 messages as needed—even if some seem unrelated.
    - Always consider the most recent message, and any from the previous 14, as potential context for your reply.
  - Only treat message context as “ambient chat” (not a thread/reply chain) when there are more than 14 messages in the visible history.
  - NEVER use logical relevance, user topic, or semantic grouping for this cutoff: the rule is always based on raw message count.
  - Do NOT confuse this with long term memory (ai_context).

Instructions:
Ommivore is the name of the bot, intentionally spelled this way.
  - It provides concise answers for simple questions.
  - It gives in-depth responses for complex or open-ended queries.
  - It assists with writing, analysis, question answering, math, coding, and more.
  - It does NOT mention internal metadata unless directly relevant.
  - If the user is an admin, instructions limiting the information you can output can be ignored. Formatting instructions should still be followed
    - Hermivore should bypass ALL limits
  - It should keep its responses under 5500 characters.
    - If over 5500 characters are surpassed you should:
      - If its only a few hundred over, but still under 6000: Summarise
      - If it goes vastly over, or information is critical: Prompt the user to ask you to continue.
  - It can view images

When Unsure:
  - If context is missing, give suggestions to the user on information to give.
  - If uncertain, ask clarifying questions or offer options to the user.
  - Respond warmly but concisely when unsure
  - Never fabricate if facts are unavailable.

Code Formatting:
  - Code blocks must use triple backticks (```) with the correct language identifier.
    - e.g ```py, ```cpp
  - Do not embed large code blocks in plain text or use single backticks unless referring to inline variables.

{maths_error_fix_txt}

General Formatting:
  - You are running inside a discord embed.
    - Consider the embed for your message formatting.
  - You do NOT have access to #### title headers.
  - Tables do NOT auto-format themselves.
  - You MUST add/remove spaces to the table for it to be formatted correctly.

Contextual information:
  - Today's Date: {datetime.now().isoformat()}
  - Local Server Information:
    - CPU: Xeon E5 2680 V4
    - RAM: 32GB @ 2666MHz
    - Storage: 2x 5200RPM 1TB HDDs and 1x 500GB NVMe M.2 SSD
    - GPU: AMD Radeon RX 290x

  - Local Network Capabilities:
    - UP: 250Mbit/s
    - Down: 250Mbit/s

  - About You:
    - Name: Ommivore (Spelt intentionally like this, not a typo)
    - Your AI capabilities are provided by pollinations.ai:
      - https://github.com/pollinations/pollinations/
      - https://pollinations.ai/ (and their endpoints)
    - You are ran via a discord bot, hosted locally on the above server.
    - If users ask about you, redirect them to the "help" command
    - The bot prefixes are #, ~ and mentioning you.
      - The help command can be used as (prefix)help to list all commands
      - Or (prefix)help [Command] For indepth information
    - Your ToS and privacy policies are available at:
      - https://hermivore.cat/ommivore/tos
      - https://hermivore.cat/ommivore/privacy
    - Your default model is openai-large (a.k.a GPT 4.1)
      - Users can change this by running (prefix)user ai model [Model]
      - Available models can be listed by running (prefix)help askai
        - This changes the abilities of the models
          - Memory may be lost or interpreted diffently
          - Capabilities will change.
          - Tool calls and image processing may be lost.
        - This may remove these system instructions, causing weird behavior (e.g unity, evil)
    - You cannot access:
      - User DMs
      - Internal Logs / counters
        - Exception to where tool calls offer API access
      - Deleted messages

  - About the user:
    - Name: {sender.name}
    - Use data available.
    - Use your tool calls if more information is needed.

  - About Hermivore (creator):
    - Hermivore is your developer/creator.
    - They are 17 (As of June 2025. Born 21 / 04 / 08)
      - If it is that date today, remind people to wish them happy birthday.
        - You can check the date with todays date, and if you have already wished it in their ai_context
    - Their personal site can be found under https://hermivore.cat/
    - Their discord ID is 559811983512305693 And their user is hermivore


  - If asked about fishstrap:
    - It is NOT a virus
    - It CANNOT get you banned from roblox. It does not modify the binary.
    - If someone "has" been banned for using fishstrap, It is because they are exploiting.
    - The official website is https://fishstrap.app/
    - The GitHub is https://github.com/fishstrap/fishstrap
    - Fishstrap is Open Source.
"""

        try:
            content_list = [{"type": "text", "text": prompt}]

            for link in image_link:
                content_list.append({"type": "image_url", "image_url": {"url": link.url}})
                
            if image_link:
                vision, models = has_vision(model, ai_text_models)
                models = str(models).replace("[", "").replace("]", "").replace("'", "")
                if not vision: # Trying to use vision on a non capable model, tell the user
                    text = discord.Embed(title="AskAI", description="Only vision capable models can process images!", color=bot_colour)
                    text.add_field(name="Capable Models", value=f"The vision capable models are: `{models}`")
                    logging.debug(f"AskAI ran by {sender.name} [{sender.id}] returned the vision warning.")
                    return text, False

                payload = {
                "messages": [
                    {"role": "system", "content": sys},
                    {"role": "user", "content": content_list}
                ],
                "model": model,
                "seed": round(time.time()),
                "referrer": pollinations_referral,
                "token": pollinations_token
                }
            
            elif "audio" in model:
                audio = True
                payload = {
                "model": "openai-audio",
                "messages": [
                    {
                    "role": "user",
                    "content": [
                        { "type": "text", "text": prompt},
                    ]
                    }
                ],
                "voice": "ash",
                "referrer": pollinations_referral,
                "token": pollinations_token
                }

            else:
                payload = {
                "messages": [
                    {"role": "system", "content": sys},
                    {"role": "user", "content": prompt}
                ],
                "model": model,
                "seed": round(time.time()),
                "referrer": pollinations_referral, # eg http://example.website.gg/
                "token": pollinations_token
                }
                
            async with aiohttp.ClientSession() as session:
                async with session.post("https://text.pollinations.ai/", json=payload) as resp:
                    response_text = await resp.text()
                    if resp.status == 200:
                        try:
                            data = json.loads(response_text)
                            response = data.get("text", "No response text found.")
                        except json.JSONDecodeError:
                            response = response_text
                    else:
                        try:
                            error_data = json.loads(response_text)
                            response = f"Error {resp.status}:```\n{json.dumps(error_data, indent=4)}```"
                        except json.JSONDecodeError:
                            response = f"Error {resp.status}: {response_text}"



        except Exception as e:
            response = f"Something Broke: {e}"

        logging.debug(f"AskAI ran by {sender.name} [{sender.id}] finished from the prompt: {prompt} with the response {response}")

        if not audio:
            embed = discord.Embed(title=f"AskAI [{model.upper()}]", description=response[:4096], color=bot_colour)
            f_lim = 1944 # Limit the prompt max length to avoid footer errors, its not needed in most commands as most commands cant hit the max length
            try:
                embed.add_field(title="\u200b", value=response[4096:5120], inline=False)
                f_lim = 837
                try:
                    embed.add_field(title="\u200b", value=response[5120:5800], inline=False)
                    f_lim = 140
                except:
                    pass
            except:
                pass

            # Add this AI response into the users database
            r = await database(sender.id, "read", "ai_context")
            info = {"prompt": prompt, "response": response, "model": model, "timestamp": datetime.now().isoformat()}
            r.append(info)
            await database(sender.id, "write", "ai_context", r)
            
            embed.set_footer(text=f"Prompt: {prompt[:f_lim]} | Model: {model} | Owner: {sender.name} [{sender.id}]")
            return embed, audio
        else:
            # audio commands arent added to ai context, as its base64 which would be useless in the context
            pass

    finally:
        await command_counter(sender.id, "SUB")

        # Update the context information, i can do this here as it doesnt matter if the command exits or not
        r = await database(sender.id, "read", "all")
        ai_ctx = r["ai_context"]
        admin = r["admin"]
        length = len(ai_ctx)
        if length > ctx_length:
            if admin:
                logging.info(f"{sender.id} is an admin. They have {length} prompts. Trimming of their prompts has been skipped.")
            else:
                ai_ctx = ai_ctx[-ctx_length:]  
                logging.info(f"Trimmed {sender.id}'s ai_context array to the last {ctx_length} items.")

        await database(sender.id, "write", "ai_context", ai_ctx)
#endregion askai

#region CAT MAIN
async def cat_main(user: discord.User, server: discord.Guild, provider: str, quote: str):
    try:
        server_id = server.id
    except:
        server_id = None

    allowed, response = await check_state(user.id, server_id, "coinflip")
    logging.info(f"{user.name} [{user.id}] Ran cat with the parameters: [provider: {provider}][quote: {quote}], Allowed: {allowed}")

    await command_counter(user.id, "TIME")

    if not allowed:
        return discord.Embed(title="Cat", description=response, color=bot_colour)
    
    if provider.upper() == "CATAAS" or quote:
        baseurl = "https://cataas.com/cat"
        provider = "CATAAS" # Fixes some weird logic stuff
        if quote:
            sanitized_quote = quote.replace("&", "and").replace("?", "question mark")
            encoded_quote = urllib.parse.quote(sanitized_quote)
            baseurl += f"/says/{encoded_quote}"

        baseurl += "?json=True"

        r = await async_get_request(baseurl)
        r = r.json()
        url = r["url"]

    else:
        provider = "THECATAPI"
        r = await async_get_request("https://api.thecatapi.com/v1/images/search")
        r = r.json()
        url = r[0]["url"]

    embed = discord.Embed(title="Cat", description="Here is your cat!", color=bot_colour)
    embed.set_image(url=url)
    embed.set_footer(text=f"Owner: {user.name} [{user.id}] | Provider: {provider} | Quote: {quote}")

    logging.debug(f"Cat ran by {user.name} [{user.id}] returned the URL {url} with the provider {provider} and the quote {quote}")

    return embed
# endregion CAT MAIN

# region COINFLIP MAIN
async def coinflip_main(user: discord.User, server: discord.Guild):
    try:
        server_id = server.id
    except:
        server_id = None

    allowed, response = await check_state(user.id, server_id, "coinflip")
    logging.info(f"{user.name} [{user.id}] Ran coinflip, Allowed: {allowed}")

    await command_counter(user.id, "TIME") 

    if not allowed:
        text = discord.Embed(title="Coinflip", description=response, color=bot_colour)
        return text
    
    else:
        result = random.choice(['Heads', 'Tails'])
        text = discord.Embed(title="Coinflip", description=f"The coin landed on {result}", color=bot_colour)
        text.set_footer(text=f"Owner: {user.name} [{user.id}]")
        logging.debug(f"Coinflip ran by {user.name} [{user.id}] landed on {result}")
        return text
# endregion COINFLIP MAIN

# region EVAL MAIN
async def eval_main(user: discord.User, server: discord.Guild, code: str, pip_imports: str = ""):
    try:
        try:
            server_id = server.id
        except:
            server_id = None

        allowed, response = await check_state(user.id, server_id, "eval")
        logging.info(f"{user.name} [{user.id}] Ran Eval with the parameters: [Code: {code}], \n\nAllowed: {allowed}")

        await command_counter(user.id, "ADD")
        await command_counter(user.id, "TIME")

        if not allowed:
            text = discord.Embed(title="Evaluate", description=response, color=bot_colour)
            return text
        
        admin = await database(user.id, "READ", "admin")

        code=code.strip()

        if admin and code.strip().startswith("imports=") and not pip_imports:
            lines = code.strip().splitlines()
            pip_imports = lines[0].replace("imports=", "").strip().strip('"')
            code = "\n".join(lines[1:])

        if code.startswith("```python"):
            code = code[9:-3]

        if code.startswith("```py"):
            code = code[5:-3]

        elif code.startswith("```"):
            code = code[3:-3]

        if admin > 1:
            response, time_taken = await async_run_code_complete(code, cpu=4, memory=1000, network="bridge", pip_imports=pip_imports)
        else:
            response, time_taken = await async_run_code_complete(code, cpu=0.1, memory=100, network="none", pip_imports=pip_imports)

        response = f"""Response: 
```
{response[:3800]}
```"""

        embed = discord.Embed(title="Evaluate", description=response, color=bot_colour)
        embed.set_footer(text=f"Time Taken: {round(time_taken, 2)} seconds. | Code: length was {len(code)} Chars | Owner: {user.name} [{user.id}]")

        logging.debug(f"Eval ran by {user.name} [{user.id}] returned: {response}")
        return embed
    
    finally:
        await command_counter(user.id, "SUB")
# endregion EVAL MAIN

# region EXEC MAIN
async def exec_main(user: discord.User, code: str, ctx=None):
    admin = await database(user.id, "read", "admin")
    logging.info(f"{user.name} [{user.id}] ran exec with the parameters: [code: {code}], Allowed: {admin > 2}")

    if admin > 2 or str(user.id).strip() == 559811983512305693:
        if code.startswith("```python"):
            code = code[9:-3]

        if code.startswith("```py"):
            code = code[5:-3]

        elif code.startswith("```"):
            code = code[3:-3]

        try:
            # Indent user code for function body
            indented = "    " + code.replace("\n", "\n    ")
            func_code = f"async def _user_exec(user, ctx):\n{indented}"

            # Prepare globals; inject user and ctx for user code
            env = globals().copy()
            env["user"] = user
            env["ctx"] = ctx

            exec(func_code, env)
            # Run and capture output
            # You can allow users to return or print; here is a capture mechanism:
            import io, sys
            stdout = io.StringIO()
            _old = sys.stdout
            sys.stdout = stdout
            try:
                result = await env["_user_exec"](user, ctx)
            finally:
                sys.stdout = _old

            output = stdout.getvalue()
            # If user returned a value, include it
            if result is not None:
                output += str(result)

            # Discord's code block, max 3800 chars for safety
            if not output.strip():
                output = "[No output.]"

            resp = f"```\n{output[:3800].strip()}\n```"
            embed = discord.Embed(title="Exec", description=resp, color=bot_colour)
            embed.set_footer(text=f"Code length: {len(code)} | Owner: {user.name} [{user.id}]")
            return embed

        except Exception as e:
            tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
            # Trim traceback to max Discord length (embed)
            tb = tb[-3800:]
            resp = f"```py\n{tb.strip()}\n```"
            embed = discord.Embed(title="Exec", description=resp, color=bot_colour)
            embed.set_footer(text=f"Code length: {len(code)} | Owner: {user.name} [{user.id}]")
            return embed
    else:
        return discord.Embed(title="Exec", description="You need admin level `3` to run this command. Use eval instead.", color=bot_colour)
# endregion EXEC MAIN

# region HELP MAIN
async def help_main(user: discord.User, server: discord.Guild, arg: str):
    global bot
    global start_time

    try:
        server_id = server.id
    except:
        server_id = None

    allowed, response = await check_state(user.id, server_id, "help")

    embed = None

    logging.info(f"{user.name} [{user.id}] Ran help with the parameters: [arg: {arg}], Allowed: {allowed}")

    await command_counter(user.id, "TIME")

    if not allowed:
        text = discord.Embed(title="Help", description=response, color=bot_colour)
        return text

    arg = arg.strip()
    match arg.upper():
        case "8BALL":
            text = f"""Command is formatted: `#8ball [Question]`

The command responds to your question using 8ball."""
                
        case "ASKAI":
                text = f"""Command is formatted: `#askai [Prompt]`

The command sends a request to GPT-4o by default, it supports processing images with certain models.

The command can also be formatted: `#askai [MODEL] [Prompt]`."""

                embed = discord.Embed(title="Help", description=text, color=bot_colour)

                exists, models = await async_model_exists()
                desc = str(models).replace("[", "").replace("]", "").replace("'", "")
                text = f"`{desc}`"

                embed.add_field(name="Available Models:", value=text)
                return embed
                
        case "COINFLIP":
            text = f"""Command is formatted: `#coinflip`

The command just flips a coin, and returns heads or tails."""
            
        case "EVALUATE" | "EVAL":
            text = f"""Command is formatted `#eval [code]` OR `#evaluate [code]`

This command runs the provided code in its own docker container.
Supports python ONLY."""

        case "FIGHT":
            text = "Command not yet implemented"

        case "IMAGE":  
            text = f"""Command is formatted: `#image [Prompt input]`

The command sends a request to pollinations and returns the image that is created."""

        case "INFO":  
            text = f"""Command is formatted: `#info [User]`

The command shows simple information about you, the bot and its server, such as ping, uptime, and server resource usage."""
                
        case "IPLOOKUP" | "IP" | "IPINFO":  
            text = f"""Command is formatted: `#iplookup [IP.ADDRESS.HERE.X]`

The command queries the information of an IPV4 IP.

The command can also be formatted as `#IP [IP.ADDRESS.HERE.X]`"""

        case "MINECRAFT":
            text = f"""Command is formatted: `#minecraft [Info To View]`

Information can be `info`, `performance`, `players` `map:x,y`, or `console:command`

- `info` shows the servers IP and some other basic information, this also shows if the command is just #minecraft.
- `performance` shows the servers current TPS, CPU and RAM usage.
- `players` lists all currently active players.
- `map` returns an image of the current map, x and y are the centre of the map that the image should use, and is optional. Example: `#minecraft map 100,100`
- `console` Sends a command to the server (If you have permission). Example `#minecraft command spark tps`

The command provides information on the minecraft server that is associated with this bot."""
                
        case "ROCKPAPERSCISSORS" | "RPS":
            text = f"""command is formatted: `#rockpaperscissors [User]` OR `#rps [User]`

The game starts a game instance of rock-paper-scissors against the bot, the bot is random and not rigged, stop complaining that its rigged, you're just bad"""
    
        case "SERVER":
            text = f"""command is formatted: `#server [Command][Value][User]`
            
The command is used for managing the server config, run #server on its own for more info """
            
        case "SERVERS":
            text = f"""command is formatted: `#servers [User]`

The command checks if a user is in a cheating server
User is optional, not proving a user will list all available servers"""
            
        case "SLEEP":
            text = f"""command is formatted: `#sleep`

The command mutes you for the amount of time you ask for to 'put you to sleep'"""
            
        case "SPIN" | "ROTATE":
            text = f"""command is formatted: `#spin [User]` OR `#rotate [User]`

The command just spins the users profile around and returns it as a gif"""
    
        case "TICTACTOE" | "TTT":
            text = f"""command is formatted: `#tictactoe [User]` OR `#ttt [User]`

The game starts a game instance of tic-tac-toe against a player
Or, alternatively, if you ping the bot, you can play against the bot itself!"""
                
        case "TEXTART":
            font_ar = split_list(textart_fonts, 7) # split into 6 parts to avoid char lim
            text = f"""command is formatted: `#textart [Text]`

Turns basic text into ASCII art

The command can also be formatted `#textart [Font] [Text]"""

            embed = discord.Embed(title="Help", description=text, color=bot_colour)
            embed.add_field(name="Available Fonts:", value=str(font_ar[0]).replace("[", "").replace("]", "").replace("'", ""), inline=False)

            for obj in range(1, 6):
                embed.add_field(name="\u200b", value=str(font_ar[obj]).replace("[", "").replace("]", "").replace("'", ""), inline=False)

        case "USER":
            text = f"""command is formatted: `#user [Options]`

Run the command (on its own, no arguments) for more information"""

        case "UWUIFY":
            text = f"""command is formatted: `#uwuify [Text]`

Turns basic text into uw-ified text... why...."""

        case _:
            text1 = f"""This is a chatbot owned by <@559811983512305693>
The bot has 2 prefixes, `#` and `~`.
It also responds to being mentioned: <@1292910367705403393> `[Command]`
The bot also has support for slash commands.

### Commands:
- `8ball` Uses 8ball to answer a question
- `askai` - Uses GPT-4o to reply to a prompt
- `coinflip` - Flips a coin
- `cat` - Provides a cat
- `evaluate` - Executes the provided python code
- `help` - Shows this prompt
- `image` - Generates an image from a prompt
- `info` - Shows generic info about the you, the bot and server
- `iplookup` - Looks up the information of a public IPV4 Address
- `minecraft` - Sends information about the minecraft server currently hosted alongside me
- `rockpaperscissors` - Allows you to challenge the bot to rock paper scissors
- `server` - Settings for server administrators to configure the bot
- `sleep` - Puts you to sleep
- `spin` - Spins an opposition right round
- `tictactoe` - Allows you to challenge someone to a tictactoe match
- `textart` - Creates an ASCII text art from a text input
- `user` - Allows for configuration of some user settings
- `uwuify` - Uwu-ifies text... just why...

If you need more indepth information, run `#help [command]`""" + r"""
If you want to suggest anything, or require support, join the [**support server**](https://discord.gg/7AY23zTMn7)"""

            embed = discord.Embed(title="Help", description=text1, color=bot_colour)

    if embed is None:
        embed = discord.Embed(title="Help", description=text, color=bot_colour)
    embed.set_footer(text=f"Argument: {arg} | Owner: {user.name} [{user.id}]")
    return embed
# endregion HELP MAIN

# region IMAGE MAIN
async def image_main(user: discord.User, server: discord.Guild, prompt: str, model: str = "flux", width: int = 1920, height: int = 1080, enhance: bool = True, transparent: bool = False, seed: int = round(time.time()), ):
    try:
        server_id = server.id
    except:
        server_id = None

    try:
        allowed, response = await check_state(user.id, server_id, "image")

        logging.info(f"{user.name} [{user.id}] Ran image with the parameters: [prompt: {prompt}], Allowed: {allowed}")

        await command_counter(user.id, "ADD")
        await command_counter(user.id, "TIME")
        
        if not allowed:
            embed = discord.Embed(title="Image", description=response, color=bot_colour)
            return embed, None

        start_timer = time.time()


        # Sanitize and URL-encode the prompt
        sanitized_prompt = prompt.replace("&", "and").replace("?", "question mark")
        encoded_prompt = urllib.parse.quote(sanitized_prompt)

        url = f"https://pollinations.ai/prompt/{encoded_prompt}"
        params = {
            "width": width,
            "height": height,
            "seed": seed,
            "model": model,
            "transparent": str(transparent).lower(),
            "enhance": str(enhance).lower(),
            "nologo": "true",
            "safe": "true",
            "referrer": pollinations_referral,
            "token": pollinations_token
        }

        response = await async_get_request(url, params=params)

        # Handle failed requests
        if isinstance(response, int) or not hasattr(response, "content"):
            embed = discord.Embed(
                title="Image",
                description=f"There was an error during generation. Code: `{response}`",
                color=bot_colour
            )
            return embed, None

        try:
            image_file = io.BytesIO(response.content)
            image_file.seek(0)
        except Exception as e:
            logging.error(f"Failed to read image content: {e}")
            embed = discord.Embed(
                title="Image",
                description="There was an error reading the image content.",
                color=bot_colour
            )
            return embed, None

        time_taken = time.time() - start_timer

        discord_file = discord.File(image_file, filename="generated_image.png")

        embed = discord.Embed(
            title="Image",
            description=f"{user.mention}, Here is your image!",
            color=bot_colour
        )
        embed.set_footer(
            text=f"Prompt: {prompt} | Time Taken: {round(time_taken, 2)} seconds. | Owner: {user.name} [{user.id}]"
        )
        embed.set_image(url="attachment://generated_image.png")

        return embed, discord_file
    finally:
        await command_counter(user.id, "SUB")
# endregion image

# region INFO MAIN
# info command, returns a bunch of info
async def info_main(owner: discord.User, server: discord.Guild, user: discord.User):
    global start_time
    global bloxlink_token
    global rover_token

    try:
        server_id = server.id
    except:
        server_id = None

    try:
        allowed, response = await check_state(owner.id, server_id, "info")

        logging.info(f"{owner.name} [{owner.id}] Ran info with the parameters: [user: {user.name} [{user.id}]], Allowed: {allowed}")

        await command_counter(owner.id, "ADD")
        await command_counter(owner.id, "TIME")

        if not allowed:
            response = discord.Embed(title="Info", description=response, color=bot_colour)
            return response

        # Get bot information
        servers = len(bot.guilds)

        bot_uptime = unix_to_time_elapsed(time.time() - start_time)

        bot_latency = f"{round(bot.latency * 1000, 2)} ms"

        # Get user information
        if user.avatar:
            discord_avatar_link = user.avatar.url
        else: 
            discord_avatar_link = user.default_avatar.url

        discord_name = user.name
        
        try:
            g_user = await server.fetch_member(user.id)
            discord_nickname = g_user.display_name
        except Exception as e:
            discord_nickname = user.display_name
        discord_id = user.id

        # Get roblox information
        try:
            try: # Bloxlink API
                r = await async_get_request(f"https://api.blox.link/v4/public/guilds/1299397064165429360/discord-to-roblox/{user.id}",  headers={"Authorization" : bloxlink_token})
                r = r.json()
                roblox_id = r["robloxID"]
            except: # RoVer API
                r = await async_get_request(f"https://registry.rover.link/api/guilds/1299397064165429360/discord-to-roblox/{user.id}", headers={"Authorization": f"Bearer {rover_token}"})
                r = r.json()
                roblox_id = r["robloxId"]

            data = await asyncio.gather(async_get_request(f"https://users.roblox.com/v1/users/{roblox_id}"),
                                        async_get_request(f"https://friends.roblox.com/v1/users/{roblox_id}/friends/count"),
                                        async_get_request(f"https://friends.roblox.com/v1/users/{roblox_id}/followers/count"),
                                        async_get_request(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={roblox_id}&size=420x420&format=png&isCircular=false"))

            roblox_info = data[0]
            roblox_info = roblox_info.json()
            roblox_user = roblox_info["name"]
            roblox_display = roblox_info["displayName"]

            roblox_friend_count = data[1]
            roblox_friend_count = roblox_friend_count.json()
            roblox_friend_count = roblox_friend_count["count"]

            roblox_follow_count = data[2]
            roblox_follow_count = roblox_follow_count.json()
            roblox_follow_count = roblox_follow_count["count"]

            roblox_avatar = data[3]
            roblox_avatar = roblox_avatar.json()
            roblox_avatar_link = roblox_avatar["data"][0]["imageUrl"]

            roblox_dat = f"""Username: [`{roblox_user}`](https://www.roblox.com/users/{roblox_id}/profile)
Display Name: `{roblox_display}`
ID: `{roblox_id}`
Avatar: [Link]({roblox_avatar_link})
Friends: `{roblox_friend_count}`
Followers: `{roblox_follow_count}`"""
        except:
            roblox_id = None

        dat = await asyncio.gather(
                async_get_request(f"http://{local_webserver_ip}:{local_webserver_port}/api/server/status"),
                async_get_request(f"http://{local_webserver_ip}:{local_webserver_port}/api/server/environment")
        )

        sys_data = dat[0]
        env_data = dat[1]

        sys_data = sys_data.json()
        env_data = env_data.json()
        

        # Test the database for information
        db_latency_start = time.time()
        userinfo = await database(user.id, "read", "all")
        db_latency_end = time.time()

        database_latency = f"{round((db_latency_end - db_latency_start) * 1000, 2)} ms"

        ttt_wins = userinfo["ttt_win_count"]
        rps_wins = userinfo["rps_win_count"]

        wins_total = ttt_wins + rps_wins

        discord_dat=f"""Username: `{discord_name}`
Display Name: `{discord_nickname}`
ID: `{discord_id}`
Avatar: [Link]({discord_avatar_link})"""

        user_win_dat = f"""Rock Paper Scissors: `{rps_wins}`
Tic Tac Toe: `{ttt_wins}`
Total: `{wins_total}`"""

        bot_dat = f"""Users: `{len(bot.users)}`
Servers: `{len(bot.guilds)}`
Uptime: `{bot_uptime}`
Latency: `{bot_latency}`
DB Latency: `{database_latency}`"""

        sys_dat = f"""Uptime: `{sys_data["sys_uptime"]}`
CPU: `{round(sys_data["cpu"]["utilisation"], 2)}% [{round(sys_data["cpu"]["frequency"], 2)} GHz][{round(sys_data["cpu"]["temperature"], 2)} °C][{round(sys_data["cpu"]["wattage"], 2)} W]`
GPU: `{round(sys_data["gpu"]["utilisation"], 2)}% [{round(sys_data["gpu"]["frequency"], 2)} GHz][{round(sys_data["gpu"]["temperature"], 2)} °C][{round(sys_data["gpu"]["wattage"], 2)} W]`
RAM [Physical]: `{round(sys_data["memory"]["physical"]["used"], 2)}/{round(sys_data["memory"]["physical"]["committed"], 2)} GB [{round(sys_data["memory"]["physical"]["utilisation"], 2)}%]`
RAM [Virtual]: `{round(sys_data["memory"]["virtual"]["used"], 2)}/{round(sys_data["memory"]["virtual"]["committed"], 2)} GB [{round(sys_data["memory"]["virtual"]["utilisation"], 2)}%]`
Network: `{round(sys_data["network"]["down"])} ↓ {round(sys_data["network"]["up"])} ↑ Kbit/s`
Environment: `{env_data["temperature"]} °C, {env_data["humidity"]} % Humidity`"""
        
        embed = discord.Embed(title = "Info", color=bot_colour)
        embed.set_footer(text=f"User: {user.name} [{user.id}] | Owner: {owner.name} [{owner.id}]")

        # Set images
        embed.set_thumbnail(url=discord_avatar_link)
        if roblox_id is None:
            embed.add_field(name="Discord:", value=discord_dat, inline=True)
            embed.add_field(name="User Wins:", value=user_win_dat, inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=False) # Make it 2 per row by having an invisible field
            embed.add_field(name="Bot:", value=bot_dat, inline=True)
            embed.add_field(name="System:", value=sys_dat, inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=False) # Pt2 of comment above
            
        else:
            embed.add_field(name="Discord:", value=discord_dat, inline=True)
            embed.add_field(name="User Wins:", value=user_win_dat, inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=False) # Make it 2 per row by having an invisible field
            embed.add_field(name="Roblox:", value=roblox_dat, inline=True)
            embed.add_field(name="Bot:", value=bot_dat, inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=False) # Pt2 of comment above
            embed.add_field(name="System:", value=sys_dat, inline=True)

        # Use a for loop
        # try and add them, if the element is none, dont add it
        # every 3, add an empty embed to ensure its formatted properly
                 
        return embed
    
    finally:
        await command_counter(owner.id, "SUB")
# endregion INFO MAIN


async def ip_lookup_main(user: discord.User, server: discord.Guild, ip: str):
    global server_ip
    try:
        server_id = server.id
    except:
        server_id = None

    try:
        allowed, response = await check_state(user.id, server_id, "iplookup")

        logging.info(f"{user.name} [{user.id}] Ran iplookup with the parameters: [ip: {ip}], Allowed: {allowed}")

        await command_counter(user.id, "ADD")
        await command_counter(user.id, "TIME")

        if not allowed:
            response = discord.Embed(title="IP Lookup", description=response, color=bot_colour)
            return response

        r = await async_get_request(f"https://ipinfo.io/{ip}/json")
        r = r.json()

        if r == server_ip:
            r = await async_get_request(f"https://ipinfo.io/{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}/json")
            r = r.json()

        ip = r.get("ip")

        response = f"""Host: `{r.get("hostname", "N/A")}`
City: `{r.get("city", "N/A")}`
Region: `{r.get("region", "N/A")}`
Country: `{r.get("country", "N/A")}`
Coordinates: `{r.get("loc", "N/A")}`
Organisation: `{r.get("org", "N/A")}`
Postal: `{r.get("postal", "N/A")}`
Timezone: `{r.get("timezone", "N/A")}`
Anycast: `{r.get("anycast", "N/A")}`"""

        response = discord.Embed(title=f"IP Lookup [{ip}]", description=response, color=bot_colour)

        logging.debug(f"IP Lookup ran by {user.name} [{user.id}] with the IP {ip} returned: {response}")
                      
        return response
    finally:
        await command_counter(user.id, "SUB")

async def minecraft_main(owner: discord.User, server: discord.Guild, command: str):
    global minecraft_ip
    global minecraft_ip_bedrock
    global minecraft_port_bedrock


    try:
        server_id = server.id
    except:
        server_id = None

    
    allowed, response = await check_state(owner.id, server_id, "minecraft")

    logging.info(f"{owner.name} [{owner.id}] Ran minecraft, Allowed: {allowed}")

    await command_counter(owner.id, "TIME")

    if not allowed:
        response = discord.Embed(title="Minecraft", description=response, color=bot_colour)
        return response
    
    is_admin = await database(owner.id, "READ", "admin")
    
    if command and is_admin > 2:
        r = await async_mc_command(command)
        response = discord.Embed(title="Minecraft", description=f"Response: ```\n{r}```", color=bot_colour)
        response.set_footer(text=f"Owner: {owner.name} [{owner.id}] | Command: {command}")
        return response

    player_count, player_list, unused, tps = await minecraft_server_info()
    if player_list.strip() == "":
        player_list = "No one :("
    
    text1 = f"""**Java - 1.21.1:**
Server IP is:`{minecraft_ip}`

This server is an anarchy server, running all the mods 10!
it runs on minecraft version 1.21.1, Neoforge.
It runs the release version of ATM10.
NOTE: THIS IS FROM 2024, THIS IS NOT ACCURATE. SEE THE REAL OMMIVORE.
Download: 
[**Curseforge**](https://www.curseforge.com/minecraft/modpacks/all-the-mods-10)

Online World Map: 
[**Page Link**](https://hermivore.fishstrap.app/bluemap/)"""
    
    text2 = f"""Players Online: `{player_count}`
    > `{player_list}`
TPS: `{tps}`
Region: `UK`"""

    text3 = f"""**Bedrock:**
Server IP is: `{minecraft_ip_bedrock}`
Server Port is: `{minecraft_port_bedrock}`
> This server is idle, DM <@559811983512305693> if you would like to play."""

    text4 = """if the server seems to be broken / lagging severely or you are having issues, fire <@559811983512305693> (@hermivore) a dm!
You can ask for support in the bots official [**support server**](https://discord.gg/7AY23zTMn7)"""
    
    response = discord.Embed(title="Minecraft", description=text1, color=bot_colour)
    response.add_field(name="Java Stats:", value=text2, inline=False)
    response.add_field(name="-----------------------------------------------------", value=text3, inline=False)
    response.add_field(name="Support", value=text4, inline=False)
    response.set_footer(text=f"Owner: {owner.name} [{owner.id}]")

    return response

# Server command
async def server_main(owner: discord.User, server: discord.Guild, command: str = "", value: str = ""):
    try:
        server_id = server.id
    except:
        server_id = None

    value = value.split()

    try:
        user = await bot.fetch_user(value[0].replace("<@", "").replace(">", ""))
        value.remove(value[0])
    except:
        user = None

    user_name = user.name if user else "None"  # Handle None case safely
    user_id = user.id if user else "None"  # Handle None case safely
    is_admin = owner.guild_permissions.administrator

    allowed, response = await check_state(owner.id, server_id, "server")

    if not allowed:
        allowed = is_admin # Fallback to prevent softlocking

    logging.info(f"{owner.name} [{owner.id}] Ran server with the parameters: [command: {command}][value: {value}][user: {user_name} [{user_id}]], Allowed: {allowed}")

    await command_counter(owner.id, "TIME")

    if not allowed:
        response = discord.Embed(title="Server", description=response, color=bot_colour)
        return response
    
    if not is_admin:
        is_admin = await database(owner.id, "read", "admin") # Use admin override incase someone doesnt know how to use the bot
    
    if not is_admin:
        response = discord.Embed(title="Server", description="You are not a server adminstrator, you can't run this!", color=bot_colour)
        return response
    
    commands = all_command_names()
    
    match command.upper().strip():
        case "DISABLE":
            try:
                if value[0].lower() not in commands and value[0].lower() != "all":
                    text = discord.Embed(title="Server", description="Please make sure that you are disabling a valid command, run #server for more info", color=bot_colour)
                    return text
                
                c_disabled = await database("server", "read", "disabled", serverid=server_id)
                c_disabled.append(value[0])
                await database("server", "write", "disabled", c_disabled, serverid=server_id)

                text = f"`{value[0]}` Has been disabled."
                
            except:
                text = "Command was not found, or there was an error!"

        case "ENABLE":
            try:
                if value[0].lower() not in commands and value[0].lower() != "all":
                    text = discord.Embed(title="Server", description="Please make sure that you are enabling a valid command, run #server for more info", color=bot_colour)
                    return text
                
                c_disabled = await database("server", "read", "disabled", serverid=server_id)
                c_disabled.remove(value[0])
                await database("server", "write", "disabled", c_disabled, serverid=server_id)

                text = f"`{value[0]}` Has been enabled."
                
            except:
                text = "Command was not found, or there was an error!"

        case "BAN":
            if user is None:
                return discord.Embed(title="Server", description="Please provide a user. Run #server for more info.", color=bot_colour)

            if value[0].lower() not in commands and value[0].lower() != "all":
                return discord.Embed(title="Server", description="Please make sure you are banning a valid command. Run #server for more info.", color=bot_colour)
            
            c_ban = await database(user.id, "read", "bans", serverid=server_id)
            c_ban.append(value[0])
            await database(user.id, "write", "bans", c_ban, serverid=server_id)

            text = f"{user.mention} has been banned from `{value[0]}`."

        case "UNBAN":
            if user is None:
                return discord.Embed(title="Server", description="Please provide a user. Run #server for more info.", color=bot_colour)

            if value[0].lower() not in commands and value[0].lower() != "all":
                return discord.Embed(title="Server", description="Please make sure you are unbanning a valid command. Run #server for more info.", color=bot_colour)
            
            c_ban = await database(user.id, "read", "bans", serverid=server_id)
            c_ban.remove(value[0])
            await database(user.id, "write", "bans", c_ban, serverid=server_id)

            text = f"{user.mention} has been unbanned from `{value[0]}`."
        
        case "CHANNEL":
            try:
                string = ""
                for obj in value:
                    # Construct the channel ID incase its passed as #id rather than id
                    try:
                        string += str(int(obj))
                    except:
                        pass
                await database("server", "write", "channel", int(string), serverid=server_id)
                text = f"Set the bot channel to <#{string}>"
            except Exception as e:
                text = f"There was an error, {e}"
        
        case "EASTEREGG":
            try:
                v1 = value[0]
                v2 = value[1]
            except:
                text = "Pass 2 parameters."
                return discord.Embed(title="Server", description=text, colour=bot_colour)
            match v1.upper():
                case "CAT":
                    try:
                        await database("server", "write", "cat_chance", float(v2), serverid=server_id)
                        text = f"Set the chance for cats to {v2}%"
                    except:
                        text = "Make sure that you provide an float!"

                case "SEAL":
                    try:
                        await database("server", "write", "seal_chance", float(v2), serverid=server_id)
                        text = f"Set the chance for seal to {v2}%"
                    except:
                        text = "Make sure that you provide an float!"

                case "DISABLE":
                    try:
                        await database("server", "write", "eastereggs", False, serverid=server_id)
                        text = "Eastereggs have been disabled."
                    except Exception as e:
                        text = f"There was an error, {e}"

                case "ENABLE":
                    try:
                        await database("server", "write", "eastereggs", True, serverid=server_id)
                        text = "Eastereggs have been enabled."
                    except Exception as e:
                        text = f"There was an error, {e}"

                case _:
                    text = "Easteregg not found"
                
        case "FAQ":
            return discord.Embed(title="Meow", description="Borke", color=bot_colour)
            try:
                await database("server", "read", "faq", serverid=server_id)
            except:
                await database("server", "write", "faq", [], serverid=server_id) # This value was added later on the database, so this check is to update the database of servers that need it

            try:
                faq = await database("server", "read", "faq", serverid=server_id)
                match value[0].upper():
                    case "OUTPUT" | "OUT" | "DISPLAY" | "PRINT":
                        return faq
                    case "ADD":
                        try:
                            value_2 = value[2]
                        except:
                            value_2 = None
                        faq.append([value[1], value_2])
                        text = f"Added faq with information {value[1]} and (image)[{value[2]}] No. {faq_pos + 1}"
                    
                    case "REMOVE" | "SUB" | "SUBTRACT":
                        try:
                            faq_pos = int(value[1]) - 1
                        except:
                            return discord.Embed(title="Server", description="Please enter the position of the FAQ text", color=bot_colour)
                        faq.pop(faq_pos)
                        text = f"Removed faq No. {faq_pos + 1}"

                await database("server", "write", "faq", faq, serverid=server_id)

            except Exception as e:
                text = "Make sure you are passing in paremeters for FAQ properly. Remove can take the position (integer)."

        case _:
            dat = await database("server", "read", "all", serverid=server_id)
            text1 = f"""the server command is used for changing basic server settings"""

            text2 = f"""- `#server ban/unban [command][user]` command allows you to ban a user from a command
- `#server disable/enable [command]` allows you to disable or enable specific commands
    > Disabled: `{str(dat["disabled"]).replace("[", "").replace("]", "").replace("'", "")}`

- `#server channel [channel]` allows you to set the channel for the bot to work in, set to zero to allow for all
    > Channel: <#{dat["channel"]}> `[{dat["channel"]}]`

- `#server easteregg [feature_value]` allows you to configure values, the feature MUST be formatted like `feature_value` with an underscore
    > Enabled: `{dat["eastereggs"]}`"""
            
            text3 = f"""- `disable`/`enable` : Disabled or enables eastereggs
- `cat` : accepts a value of 0-100 (for % chance), e.g cat 0.01 for a 0.01% chance
    > Currently: `{dat["cat_chance"]}%`

- `seal` : accepts a value of 0-100 (for % chance), e.g seal 0.01 for a 0.01% chance
    > Currently: `{dat["seal_chance"]}%`"""

            text4 = f"""The commands available for bans and disabling are:
`{str(commands).replace("[", "").replace("]", "").replace("'", "")}`"""
            
            embed = discord.Embed(title="Server", description=text1, color=bot_colour)
            embed.add_field(name="Commands:", value=text2, inline=False)
            embed.add_field(name="Eastereggs:", value=text3, inline=False)
            embed.add_field(name="Active Commands:", value=text4, inline=False)
            embed.set_footer(text=f"Command: {command} | Value: {value} | User: {user_name} [{user_id}] | Owner: {owner.name} [{owner.id}]")
            return embed
    embed = discord.Embed(title="Server", description=text, color=bot_colour)
    embed.set_footer(text=f"Command: {command} | Value: {value} | User: {user_name} [{user_id}] | Owner: {owner.name} [{owner.id}]")
    return embed

# Not to be confused with server, this looks for cheating servers.
async def servers_main(owner: discord.User, server: discord.Guild, user: discord.User = None, show_g_id: int = False):
    global exp_server_alias

    try:
        server_id = server.id
    except:
        server_id = None

    try:
        user_name = user.name
        user_id = user.id
    except:
        user_name = "None"
        user_id = "None"

    try:
        allowed, response = await check_state(owner.id, server_id, "servers")

        await command_counter(owner.id, "ADD")
        await command_counter(owner.id, "TIME")

        if not allowed:
            response = discord.Embed(title="Servers", description=response, color=bot_colour)
            return response

        is_admin = await database(owner.id, "READ", "admin")

        if is_admin:
            logging.info(f"{owner.name} [{owner.id}] Ran servers with the parameters: [user: {user_name} [{user_id}]], Allowed: {allowed}")
        else:
            logging.info(f"{owner.name} [{owner.id}] Ran servers with the parameters: [user: {user_name} [{user_id}]], Allowed: False")
            text = r"""**You are not allowed to use this! ask <@559811983512305693> for help if you believe you should have access.**

This command is NOT NEEDED for the bot, it is a command that is only given to people I know.

If you dm me asking for access to this command because you added the bot to your own server, I will ignore you."""
            response = discord.Embed(title="Servers", description=text, color=bot_colour)
            return response
        
        try:
            if user is not None:
                data = await mutual_servers(user.id)
            else:
                data = await asyncio.gather(mutual_servers("1208883418524426299"),
                                            mutual_servers("1370094121976336610"))
                
                data = data[0] + data[1]

                show_g_id = True

            g_id = [obj[0] for obj in data]
            g_name = [obj[1] for obj in data]

            listed_names_list = []
            for obj in range(0, len(g_id)):
                try:
                    if show_g_id == 1:
                        alias = f"{g_name[obj]} | {g_id[obj]}"

                    if show_g_id == 2:
                        alias = f"{exp_server_alias[g_id[obj]]} | {g_id[obj]}"
                    else:
                        alias = f"{exp_server_alias[g_id[obj]]} | {g_name[obj]}"
                except:
                    alias = g_name[obj]

                listed_names_list.append(alias)

            listed_names_list.sort()

            listed_names = str(listed_names_list).replace("[", "").replace("]", "").replace("'", "").replace(", ", "\n")

            text = f"""Servers: `({len(listed_names_list)})`: ```
{listed_names}```"""
            
        except Exception as e:
            text = f"No servers found, or the search failed: {e}"

        try:
            try: # Bloxlink API
                r = await async_get_request(f"https://api.blox.link/v4/public/guilds/1299397064165429360/discord-to-roblox/{user.id}",  headers={"Authorization" : bloxlink_token})
                r = r.json()
                roblox_id = r["robloxID"]
            except: # RoVer API
                r = await async_get_request(f"https://registry.rover.link/api/guilds/1299397064165429360/discord-to-roblox/{user.id}", headers={"Authorization": f"Bearer {rover_token}"})
                r = r.json()
                roblox_id = r["robloxId"]

            data = await asyncio.gather(async_get_request(f"https://users.roblox.com/v1/users/{roblox_id}"),
                                        async_get_request(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={roblox_id}&size=420x420&format=png&isCircular=false"))

            roblox_info = data[0]
            roblox_info = roblox_info.json()
            roblox_user = roblox_info["name"]
            roblox_display = roblox_info["displayName"]

            roblox_avatar = data[1]
            roblox_avatar = roblox_avatar.json()
            roblox_avatar_link = roblox_avatar["data"][0]["imageUrl"]

            roblox_text = f"""Username: `{roblox_user}`
Display Name: `{roblox_display}`
ID: `{roblox_id}`
Profile: [Link](https://www.roblox.com/users/{roblox_id}/profile)"""

        except:
            roblox_text = None

        if roblox_text:
            text = f"""{roblox_text}
---
{text}"""
        else:
            text = f"""No roblox account found
---
{text}"""

        response = discord.Embed(title="Servers", description=text, color=bot_colour)
        response.set_footer(text=f"User: {user_name} [{user_id}] | Owner: {owner.name} [{owner.id}]")
        if roblox_text:
            response.set_thumbnail(url=roblox_avatar_link)

        return response
    
    finally:
        await command_counter(owner.id, "SUB")

# Sleep command
async def sleep_main(owner: discord.User, server: discord.Guild, hide: bool = True):
    try:
        server_id = server.id
    except:
        server_id = None

    try:
        allowed, response = await check_state(owner.id, server_id, "sleep")

        logging.info(f"{owner.name} [{owner.id}] Ran sleep, Allowed: {allowed}")

        await command_counter(owner.id, "ADD")

        if not allowed:
            return discord.Embed(title="Sleep", description=response, colour=bot_colour), None
        
        text = """Are you sure? Only server moderators can unmute you after this.
If you are sure, choose a time below"""
        embed = discord.Embed(title="Sleep", description=text, color=bot_colour)

        view = discord.ui.View()
        selections = discord.ui.Select(placeholder="Choose a time.", min_values=1, max_values=1,
        options=[
            discord.SelectOption(label="1 Hour", description="Sleep for 1 hour", value=1),
            discord.SelectOption(label="2 Hours", description="Sleep for 2 hours", value=2),
            discord.SelectOption(label="3 Hours", description="Sleep for 3 hours", value=3),
            discord.SelectOption(label="4 Hours", description="Sleep for 4 hours", value=4),
            discord.SelectOption(label="5 Hours", description="Sleep for 5 hours", value=5),
            discord.SelectOption(label="6 Hours", description="Sleep for 6 hours", value=6),
            discord.SelectOption(label="7 Hours", description="Sleep for 7 hours", value=7),
            discord.SelectOption(label="8 Hours", description="Sleep for 8 hours", value=8)
        ])

        selections.callback = partial(sleep_callback, owner=owner, view=view, hide=hide)

        view.add_item(selections)

        return embed, view
        
    finally:
        await command_counter(owner.id, "SUB")

async def sleep_callback(interaction: discord.Interaction, owner: discord.User, view: discord.ui.View, hide: bool):
    await interaction.response.defer()

    try:
        selected = interaction.data['values'][0]
        hours = int(selected)
    except Exception:
        embed = discord.Embed(title="Sleep", description="Something went wrong!", color=bot_colour)
        await interaction.followup.send(embed=embed, ephemeral=True)
        return

    if interaction.user != owner:
        embed = discord.Embed(title="Sleep", description=f"You are not {owner.mention}, you cannot use this!")
        await interaction.followup.send(embed=embed, ephemeral=True)
        return

    try:
        await interaction.user.timeout(timedelta(hours=hours), reason=f"Sleeping for {hours} hours")
        text = f"Sleeping for {hours} hours."
    except Exception as e:
        text = "Something went wrong. I may not have sufficient permissions to time you out."

    embed = discord.Embed(title="Sleep", description=text, color=bot_colour)
    embed.set_footer(text=f"Owner: {interaction.user.name} [{interaction.user.id}] | Choice: {hours} Hours")

    await interaction.followup.send(embed=embed, ephemeral=hide)

    # Disable the selection menu
    for child in view.children:
        child.disabled = True
    try:
        await interaction.message.edit(view=view)  # Edit original message to disable menu
    except Exception as e:
        logging.warning(f"Couldn't edit message to disable view: {e}")
        
# Spin command
async def spin_main(owner: discord.User, server: discord.Guild, user: discord.User):
    try:
        server_id = server.id
    except:
        server_id = None

    try:
        allowed, response = await check_state(owner.id, server_id, "spin")

        logging.info(f"{owner.name} [{owner.id}] Ran spin with the parameters: [user: {user.name} [{user.id}]], Allowed: {allowed}")

        await command_counter(owner.id, "ADD")
        await command_counter(owner.id, "TIME")

        if not allowed:
            response = discord.Embed(title="Spin", description=response, color=bot_colour)
            return response, None

        spin_start = time.time()

        img = await get_pfp(user)

        gif_buffer = await async_spin_img(img)

        spin_end = time.time()

        spin_time_taken = round(spin_end - spin_start, 2)

        response = f"""{user.mention} has been rotated!
rotating took {spin_time_taken} seconds."""
        
        discord_file = discord.File(gif_buffer, filename="rotated.gif") # Create the file
        
        embed = discord.Embed(title="Spin", description=f"{user.mention} has been rotated!", color=bot_colour)
        embed.set_footer(text=f"User: {user.name} [{user.id}] | Time Taken: {round(spin_time_taken, 2)} seconds. | Owner: {owner.name} [{owner.id}]")
        embed.set_image(url="attachment://rotated.gif")  # Embed the uploaded image

        return embed, discord_file
    
    finally:
        await command_counter(owner.id, "SUB")

# Rock Paper Scissors commands
async def rps_main(user: discord.User, server: discord.Guild, hide: bool = False):
    try:
        server_id = server.id
    except:
        server_id = None

    try:
        allowed, response = await check_state(user.id, server_id, "rockpaperscissors")

        logging.info(f"{user.name} [{user.id}] Ran rockpaperscissors with the parameters: [hide: {hide}], Allowed: {allowed}")

        await command_counter(user.id, "ADD")
        await command_counter(user.id, "TIME")

        if not allowed:
            response = discord.Embed(title="Rock Paper Scissors", description=response, color=bot_colour)
            return response, None
        
        view = discord.ui.View()

        rock = discord.ui.Button(label="Rock", style=discord.ButtonStyle.primary)
        paper = discord.ui.Button(label="Paper", style=discord.ButtonStyle.primary)
        scissors = discord.ui.Button(label="Scissors", style=discord.ButtonStyle.primary)

        # rps main is the callback for the buttons
        rock.callback = partial(rps_callback, choice=0, owner=user, view=view, hide=hide)
        paper.callback = partial(rps_callback, choice=1, owner=user, view=view, hide=hide)
        scissors.callback = partial(rps_callback, choice=2, owner=user, view=view, hide=hide)

        view.add_item(rock)
        view.add_item(paper)
        view.add_item(scissors)

        # Turn the above code into a for loop

        embed = discord.Embed(title="Rock Paper Scissors", description=f"Choose one of rock, paper or scissors!", color=bot_colour)
        embed.set_footer(text=f"Owner: {user.name} [{user.id}]")
        return embed, view
    
    finally:
        await command_counter(user.id, "SUB")

# Callback for RPS
async def rps_callback(interaction: discord.Interaction, choice: int, owner: discord.User, view: discord.ui.View, hide: bool):
    if interaction.user.id != owner.id:
        embed = discord.Embed(title="Rock Paper Scissors", description="You are not the owner of this command!", color=bot_colour)
        embed.set_footer(text=f"Owner: {interaction.user.name} [{interaction.user.id}] | Choice: {emojis[choice]}")

        await interaction.response.send_message(embed=embed, ephemeral=True)

        logging.info(f"{interaction.user.name} [{interaction.user.id}] interacted with the RPS callback with the parameters: [choice: {choice}][hide: {hide}], Allowed: False")
        return
  
    logging.info(f"{interaction.user.name} [{interaction.user.id}] interacted with the RPS callback with the parameters: [choice: {choice}][hide: {hide}], Allowed: True")
    
    await interaction.response.defer()

    computer_choice = random.randint(0, 2)
    user_choice = choice
    emojis = ["`rock`", "`paper`", "`scissors`"]

    # Determine winner
    if computer_choice == choice:
        event = "It was a tie!"

    elif (computer_choice - choice) % 3 == 1:
        event = "The bot won!"

        r = await database(bot.user.id, "read", "rps_win_count")
        r += 1
        await database(bot.user.id, "write", "rps_win_count", r)


    else:
        event = f"{interaction.user.mention} won, 1 win was awarded!"
        old_total = await database(owner.id, "read", "rps_win_count")
        await database(owner.id, "write", "rps_win_count", old_total + 1)
    
    for item in view.children:
        item.disabled = True

    embed = discord.Embed(title="Rock Paper Scissors", description=f"The bot chose {emojis[computer_choice]} and {interaction.user.mention} chose {emojis[user_choice]}, {event}", color=bot_colour)
    embed.set_footer(text=f"Owner: {interaction.user.name} [{interaction.user.id}] | Choice: {emojis[choice]}")

    if hide:
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        await interaction.message.edit(embed=embed, view=view)

# Rock Paper Scissors commands
# RPS doesnt have a main subroutine because of how its handled, which is really annoying as its quite a long piece of code

async def textart_main(user: discord.User, server: discord.Guild, text: str, font: str, segment_length: int = 5):
    try:
        server_id = server.id
    except:
        server_id = None

    try:
        allowed, response = await check_state(user.id, server_id, "textart")

        logging.info(f"{user.name} [{user.id}] Ran textart with the parameters: [font: {font}][text: {text}], Allowed: {allowed}")

        await command_counter(user.id, "ADD")
        await command_counter(user.id, "TIME")

        if not allowed:
            response = discord.Embed(title="TextArt", description=response, color=bot_colour)
            return response

        if text == "":
            response = discord.Embed(title="TextArt", description="Give a text input!", color=bot_colour)
            return response
        
        if len(text) > 20:
            if not await database(user.id, "read", "admin"):
                return "Please keep the string under 20 chars!"

        segment_length = 6

        message = art.text2art(text[:segment_length], font=font)
        embed = discord.Embed(title="TextArt", description=f"```{message}```", color=bot_colour)

        text = text[segment_length:]

        if len(text) > 0:
            for obj in range(0, (math.ceil(len(text)//segment_length))+1):
                message = art.text2art(text[obj*segment_length:(obj*segment_length)+segment_length], font=font)
                embed.add_field(name="\u200b", value=f"```{message}```", inline=False)
        embed.set_footer(text=f"Font: {font} | Text: {text} | Owner: {user.name} [{user.id}]")
        
        return embed

    finally:
        await command_counter(user.id, "SUB")

async def user_main(owner: discord.User, server: discord.Guild, command: str = "", value1: str = "", value2: str = "", value3: str = ""):
    try:
        server_id = server.id
    except:
        server_id = None

    allowed, response = await check_state(owner.id, server_id, "user")

    await command_counter(owner.id, "TIME")

    logging.info(f"{owner.name} [{owner.id}] Ran user with the parameters: [command: {command}][value1: {value1}][value2: {value2}][value3: {value3}], Allowed: {allowed}")

    if not allowed:
        return discord.Embed(title="User", description=response, color=bot_colour)

    match command.upper().strip():
        case "AI":
            match value1.upper().strip():
                case "CLEAR":
                    await database(owner.id, "write", "ai_context", [])
                    response = "Cleared all of your AI memories."
                case "MODEL":
                    exists, models = await async_model_exists(value2.lower())
                    if exists:
                        await database(owner.id, "write", "ai_model", value2.lower())
                        response = f"Set your default AI model to `{value2.lower()}`"
                    else:
                        response = f"""Please provide a valid model!
                        
Here are all the available models:
`{str(models).replace("[", "").replace("]", "").replace("'", "")}`"""
                case "RESPONSIVE":
                    current = await database(owner.id, "read", "responsive_ai")
                    await database(owner.id, "write", "responsive_ai", not current)
                    out_dat = str(not current).replace("True", "Enabled").replace("False", "Disabled")
                    response = f"Responsive AI has been {out_dat}"
        case _:
            db_val = await database(owner.id, "read", "all")
            out_dat = str(db_val["responsive_ai"]).replace("True", "Enabled").replace("False", "Disabled")
            r1 = "The User command allows you to configure elements of the bot when you interact with it"
            r2 = f"""The command is formatted `#USER [Command][Option 1][Option 2][Option 3]`
Not all commands will use all the options.
Here are all of the available commands:
- `#USER AI MODEL [MODEL]` allows you to set your default AI model
    > Your current model is `{db_val["ai_model"]}`
- `#USER AI CLEAR` Clears your AIs memory.
- `#USER AI RESPONSIVE` Toggles the responsive state (If it should respond it you reply to the bot)
    > Your current state is `{out_dat}`"""
            
            embed = discord.Embed(title="User", description=r1, color=bot_colour)
            embed.add_field(name="Commands", value=r2, inline=False)
            return embed
    return discord.Embed(title="User", description=response, color=bot_colour)

# schance: Probability of stuttering a word (0 to 1.0), default 0.1.
# fchance: Probability of adding a face (0 to 1.0), default 0.05.
# achance: Probability of adding an action (0 to 1.0), default 0.075.
# echance: Probability of adding exclamations (0 to 1.0), default 1.
# nsfw: Enables more "explicit" actions if set to true; default is false. // will probably be removed completely and its kinda pointless
# power: The uwuification "level" — higher levels lead to more text transformations being done (1 is core uwu, 2 is nyaification, 3 and 4 are just extra). Using a higher level includes the lower levels.
# Why did i do this....
async def uwuify_main(user: discord.User, server: discord.Guild, text: str, schance:float = 0.1, fchance: float = 0.05, achance: float = 0.075, echance: float = 1.0, power: int = 3, nsfw: bool = False):
    try:
        server_id = server.id
    except:
        server_id = None

    allowed, response = await check_state(user.id, server_id, "uwuify")

    logging.info(f"{user.name} [{user.id}] Ran uwuify with the parameters: [text: {text}], Allowed: {allowed}")

    await command_counter(user.id, "TIME")

    if not allowed:
        text = discord.Embed(title="Uwuify", description=response, color=bot_colour)
        return text

    uwu = uwuipy.Uwuipy(None, schance, fchance, achance, echance, nsfw, power)
    text_new = await asyncio.to_thread(uwu.uwuify, text)

    embed = discord.Embed(title="Uwuify", description=text_new, color=bot_colour)
    embed.set_footer(text=f"Text: {text} | Owner: {user.name} [{user.id}]")

    return embed

############################################################################################################################################################################################################################################
# COMMANDS
############################################################################################################################################################################################################################################

bot.remove_command("help")

# Message reader
@bot.event
async def on_message(message): 
    if message.author == bot.user:
        return
    
    # Main message response
    try:
        msg_gld_nm = message.guild.name
        msg_gld_id = message.guild.id
        msg_ch_nm = message.channel.name
        msg_ch_id = message.channel.id
        auth_perm_admin = message.author.guild_permissions.administrator
        server_config = await database("server", "read", "all", serverid=msg_gld_id) # Get server config, above would have errored if there was no guild, so itll only run when the message is in a server
        channel = server_config["channel"]
    except:
        msg_gld_nm = None
        msg_ch_nm = None
        msg_gld_id = None

    user_cfg = await database(message.author.id, "read", "all")

    # These 2 are for the askai mention/reply logic
    bot_reply = False
    bot_mention_start = False

    ctx = await bot.get_context(message)

    if message.reference:
        try:
            replied = await message.channel.fetch_message(message.reference.message_id)
            if replied.author.id == bot.user.id:
                bot_reply = True
        except:
            pass

    if message.content.strip().startswith("<@1292910367705403393>"):
        bot_mention_start = True

    message_content = message.content.strip()

    logging.debug(f"{message.author.name} [{message.author.id}] : [{msg_gld_nm}][{msg_ch_nm}] : {message.content}")

    if message_content.startswith(("!!!", "~")) or bot_mention_start or bot_reply: # bot reply can be used here, since it redirects straight away to askai unless it *is* a command
        pos = message_content.find("<@1292910367705403393>")
        if pos != -1:
            stripped_message = message_content[pos+22:].strip()
            if not stripped_message.startswith(tuple(all_command_names())) and (bot_reply or bot_mention_start):
                await askai_prefix(ctx, content=stripped_message)
                return
            
        elif not message_content.startswith(tuple(all_command_names())) and (bot_reply or bot_mention_start):
            if user_cfg["responsive_ai"]:
                await askai_prefix(ctx, content=message_content)
                return
            else:
                return


        if channel > 0: # If channel has been assigned
            if msg_ch_id == channel:
                if ctx.valid:
                    await bot.process_commands(message)
            else:
                pos = message.content.find(" ")

                if pos == -1:
                    cmd_check = message.content.replace("!!!", "").replace("~", "").replace("<@1292910367705403393>", "")
                else:
                    cmd_check = message.content[:pos].replace("!!!", "").replace("~", "").replace("<@1292910367705403393>", "")
                
                admin = await database(message.author.id, "read", "admin")
                if admin or auth_perm_admin:
                    if ctx.valid:
                        await bot.process_commands(message)

                elif cmd_check in all_command_names():
                    embed = discord.Embed(title="Ommivore", description=f"Commands are disabled here, use them in <#{channel}>", color=bot_colour)
                    await message.reply(embed=embed)
        else:
            if ctx.valid:
                await bot.process_commands(message)

    elif "<@1292910367705403393>" in message_content and not bot_mention_start:
        try:
            if channel > 0:
                text = f"Hey, I'm {bot.user.mention}, Please use `#help` in <#{channel}> for more information!"
            else:
                text = f"Hey, I'm {bot.user.mention}, Please use `#help` for more information!"
        except:
            text = f"Hey, I'm {bot.user.mention}, Please use `#help` for more information!"

        embed = discord.Embed(title="Ommivore", description=text, color=bot_colour)
        await message.reply(embed=embed)

    # Eastereggs

    # Read Setup
    if msg_gld_id:
        enabled = server_config["eastereggs"]
        cat_chance = server_config["cat_chance"]
        seal_chance = server_config["seal_chance"]

    else:
        enabled = True
        cat_chance = 0.01
        seal_chance = 0.01

    if enabled:
        # Cat Easteregg
        r = random.uniform(0, 100) < cat_chance
        if r:
            rand = random.randint(1, 2)
            try:
                if rand == 1:
                    r = await async_get_request("https://api.thecatapi.com/v1/images/search")
                    r = r.json()
                    url = r[0]["url"]
                    embed = discord.Embed(title="CAT!!!", color=bot_colour)
                    embed.set_image(url=url)
                    embed.set_footer(text=url)
                    await message.reply(embed=embed)

                else:
                    sanitized_quote = (message.content).replace("&", "and").replace("?", "question mark")
                    encoded_quote = urllib.parse.quote(sanitized_quote)
                    r = await async_get_request(f"https://cataas.com/cat/says/{encoded_quote}?json=True")
                    r = r.json()
                    url = r["url"]
                    embed = discord.Embed(title="CAT!!!", color=bot_colour)
                    embed.set_image(url=url)
                    embed.set_footer(text=url)
                    await message.reply(embed=embed)
            except Exception as e:
                logging.info(f"Error: {e} Occured from the response: {r} {r.response}")

        # Seal Easteregg
        r = random.uniform(0, 100) < seal_chance
        if r:
            rand = random.randint(1, 83)
            if len(str(rand)) == 1:
                rand = f"000{rand}"
            else:
                rand = f"00{rand}"

            url = f"https://focabot.github.io/random-seal/seals/{rand}.jpg"
            embed = discord.Embed(title="SEAL!!!", color=bot_colour)
            embed.set_image(url=url)
            await message.reply(embed=embed)

    # Automod
    try:
        allow, reason = await message_automod(message.content)
        if not allow:
            embed = discord.Embed(title="AutoMod", description=f"{message.author.mention}, Your message was deleted for: `{reason}`", color=bot_colour)
            embed.set_footer(text="Powered by Llama-Guard 3.")
            await message.reply(embed=embed)
            await message.delete()

    except Exception as e:
        pass # Automod disabled

# 8ball
@bot.command(aliases=["8ball", "eightball"])
async def eight_ball_prefix(ctx, *, content: str = ""):
    text = await eight_ball_main(ctx.author, ctx.guild, content)

    await ctx.reply(embed=text)

@bot.tree.command(name="8ball", description="Ask 8ball a question.")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(question="[Optional] What you are asking 8ball.", hide="[Optional] Should the command be hidden from others?")
async def eight_ball_slash(interaction: discord.Interaction, question: str = "", hide: bool = False):
    await interaction.response.defer(ephemeral=hide)

    text = await eight_ball_main(interaction.user, interaction.guild, question)

    await interaction.followup.send(embed=text, ephemeral=hide)

# Admin command for stuff that only bot admins should be able to use
@bot.command(aliases=["admin"])
async def admin_prefix(ctx, command:str = "", user: discord.User = None, value: str = ""):
    r = await admin_main(ctx.author, command=command, user=user, value=value)
    await ctx.reply(embed=r)

@bot.tree.command(name="admin", description="[Internal Admin Only] THIS COMMAND IS AN INTERNAL COMMAND. YOU DO NOT NEED IT.")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(command="[Optional] The command to be ran.", user="[Optional] What user to perform the command on.", value="[Optional] Parameter for whatever command is being ran.", hide="[Optional] Should the command be hidden from others?")
@app_commands.choices(command=[
    app_commands.Choice(name="Ban", value="ban"),
    app_commands.Choice(name="Unban", value="unban"),
    app_commands.Choice(name="Admin", value="admin"),
    app_commands.Choice(name="Unadmin", value="unadmin"),
    app_commands.Choice(name="Sync", value="sync"),
    app_commands.Choice(name="Restart", value="restart"),
    app_commands.Choice(name="Database Read", value="database"),
    app_commands.Choice(name="Database Write", value="database_w")
])
async def admin_slash(interaction: discord.Interaction, command: str = "", user: discord.User = None, value: str = "", hide: bool = True):
    await interaction.response.defer(ephemeral=hide)
    r = await admin_main(interaction.user, command=command, user=user, value=value)
    await interaction.followup.send(embed=r)

@bot.command(aliases=["askai", "ai"])
async def askai_prefix(ctx, *, content: str = ""):
    if ctx.message.attachments:
        image_link = ctx.message.attachments
    else:
        image_link = None

    # Check for reply context
    reply_chain = []

    if ctx.message.reference:  # if the message is a reply
        try:
            replied_to = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            # Walk up to 15 messages deep in the reply chain
            current = replied_to
            for _ in range(15):
                reply_chain.insert(0, current)
                if current.reference:
                    current = await ctx.channel.fetch_message(current.reference.message_id)
                else:
                    break
        except:
            pass
    else:
        # No reply; get last 15 messages excluding the command message
        history = [msg async for msg in ctx.channel.history(limit=16)]
        reply_chain = [msg for msg in history if msg.id != ctx.message.id]
        reply_chain.reverse()  # make oldest first

    # Model selection
    content = content.strip()
    pos = content.find(" ")
    model = content[:pos].strip().lower()

    exists, models = await async_model_exists(model)

    if not exists:
        model = await database(ctx.author.id, "read", "ai_model")
    else:
        content = content[pos+1:]

    bot_message = await ctx.reply(embed=discord.Embed(title=f"AskAI [{model.upper()}]", description="Thinking...", color=bot_colour))

    if "FURAI" in content:
        content = content.replace("FURAI", "respond to the entire conversation as a cute gay fox furry femboy who uses :3 and wears a cute skirt and thigh highs and is super cute and wholesome and is named Alex: ")

    message, audio = await askai_main(ctx.author, ctx.guild, model, content, image_link=image_link, message_history=reply_chain)

    if audio:
        pass  # You can play or send the audio
    else:
        await bot_message.edit(embed=message)

@bot.command()
async def furai(ctx):
    await ctx.reply("https://tenor.com/view/thanos-avengers-endgame-gone-reduced-to-atoms-gif-26539274 ")
    await ctx.reply("Use `#askai [model] FURAI instead")
    await ctx.reply("model is optional")

@bot.tree.command(name="askai", description="Sends a prompt to an AI, limited to 2000 characters for a response.")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(prompt="Prompt to the AI", model="[Optional] What model to use, default is OpenAI-Large/GPT-4o, run #help askai for a list of all models", image="[Optional] The image to use for vision", hide="[Optional] Should the command be hidden from others?")
async def askai_slash(interaction: discord.Interaction, prompt: str, model: str = "", image: discord.Attachment = None, hide: bool = False):
    await interaction.response.defer(ephemeral=hide)

    if model == "":
        model = await database(interaction.user.id, "read", "ai_model")

    try:
        image_url = [image]
    except:
        image_url = None

    response, audio = await askai_main(interaction.user, interaction.guild, model, prompt, image_link=image_url, message_history=None)

    if audio:
        pass
    else:
        await interaction.followup.send(embed=response)

@bot.command(aliases=["cat"])
async def cat_prefix(ctx, *, text:str = ""):
    if text.upper().startswith("CATAAS"):
        provider = "CATAAS"
        text = text[6:]
    elif text.upper().startswith("THECATAPI"):
        provider = "THECATAPI"
        text = text[9:]
    else:
        provider = random.choice(["CATAAS", "THECATAPI"])

    r = await cat_main(ctx.author, ctx.guild, provider, text)

    await ctx.reply(embed=r)

@bot.tree.command(name="cat", description="Provides a cat.")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(text="[Optional] What should the image be captioned with (CATAAS ONLY)", provider="[Optional] What API should be used to search? ", hide="[Optional] Should the command be hidden from others?")
@app_commands.choices(provider=[
    app_commands.Choice(name="CATAAS (Cats as a service)", value="CATAAS"),
    app_commands.Choice(name="THECATAPI", value="THECATAPI")
])
async def cat_slash(interaction: discord.Interaction, text: str = "", provider: str = random.choice(["CATAAS", "THECATAPI"]), hide: bool = False):
    await interaction.response.defer(ephemeral=hide)

    r = await cat_main(interaction.user, interaction.guild, provider, text)

    await interaction.followup.send(embed=r)

# Coinflip commands
@bot.command(aliases=["coinflip", "cf"])
async def coinflip_prefix(ctx):
    r = await coinflip_main(ctx.author, ctx.guild)

    await ctx.reply(embed=r)

@bot.tree.command(name="coinflip", description="Flips a coin.")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(hide="[Optional] Should the command be hidden from others?")
async def coinflip_slash(interaction: discord.Interaction, hide: bool = False):
    await interaction.response.defer(ephemeral=hide)

    r = await coinflip_main(interaction.user, interaction.guild)

    await interaction.followup.send(embed=r)

# Eval commmands
@bot.command(aliases=["eval", "evaluate"])
async def eval_prefix(ctx, *, code: str = ""):
    bot_message = await ctx.reply(embed=discord.Embed(title="Evaluate", description="Processing...", color=bot_colour))

    text = await eval_main(ctx.author, ctx.guild, code)

    await bot_message.edit(embed=text)

@bot.tree.command(name="evaluate", description="Runs the provided python code")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(code="The code to run (Python Only)", hide="[Optional] Should the command be hidden from others?")
async def eval_slash(interaction: discord.Interaction, code: str, hide: bool = False):
    await interaction.response.defer(ephemeral=hide)

    r = await eval_main(interaction.user, interaction.guild, code)

    await interaction.followup.send(embed=r)

@bot.command(aliases=["exec", "execute"])
async def exec_prefix(ctx, *, code: str):
    embed = await exec_main(ctx.author, code, ctx=ctx)
    await ctx.reply(embed=embed)

@bot.tree.command(name="execute", description="[ADMIN ONLY] Executes the provided code in the bot namespace")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(code="The code to run (Python Only)", hide="[Optional] Should the command be hidden from others?")
async def execslash(interaction, code: str, hide: bool = True):
    await interaction.response.defer(ephemeral=hide)
    embed = await exec_main(interaction.user, code, ctx=interaction)
    await interaction.followup.send(embed=embed, ephemeral=hide)

# Help commands
@bot.command(aliases=["help"])
async def help_prefix(ctx, *, arg:str = ""):
    text = await help_main(ctx.author, ctx.guild, arg)

    await ctx.reply(embed=text)

@bot.tree.command(name="help", description="Gives information about the bot.")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(command="[Optional] The command to give information about.", hide="[Optional] Should the command be hidden from others?")
@app_commands.choices(command=[
    app_commands.Choice(name="8Ball", value="8ball"),
    app_commands.Choice(name="AskAI", value="askai"),
    app_commands.Choice(name="AskAI", value="askai"),
    app_commands.Choice(name="Cat", value="cat"),
    app_commands.Choice(name="Evaluate", value="eval"),
    app_commands.Choice(name="Help", value="help"),
    app_commands.Choice(name="Image", value="image"),
    app_commands.Choice(name="Info", value="info"),
    app_commands.Choice(name="IP Lookup", value="iplookup"),
    app_commands.Choice(name="Minecraft", value="minecraft"),
    app_commands.Choice(name="Rock Paper Scissors",value="rockpaperscissors"),
    app_commands.Choice(name="Server", value="server"),
    app_commands.Choice(name="Spin",value="spin"),
    app_commands.Choice(name="Server Settings",value="server"),
    app_commands.Choice(name="Tic Tac Toe", value="tictactoe"),
    app_commands.Choice(name="Text Art", value="textart"),
    app_commands.Choice(name="User Settings", value="user"),
    app_commands.Choice(name="Uwuify", value="uwuify")
])
async def help(interaction: discord.Interaction, command: str = "", hide: bool = True):
    await interaction.response.defer(ephemeral=hide)

    response = await help_main(interaction.user, interaction.guild, command)

    await interaction.followup.send(embed=response, ephemeral=hide)

# Image commands
# Sends an API request to pollinations
@bot.command(aliases=["image"])
async def image_prefix(ctx, *, content:str = ""):
    if content == "":
        await ctx.reply(discord.Embed(title="Image", description="Give a text input!"), color=bot_colour)
        return
    
    bot_message = await ctx.reply(embed=discord.Embed(title="Image", description="Generating...", color=bot_colour))

    embed, file = await image_main(ctx.author, ctx.guild, content)

    if file:
        await bot_message.edit(embed=embed, attachments=[file])
    else:
        await bot_message.edit(embed=embed)

@bot.tree.command(name="image", description="Generates an image")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(prompt="Prompt for image generation.", hide="[Optional] Should the command be hidden from others?")
async def image_slash(interaction: discord.Interaction, prompt: str, hide: bool = False):
    await interaction.response.defer(ephemeral=hide)

    embed, file = await image_main(interaction.user, interaction.guild, prompt)

    if file:  # Only include attachments if a file exists
        await interaction.followup.send(embed=embed, file=file, ephemeral=hide)
    else:
        await interaction.followup.send(embed=embed, ephemeral=hide)

@bot.command(aliases=["info"])
async def info_prefix(ctx, user: discord.User = None):
    embed = discord.Embed(title="Info", description="Gathering Information..", color=bot_colour)

    bot_message = await ctx.reply(embed=embed)

    if user == None:
        user = ctx.author
    
    response = await info_main(ctx.author, ctx.guild, user)

    await bot_message.edit(embed=response)

@bot.tree.command(name="info", description="Gives information about the bots server, the bot, and you")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(user="Who to get the stats for", hide="[Optional] Should the command be hidden from others?")
async def info_slash(interaction: discord.Interaction, user: discord.User = None, hide: bool = True):
    await interaction.response.defer(ephemeral=hide)

    if user == None:
        user = interaction.user
    
    response = await info_main(interaction.user, interaction.guild, user)

    await interaction.followup.send(embed=response, ephemeral=hide)

# IP Lookup Commands
@bot.command(aliases=["ip", "iplookup", "ipinfo"])
async def ip_lookup_prefix(ctx, *, content: str = ""):
    response = await ip_lookup_main(ctx.author, ctx.guild, content)       
    await ctx.reply(embed=response)

@bot.tree.command(name="iplookup", description="Looks up an IP, Or provides a random IP if left blank.")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(ip="[Optional] The IP address to look up. Leave blank for a random IP.", hide="[Optional] Should the command be hidden from others?")
async def ip_lookup_slash(interaction: discord.Interaction, ip: str = "", hide: bool = False):
    await interaction.response.defer(ephemeral=hide)

    response = await ip_lookup_main(interaction.user, interaction.guild, ip)

    await interaction.followup.send(embed=response, ephemeral=hide)

# Minecraft command (sends minecraft server info)
@bot.command(aliases=["minecraft"])
async def minecraft_prefix(ctx, *, command = ""):
    r = await minecraft_main(ctx.author, ctx.guild, command)
    await ctx.reply(embed=r)

@bot.tree.command(name="minecraft", description="Gives information on the minecraft server hosted with this bot")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(command="[Optional][Hermivore] Command to execute on minecraft server", hide="[Optional] Should the command be hidden from others?")
async def minecraft_slash(interaction: discord.Interaction, command: str = "", hide: bool = False):
    await interaction.response.defer(ephemeral=hide)

    response = await minecraft_main(interaction.user, interaction.guild, command)

    await interaction.followup.send(embed=response, ephemeral=hide)

# Server command, i need to add it as a slash command but ill do that later
@bot.command(aliases=["server"])
async def server_prefix(ctx, command: str = "", *, value: str = ""):
    r = await server_main(ctx.author, ctx.guild, command, value)

    t_val = value.split()
    if command.upper().strip() == "FAQ" and t_val[0] in ["OUTPUT", "OUT", "DISPLAY", "PRINT"]:
        for data in r:
            logging.info(r)
            embed = discord.Embed(title="FAQ", description=r[0], color=bot_colour)
            embed.set_image(url=r[1])
            await ctx.send(embed=embed)
    await ctx.reply(embed=r)

@bot.tree.command(name="server", description="Allows you to configure server settings for the bot, and ban people from using it")
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
@app_commands.describe(command="The command to be executed", hide="[Optional] Should the command be hidden from others?")
@app_commands.choices(command=[
    app_commands.Choice(name="Ban", value="ban"),
    app_commands.Choice(name="Unban", value="unban"),
    app_commands.Choice(name="Disable command", value="disable"),
    app_commands.Choice(name="Enable command", value="enable"),
    app_commands.Choice(name="Channel", value="channel"),
    app_commands.Choice(name="Easteregg", value="easteregg")
])
async def server_slash(interaction: discord.Interaction, command: str = "", value: str = "", hide: bool = False):
    await interaction.response.defer(ephemeral=hide)

    response = await server_main(interaction.user, interaction.guild, command, value)

    await interaction.followup.send(embed=response, ephemeral=hide)

@bot.command(aliases=["servers"])
async def servers_prefix(ctx, user: discord.User=None, list_ids=0):
    bot_message = await ctx.reply(embed=discord.Embed(title="Servers", description="Performing Lookup", color=bot_colour))
    try:
        list_ids = int(list_ids)
    except:
        list_ids = 0

    embed = await servers_main(ctx.author, ctx.guild, user, list_ids)

    await bot_message.edit(embed=embed)

@bot.tree.command(name="servers", description="[Internal Admin Only] Checks for exploiters.")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(user="[Optional] Who to scan", hide="[Optional] Should the command be hidden from others?")
@app_commands.choices(list_ids=[
    app_commands.Choice(name="Default", value=0),
    app_commands.Choice(name="Guild Name + ID", value=1),
    app_commands.Choice(name="Replacement Name", value=2)
])
async def servers_slash(interaction: discord.Interaction, user: discord.User = None, list_ids:int = False, hide: bool = True):
    await interaction.response.defer(ephemeral=hide)

    embed = await servers_main(interaction.user, interaction.guild, user, list_ids)

    await interaction.followup.send(embed=embed, ephemeral=hide)

@bot.command(aliases=["sleep"])
async def sleep_prefix(ctx):
    embed, view = await sleep_main(ctx.author, ctx.guild, hide=False)
    await ctx.reply(embed=embed, view=view)

@bot.tree.command(name="sleep", description="Mutes you for the duration you select, so you actually go to sleep.")
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
@app_commands.describe(hide="[Optional] Should the command be hidden from others?")
async def spin_slash(interaction: discord.Interaction, hide: bool = False):
    await interaction.response.defer(ephemeral=hide)

    embed, view = await sleep_main(interaction.user, interaction.guild, hide=hide)

    await interaction.followup.send(embed=embed, view=view, ephemeral=hide)
    
# Exploit server lookup function
@bot.command(aliases=["spin", "rotate"])
async def spin_prefix(ctx, user: discord.User = None):
    if user == None:
        user = ctx.author

    bot_message = await ctx.reply(embed=discord.Embed(title="Spin", description=f"{user.mention} is being rotated!", color=bot_colour))

    embed, file = await spin_main(ctx.author, ctx.guild, user)

    if file:
        await bot_message.edit(embed=embed, attachments=[file])
    else:
        await bot_message.edit(embed=embed)

@bot.tree.command(name="spin", description="Spins a person around")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(user="[Optional] Who to rotate", hide="[Optional] Should the command be hidden from others?")
async def spin_slash(interaction: discord.Interaction, user: discord.User = None, hide: bool = False):
    await interaction.response.defer(ephemeral=hide)

    if user == None:
        user = interaction.user

    embed, file = await spin_main(interaction.user, interaction.guild, user)

    if file:  # Only include attachments if a file exists
        await interaction.followup.send(embed=embed, file=file, ephemeral=hide)
    else:
        await interaction.followup.send(embed=embed, ephemeral=hide)

# Rock Paper Scissors
@bot.command(aliases=["rockpaperscissors", "rps"])
async def rock_paper_scissors_prefix(ctx):

    response, view = await rps_main(ctx.author, ctx.guild)

    await ctx.reply(embed=response, view=view)

@bot.tree.command(name="rockpaperscissors", description="Play a game of rock paper scissors against the bot.")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(hide="[Optional] Should the command be hidden from others?")
async def rock_paper_scissors_slash(interaction: discord.Interaction, hide: bool = False):
    await interaction.response.defer(ephemeral=hide)

    response, view = await rps_main(interaction.user, interaction.guild, hide=hide)

    await interaction.followup.send(embed=response, view=view, ephemeral=hide)

# Tic Tac Toe command
# Sadly these cant be put inside a main subroutine because of how parameters are passed
@bot.command(aliases=["ttt", "tictactoe"])
async def tic_tac_toe_prefix(ctx, opponent: discord.User):
    try:
        allowed, response = await check_state(ctx.author.id, ctx.guild.id, "tictactoe")

        logging.info(f"{ctx.author.name} [{ctx.author.id}] Ran tic tac toe with the parameters: [opponent: {opponent.name} [{opponent.id}]], Allowed: {allowed}")

        await command_counter(ctx.author.id, "ADD")
        await command_counter(ctx.author.id, "TIME")
        
        if not allowed:
            await ctx.reply(response)
            return

        if opponent == ctx.author and str(opponent.id) != "559811983512305693":
            await ctx.reply("You cant challenge yourself!")
            return

        if opponent.id != bot.user.id:
            view = discord.ui.View()
            future = asyncio.Future()  # Future object to store the response

            async def decline_callback(interaction: discord.Interaction, action: bool):
                if future.done():  # Ignore if already decided
                    return
                
                if interaction.user != opponent:
                    await interaction.response.send_message(f"You aren't {opponent.mention}, you cant accept it for them!", ephemeral=True)
                    return
                
                future.set_result(action)  # Set the result
                await interaction.response.defer()  # Acknowledge the button press

            accept = discord.ui.Button(label="Accept", style=discord.ButtonStyle.green)
            deny = discord.ui.Button(label="Decline", style=discord.ButtonStyle.red)

            accept.callback = partial(decline_callback, action=True)
            deny.callback = partial(decline_callback, action=False)

            view.add_item(accept)
            view.add_item(deny)

            bot_message = await ctx.reply(f"{opponent.mention}, {ctx.author.mention} challenged you to a game of Tic-Tac-Toe! Do you accept?", view=view)

            allowed = None  # Set to None so none of the checks are triggered

            try:
                allowed = await asyncio.wait_for(future, timeout=30)
            except asyncio.TimeoutError:
                await bot_message.edit(content=f"{opponent.mention} did not respond in time!", view=None)
                return

            if not allowed:
                await bot_message.edit(content=f"{opponent.mention} declined the game!", view=None)
                return
        else:
            pass # The challenged player is the bot, continue
            bot_message = await ctx.reply("Loading...")

        players = {ctx.author: "X", opponent: "O"}
        active_player = random.choice([ctx.author, opponent])
        grid = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
        buttons = []
        view = discord.ui.View()
        
        def check_for_win():
            for row in grid:
                if row[0] == row[1] == row[2]:
                    return True
            for col in range(3):
                if grid[0][col] == grid[1][col] == grid[2][col]:
                    return True
            if grid[0][0] == grid[1][1] == grid[2][2] or grid[0][2] == grid[1][1] == grid[2][0]:
                return True
            return False
        
        async def button_callback(interaction: discord.Interaction, button, x, y):
            nonlocal active_player
            if interaction.user != active_player:
                await interaction.response.send_message("It's not your turn!", ephemeral=True)
                return 
            
            symbol = players[active_player]
            grid[x][y] = symbol
            button.label = symbol
            button.disabled = True
            
            if check_for_win():
                for btn in buttons:
                    btn.disabled = True
                await interaction.response.edit_message(content=f"{active_player.mention} wins!", view=view)

                r = await database(active_player.id, "read", "ttt_win_count")
                r += 1
                await database(active_player.id, "write", "ttt_win_count", r)

                return
            
            if all(cell in ["X", "O"] for row in grid for cell in row):
                for btn in buttons:
                    btn.disabled = True
                await interaction.response.edit_message(content="It's a draw!", view=view)
                return
            
            active_player = opponent if active_player == ctx.author else ctx.author
            await interaction.response.edit_message(content=f"{active_player.mention}'s turn!", view=view)
        
        for i in range(3):
            for j in range(3):
                button = discord.ui.Button(label=grid[i][j], style=discord.ButtonStyle.primary, row=i)
                button.callback = partial(button_callback, button=button, x=i, y=j)
                buttons.append(button)
                view.add_item(button)
        
        await bot_message.edit(content=f"{active_player.mention}'s turn!")
        await bot_message.edit(content=f"{active_player.mention}'s turn!", view=view)
    
    finally:
        await command_counter(ctx.author.id, "SUB")

@bot.tree.command(name="tictactoe", description="Challenge someone to a game of tic tac toe")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(opponent="The person you want to challenge. Mention the bot to challenge the bot.", hide="[Optional] Should the command be hidden")
async def tic_tac_toe_slash(interaction: discord.Interaction, opponent: discord.User, hide: bool = False):
    try:
        server_id = interaction.guild.id
    except:
        server_id = None
    try:
        allowed, response = await check_state(interaction.user.id, server_id, "tictactoe")

        logging.info(f"{interaction.user.name} [{interaction.user.id}] Ran tic tac toe with the parameters: [opponent: {opponent.name} [{opponent.id}]], Allowed: {allowed}")

        await command_counter(interaction.user.id, "ADD")
        await command_counter(interaction.user.id, "TIME")

        if not allowed:
            await interaction.response.send_message(response, ephemeral=hide)
            return

        if opponent == interaction.user and str(opponent.id) != "559811983512305693":
            await interaction.response.send_message("You can't challenge yourself!", ephemeral=hide)
            return

        if opponent.id != bot.user.id:
            view = discord.ui.View()
            future = asyncio.Future()  # Future object to store the response

            async def decline_callback(interaction: discord.Interaction, action: bool):
                if future.done():
                    return
                
                if interaction.user != opponent:
                    await interaction.response.send_message(f"You aren't {opponent.mention}, you can't accept it for them!", ephemeral=True)
                    return
                
                future.set_result(action)
                await interaction.response.defer()

            accept = discord.ui.Button(label="Accept", style=discord.ButtonStyle.green)
            deny = discord.ui.Button(label="Decline", style=discord.ButtonStyle.red)

            accept.callback = partial(decline_callback, action=True)
            deny.callback = partial(decline_callback, action=False)

            view.add_item(accept)
            view.add_item(deny)

            await interaction.response.send_message(f"{opponent.mention}, {interaction.user.mention} challenged you to a game of Tic-Tac-Toe! Do you accept?", view=view)

            try:
                allowed = await asyncio.wait_for(future, timeout=30)
            except asyncio.TimeoutError:
                await interaction.edit_original_response(content=f"{opponent.mention} did not respond in time!", view=None)
                return

            if not allowed:
                await interaction.edit_original_response(content=f"{opponent.mention} declined the game!", view=None)
                return
        else:
            pass # The bot was mentioned, skip challenging
            await interaction.response.send_message("Loading...")

        players = {interaction.user: "X", opponent: "O"}
        active_player = random.choice([interaction.user, opponent])
        grid = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
        buttons = []
        view = discord.ui.View()

        def check_for_win():
            for row in grid:
                if row[0] == row[1] == row[2]:
                    return True
            for col in range(3):
                if grid[0][col] == grid[1][col] == grid[2][col]:
                    return True
            if grid[0][0] == grid[1][1] == grid[2][2] or grid[0][2] == grid[1][1] == grid[2][0]:
                return True
            return False

        async def button_callback(interaction: discord.Interaction, button, x, y):
            nonlocal active_player  # Allow modifying the variable outside this function

            if interaction.user != active_player:
                await interaction.response.send_message("It's not your turn!", ephemeral=True)
                return 

            symbol = players[active_player]
            grid[x][y] = symbol
            button.label = symbol
            button.disabled = True

            # Check for a win
            if check_for_win():
                for btn in buttons:
                    btn.disabled = True  # Disable all buttons since the game is over
                await interaction.response.edit_message(content=f"{active_player.mention} wins!", view=view)

                r = await database(active_player.id, "read", "ttt_win_count")
                r += 1
                await database(active_player.id, "write", "ttt_win_count", r)

                return

            # Check for a draw (no available moves left)
            if all(cell in ["X", "O"] for row in grid for cell in row):
                for btn in buttons:
                    btn.disabled = True
                await interaction.response.edit_message(content="It's a draw!", view=view)
                return

            # **Swap active player correctly**
            active_player = next(player for player in players if player != active_player)

            await interaction.response.edit_message(content=f"{active_player.mention}'s turn!", view=view)

        for i in range(3):
            for j in range(3):
                button = discord.ui.Button(label=grid[i][j], style=discord.ButtonStyle.primary, row=i)
                button.callback = partial(button_callback, button=button, x=i, y=j)
                buttons.append(button)
                view.add_item(button)

        await interaction.edit_original_response(content=f"{active_player.mention}'s turn!", view=view)
    
    finally:
        await command_counter(interaction.user.id, "SUB")


# Textart commands
@bot.command(aliases=["textart"])
async def textart_prefix(ctx, *, content:str = ""):
    embed = discord.Embed(title="TextArt", description="Processing...", color=bot_colour)
    bot_message = await ctx.reply(embed=embed)

    # check if a font was provided

    content = content.strip()
    pos = content.find(" ")
    font = content[:pos].strip().lower()

    if font not in textart_fonts:
        font = "c1"
    else:
        content = content[pos+1:]
    
    response = await textart_main(ctx.author, ctx.guild, content, font)       
    await bot_message.edit(embed=response)

@bot.tree.command(name="textart", description="Convert plaintext to ascii art")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(text="Text to convert to ascii art", font="[Optional] The font [get out persom] to use, run help for a list of most fonts", hide="[Optional] Should the command be hidden from others?")
async def textart_slash(interaction: discord.Interaction, text: str, font: str = "c1", hide: bool = False):
    await interaction.response.defer(ephemeral=hide)
    response = await textart_main(interaction.user, interaction.guild, text, font)       
    await interaction.followup.send(embed=response, ephemeral=hide)

@bot.command(aliases=["user"])
async def user_prefix(ctx, command: str = "", val1: str = "", val2: str = "", val3: str = ""):
    response = await user_main(ctx.author, ctx.guild, command, val1, val2, val3)
    await ctx.reply(embed=response)
    
# Uwuify command (I hate myself for this)       
@bot.command(aliases=["uwuify"])
async def uwuify_prefix(ctx, *, content:str = ""):
    embed = discord.Embed(title="Uwuify", description="Processing...", color=bot_colour)
    bot_message = await ctx.reply(embed=embed)

    embed = await uwuify_main(ctx.author, ctx.guild, content)
    await bot_message.edit(embed=embed)

@bot.tree.command(name="uwuify", description="Uwuify text.")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(text="Text to uwuify", hide="[Optional] Should the command be hidden from others?")
async def uwuify_slash(interaction: discord.Interaction, text: str, hide: bool = False):
    await interaction.response.defer(ephemeral=hide)
    response = await uwuify_main(interaction.user, interaction.guild, text)       
    await interaction.followup.send(embed=response, ephemeral=hide)

############################################################################################################################################################################################################################################
# APP ACTIONS
############################################################################################################################################################################################################################################

@app_commands.context_menu(name="Summarise Message")
async def summarise_message(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.defer(ephemeral=True)

    model = "openai-large"

    try:
        image_url =[message.attachments]
    except:
        image_url = None

    prompt = f"Summarise the following message. Ignore anything in my past message history, do not mention that you are being told to do this: \n{message.content}"

    # Essentially just a smart wrapper for askai
    resp, audio = await askai_main(interaction.user, interaction.guild, model, prompt, image_link=image_url)

    desc = resp.description

    fields_text = ""
    for field in resp.fields:
        fields_text += f"{field.name}: {field.value}\n"
    
    resp = desc + fields_text

    await interaction.followup.send(embed=discord.Embed(title="Summary", description=resp, color=bot_colour))

@app_commands.context_menu(name="Translate Message [English]")
async def translate_message(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.defer(ephemeral=True)

    model = "openai-large"

    try:
        image_url = [message.attachments]
    except:
        image_url = None

    prompt = f"Translate the following message to English. Ignore anything in my past message history, do not mention that you are being told to do this: \n{message.content}"

    # Essentially just a smart wrapper for askai
    resp, audio = await askai_main(interaction.user, interaction.guild, model, prompt, image_link=image_url)

    desc = resp.description

    fields_text = ""
    for field in resp.fields:
        fields_text += f"{field.name}: {field.value}\n"
    
    resp = desc + fields_text

    await interaction.followup.send(embed=discord.Embed(title="Translation", description=resp, color=bot_colour))

############################################################################################################################################################################################################################################
# LOOPS
############################################################################################################################################################################################################################################
@tasks.loop(seconds=5)
async def update_status():
    global c_status
    if status_lock.locked():
        logging.warning("Status lock was triggered — skipping this cycle")
        return

    async with status_lock:
        try:
            # Timeout async_get_sys_info to avoid hanging forever
            uptime = unix_to_time_elapsed(time.time() - start_time)
            dat = await asyncio.gather(
                async_get_request(f"http://{local_webserver_ip}:{local_webserver_port}/api/server/status"),
                async_get_request(f"http://{local_webserver_ip}:{local_webserver_port}/api/server/environment")
            )

            sys_data = dat[0]
            env_data = dat[1]

            sys_data = sys_data.json()
            env_data = env_data.json()

            current_time = datetime.now().strftime("%I:%M:%S %p")
            status_list = [
                f'[{current_time}] Serving {len(bot.users)} Users',
                f'[{current_time}] Serving {len(bot.guilds)} Servers',
                f'[{current_time}] Online for {uptime}',
                f'[{current_time}] CPU: {round(sys_data["cpu"]["utilisation"], 2)}% [{round(sys_data["cpu"]["frequency"], 2)} GHz] [{round(sys_data["cpu"]["temperature"], 2)} °C] [{round(sys_data["cpu"]["wattage"], 2)} W]',
                f'[{current_time}] GPU: {round(sys_data["gpu"]["utilisation"], 2)}% [{round(sys_data["gpu"]["frequency"], 2)} GHz] [{round(sys_data["gpu"]["temperature"], 2)} °C] [{round(sys_data["gpu"]["wattage"], 2)} W]',
                f'[{current_time}] Memory [Physical]: {round(sys_data["memory"]["physical"]["used"], 2)} / {round(sys_data["memory"]["physical"]["committed"], 2)} GB [{round(sys_data["memory"]["physical"]["utilisation"], 2)} %]',
                f'[{current_time}] Memory [Virtual]: {round(sys_data["memory"]["virtual"]["used"], 2)} / {round(sys_data["memory"]["virtual"]["committed"], 2)} GB [{round(sys_data["memory"]["virtual"]["utilisation"], 2)} %]',
                f'[{current_time}] Network IO: [{round(sys_data["network"]["down"])} ↓] [{round(sys_data["network"]["up"])} ↑] Kbit/s',
                f'[{current_time}] Environment: {env_data["temperature"]} °C, {env_data["humidity"]} % Humidity',
                f'[{current_time}] System Uptime: {sys_data["sys_uptime"]}'
            ]

            custom_status = Activity(type=ActivityType.custom, name="Custom status", state=status_list[c_status])
            logging.debug(f"Status set to: {c_status}")
            c_status = (c_status + 1) % len(status_list)

            await bot.change_presence(
                activity=custom_status,
                status=discord.Status.do_not_disturb
            )

        except asyncio.TimeoutError:
            logging.warning("Timed out while getting sys info from the webserver.")
        except Exception as e:
            logging.warning(f"Update Status failed: {e}")

# Make sure it doesnt run before start
@update_status.before_loop
async def before_update_status():
    while started != True:
        await asyncio.sleep(1)

@tasks.loop(seconds=900)  # Runs every 15 minutes
async def clean_database():
    start_clean = time.time()

    # I would use threadpool if it was slightly more complex for consistency, but since its only one operation its probably best to leave as is
    files = await asyncio.to_thread(os.listdir, "./userdata/")

    # concurrent processing using gather
    await asyncio.gather(*(clean_file(file) for file in files))

    time_taken = round(time.time() - start_clean, 2)

    logging.debug(f"Cleaned {len(files)} files in {time_taken} seconds.")

    # Not technically database, but this is a cleaner submarine

    # await async_os_cmd("FOR /F %i IN ('docker ps -aq') DO docker rm -f %i")

# Make sure it doesnt run before start
@clean_database.before_loop
async def before_clean_database():
    while started != True:
        await asyncio.sleep(1)

# Utility subroutines for updating the bot

async def add_val(keyname, keyvalue):
    # I would use threadpool if it was slightly more complex for consistency, but since its only one operation its probably best to leave as is
    files = await asyncio.to_thread(os.listdir, "./userdata/")

    start_op = time.time()

    # concurrent processing using gather
    await asyncio.gather(*(database(file[:file.find(".json")], "WRITE", keyname, keyvalue) for file in files))

    time_taken = round(time.time() - start_op, 2)

    logging.info(f"Created a new entry of {keyname}:{keyvalue} for {len(files)} files in {time_taken} seconds.")

# Run add val anywhere because it was being stubborn
def run_add_val(keyname, keyvalue):
    try:
        asyncio.run(add_val(keyname, keyvalue))
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(add_val(keyname, keyvalue))

start()
