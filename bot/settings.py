from environs import Env

env = Env()
env.read_env()

with env.prefixed("BOT_"):
    TOKEN = env.str("TOKEN", default="")
    FILES_DIR_PATH = env.str("FILES_DIR_PATH")
    STATS_FILE = env.str("STATS_FILE")
