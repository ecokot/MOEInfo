import aiohttp
import asyncio
from typing import Optional, Dict, Any


async def get_server_info(server_ip: str) -> Optional[Dict[str, Any]]:
    """
    Получает информацию о сервере Minecraft по его IP-адресу
    
    Args:
        server_ip (str): IP-адрес сервера Minecraft
    
    Returns:
        Optional[Dict[str, Any]]: Словарь с информацией о сервере или None в случае ошибки
    """
    # Пытаемся определить порт из IP-адреса, если он указан
    if ':' in server_ip:
        ip, port = server_ip.split(':')
    else:
        ip = server_ip
        port = 25565  # Стандартный порт Minecraft
    
    # Используем один из публичных API для проверки сервера Minecraft
    url = f"https://api.mcsrvstat.us/2/{ip}:{port}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "ip": ip,
                        "port": port,
                        "online": data.get("online", False),
                        "motd": data.get("motd", {}).get("clean", [""])[0] if data.get("motd") else "N/A",
                        "players_online": data.get("players", {}).get("online", 0),
                        "players_max": data.get("players", {}).get("max", 0),
                        "version": data.get("version", "N/A"),
                        "protocol": data.get("protocol", "N/A"),
                        "hostname": data.get("hostname", "N/A"),
                        "icon": data.get("icon", None)
                    }
                else:
                    print(f"Ошибка при запросе к API статуса сервера: {response.status}")
                    return None
    except Exception as e:
        print(f"Ошибка при получении информации о сервере: {e}")
        return None


if __name__ == "__main__":
    # Пример использования
    import sys
    if len(sys.argv) > 1:
        server_ip = sys.argv[1]
        result = asyncio.run(get_server_info(server_ip))
        if result:
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print("Не удалось получить информацию о сервере")
    else:
        print("Использование: python server_info.py <ip_сервера>")