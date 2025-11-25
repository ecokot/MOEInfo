# config/settings.py

# Настройки лобби сервера. Указывать ip сервера. Указать Query порт отличный от настроек сервера
SERVER_IP = "192.168.1.3"
QUERY_PORT = 6014
GAME_PORT = 6010
VERSION_GAME = b'1.101'

# Имя сервера для ответа на запросы
SERVER_NAME = b"MOE"

# Пути к файлам логов серверов лобби и сцен сервера
LOG_FILES = [
    "C:\\moe\\serv1\\Myth of Empires Dedicated Server\\MOE\\Saved\\Logs\\LobbyServer_70000.log",
    "C:\\moe\\serv3\\Myth of Empires Dedicated Server\\MOE\\Saved\\Logs\\SceneServer_1007.log",
    "C:\\moe\\serv2\\Myth of Empires Dedicated Server\\MOE\\Saved\\Logs\\SceneServer_1006.log",
    "C:\\moe\\serv4\\Myth of Empires Dedicated Server\\MOE\\Saved\\Logs\\SceneServer_1008.log"
]

# Параметры защиты от DDoS
DDOS_THRESHOLD = 150
DDOS_INTERVAL = 5

# Путь к Steam CMD
STEAMCMD_PATH = "C:\\steamcmd\\steamcmd.exe"  # Укажите путь к вашей Steam CMD
GAME_APP_ID = "1794810"  # Замените на ID вашей игры в Steam

# Файл для хранения текущего change number
VERSION_FILE = r".\data\game_version.json"

# Файл для хранения заблокированных IP
BLOCKED_IPS_FILE = r".\data\blocked_ips.json"

# Файл для хранения данных о игроках
PLAYERS_DATA_FILE = r".\data\players_data.json"



