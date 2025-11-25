import aiohttp
import asyncio
from typing import Optional, Dict, Any


async def get_player_info(player_name: str) -> Optional[Dict[str, Any]]:
    """
    Получает информацию об игроке Minecraft по его имени
    
    Args:
        player_name (str): Имя игрока Minecraft
    
    Returns:
        Optional[Dict[str, Any]]: Словарь с информацией об игроке или None в случае ошибки
    """
    url = f"https://api.mojang.com/users/profiles/minecraft/{player_name}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "player_name": data.get("name"),
                        "player_uuid": data.get("id"),
                        "timestamp": data.get("timestamp")
                    }
                elif response.status == 204:
                    # Игрок не найден
                    return None
                else:
                    print(f"Ошибка при запросе к API Mojang: {response.status}")
                    return None
    except Exception as e:
        print(f"Ошибка при получении информации об игроке: {e}")
        return None


if __name__ == "__main__":
    # Пример использования
    import sys
    if len(sys.argv) > 1:
        player_name = sys.argv[1]
        result = asyncio.run(get_player_info(player_name))
        if result:
            print(f"Игрок: {result['player_name']}")
            print(f"UUID: {result['player_uuid']}")
        else:
            print("Игрок не найден")
    else:
        print("Использование: python player_info.py <имя_игрока>")