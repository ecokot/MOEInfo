# main.py
import asyncio
from server.query_server import QueryServer
from server.game_version_checker import GameVersionChecker
from utils.logger_config import get_logger
from config.settings import SERVER_IP, QUERY_PORT, LOG_FILES

# Инициализация логгера
logger = get_logger()


async def main():
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
        await server.main()
    except Exception as e:
        logger.error(f"Критическая ошибка сервера: {e}")


if __name__ == "__main__":

    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")

