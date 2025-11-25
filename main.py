#!/usr/bin/env python3
# main.py
import asyncio
import sys
import argparse
from server.query_server import QueryServer
from server.game_version_checker import GameVersionChecker
from server.player_info import get_player_info
from server.server_info import get_server_info
from utils.ip_checker import check_ip
from utils.logger_config import get_logger
from config.settings import SERVER_IP, QUERY_PORT, LOG_FILES

# Инициализация логгера
logger = get_logger()


def check_version():
    """Проверка версии игры"""
    try:
        version_checker = GameVersionChecker()
        # Получаем информацию о версии напрямую из метода
        result = asyncio.run(version_checker.get_latest_version_info())
        if result:
            print(f"Текущая версия: {result.get('current_version', 'Неизвестна')}")
            print(f"Последняя версия: {result.get('latest_version', 'Неизвестна')}")
            print(f"Дата последнего обновления: {result.get('update_date', 'Неизвестна')}")
        else:
            print("Не удалось получить информацию о версии")
    except Exception as e:
        print(f"Ошибка при проверке версии: {e}", file=sys.stderr)


async def check_version_async():
    """Асинхронная версия проверки версии для внутреннего использования"""
    version_checker = GameVersionChecker()
    return await version_checker.get_latest_version_info()


def handle_get_player_info(player_name):
    """Получение информации об игроке"""
    try:
        result = asyncio.run(get_player_info(player_name))
        if result:
            print(f"Информация об игроке {player_name}:")
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print(f"Информация об игроке {player_name} не найдена")
    except Exception as e:
        print(f"Ошибка при получении информации об игроке: {e}", file=sys.stderr)


def handle_get_server_info(server_ip):
    """Получение информации о сервере"""
    try:
        result = asyncio.run(get_server_info(server_ip))
        if result:
            print(f"Информация о сервере {server_ip}:")
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print(f"Информация о сервере {server_ip} не найдена")
    except Exception as e:
        print(f"Ошибка при получении информации о сервере: {e}", file=sys.stderr)


def handle_check_ip(ip_address):
    """Проверка IP-адреса"""
    try:
        result = check_ip(ip_address)
        if result:
            print(f"Результат проверки IP {ip_address}:")
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print(f"Не удалось получить информацию для IP {ip_address}")
    except Exception as e:
        print(f"Ошибка при проверке IP: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description='Minecraft Checker CLI')
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')

    # Подкоманда для проверки версии
    subparsers.add_parser('check_version', help='Проверить версию игры')

    # Подкоманда для получения информации об игроке
    player_parser = subparsers.add_parser('get_player_info', help='Получить информацию об игроке')
    player_parser.add_argument('player_name', help='Имя игрока')

    # Подкоманда для получения информации о сервере
    server_parser = subparsers.add_parser('get_server_info', help='Получить информацию о сервере')
    server_parser.add_argument('server_ip', help='IP-адрес сервера')

    # Подкоманда для проверки IP
    ip_parser = subparsers.add_parser('check_ip', help='Проверить IP-адрес')
    ip_parser.add_argument('ip_address', help='IP-адрес для проверки')

    args = parser.parse_args()

    if args.command == 'check_version':
        check_version()
    elif args.command == 'get_player_info':
        handle_get_player_info(args.player_name)
    elif args.command == 'get_server_info':
        handle_get_server_info(args.server_ip)
    elif args.command == 'check_ip':
        handle_check_ip(args.ip_address)
    else:
        # Если не указана команда, запускаем сервер как обычно
        logger.info("Запуск сервера...")

        # Инициализация QueryServer
        server = QueryServer(SERVER_IP, QUERY_PORT, LOG_FILES)

        # Инициализация GameVersionChecker
        version_checker = GameVersionChecker()
        # Запускаем задачи для проверки обновлений и уведомлений
        asyncio.create_task(version_checker.check_for_updates())
        asyncio.create_task(version_checker.notify_about_update())

        # Запускаем основной цикл сервера
        try:
            asyncio.run(server.main())
        except Exception as e:
            logger.error(f"Критическая ошибка сервера: {e}")


if __name__ == "__main__":
    main()

