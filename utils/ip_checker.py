import aiohttp
import asyncio
from typing import Optional, Dict, Any


def check_ip(ip_address: str) -> Optional[Dict[str, Any]]:
    """
    Проверяет IP-адрес с помощью внешнего API
    
    Args:
        ip_address (str): IP-адрес для проверки
    
    Returns:
        Optional[Dict[str, Any]]: Словарь с информацией об IP-адресе или None в случае ошибки
    """
    import subprocess
    import json
    
    try:
        # Используем сервис ip-api.com для получения информации об IP
        result = subprocess.run(['curl', '-s', f'http://ip-api.com/json/{ip_address}'], 
                                capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data.get('status') == 'success':
                return {
                    "ip": ip_address,
                    "country": data.get('country', 'N/A'),
                    "country_code": data.get('countryCode', 'N/A'),
                    "region": data.get('regionName', 'N/A'),
                    "city": data.get('city', 'N/A'),
                    "zip_code": data.get('zip', 'N/A'),
                    "latitude": data.get('lat', 'N/A'),
                    "longitude": data.get('lon', 'N/A'),
                    "timezone": data.get('timezone', 'N/A'),
                    "isp": data.get('isp', 'N/A'),
                    "org": data.get('org', 'N/A'),
                    "as": data.get('as', 'N/A')
                }
            else:
                print(f"Сервис вернул ошибку: {data.get('message', 'Неизвестная ошибка')}")
                return None
        else:
            print(f"Ошибка при запросе к API проверки IP: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        print("Таймаут выполнения команды проверки IP")
        return None
    except Exception as e:
        print(f"Ошибка при проверке IP: {e}")
        return None


async def check_ip_async(ip_address: str) -> Optional[Dict[str, Any]]:
    """
    Асинхронная версия проверки IP-адреса
    
    Args:
        ip_address (str): IP-адрес для проверки
    
    Returns:
        Optional[Dict[str, Any]]: Словарь с информацией об IP-адресе или None в случае ошибки
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://ip-api.com/json/{ip_address}', timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('status') == 'success':
                        return {
                            "ip": ip_address,
                            "country": data.get('country', 'N/A'),
                            "country_code": data.get('countryCode', 'N/A'),
                            "region": data.get('regionName', 'N/A'),
                            "city": data.get('city', 'N/A'),
                            "zip_code": data.get('zip', 'N/A'),
                            "latitude": data.get('lat', 'N/A'),
                            "longitude": data.get('lon', 'N/A'),
                            "timezone": data.get('timezone', 'N/A'),
                            "isp": data.get('isp', 'N/A'),
                            "org": data.get('org', 'N/A'),
                            "as": data.get('as', 'N/A')
                        }
                    else:
                        print(f"Сервис вернул ошибку: {data.get('message', 'Неизвестная ошибка')}")
                        return None
                else:
                    print(f"Ошибка при запросе к API проверки IP: {response.status}")
                    return None
    except asyncio.TimeoutError:
        print("Таймаут выполнения запроса проверки IP")
        return None
    except Exception as e:
        print(f"Ошибка при проверке IP: {e}")
        return None


if __name__ == "__main__":
    # Пример использования
    import sys
    if len(sys.argv) > 1:
        ip_address = sys.argv[1]
        result = check_ip(ip_address)
        if result:
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print("Не удалось получить информацию об IP-адресе")
    else:
        print("Использование: python ip_checker.py <ip_адрес>")