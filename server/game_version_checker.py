# game_version_checker.py
import os
import asyncio
import json
from utils.logger_config import get_logger
from config.settings import VERSION_FILE, STEAMCMD_PATH, GAME_APP_ID


# Инициализация логгера
logger = get_logger()


class GameVersionChecker:
    _instance = None  # Хранит единственный экземпляр класса

    def __new__(cls):
        """
        Создает единственный экземпляр класса (синглтон).
        """
        if cls._instance is None:
            logger.info("Создание нового экземпляра GameVersionChecker.")
            cls._instance = super(GameVersionChecker, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """
        Инициализация атрибутов экземпляра.
        """
        self.current_change_number = self._load_current_change_number()  # Текущий change number
        self.latest_change_number = None  # Последний доступный change number
        self.update_required = False  # Флаг необходимости обновления
        logger.debug(f"Инициализирован текущий change number: {self.current_change_number}")

    def _load_current_change_number(self):
        """
        Загружает текущий change number из файла.
        Если файл не существует, создает новый файл с начальным change number 0.
        """
        if os.path.exists(VERSION_FILE):
            try:
                with open(VERSION_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    change_number = data.get("change_number", None)
                    if not isinstance(change_number, int):
                        raise ValueError("Некорректный change number в файле.")
                    logger.info(f"Загружен текущий change number: {change_number}")
                    return change_number
            except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:
                logger.error(f"Ошибка при загрузке текущего change number: {e}")
                return self._create_default_change_number_file()
        else:
            logger.info("Файл game_version.json не найден. Создается новый файл.")
            return self._create_default_change_number_file()

    def _create_default_change_number_file(self):
        """
        Создает файл с начальным change number (0).
        """
        default_change_number = 0
        try:
            with open(VERSION_FILE, "w", encoding="utf-8") as f:
                json.dump({"change_number": default_change_number}, f, indent=4, ensure_ascii=False)
            logger.info(f"Создан файл game_version.json с начальным change number: {default_change_number}")
            return default_change_number
        except Exception as e:
            logger.error(f"Ошибка при создании файла game_version.json: {e}")
            return None

    def _save_current_change_number(self):
        """
        Сохраняет текущий change number в файл.
        """
        try:
            with open(VERSION_FILE, "w", encoding="utf-8") as f:
                json.dump({"change_number": self.current_change_number}, f, indent=4, ensure_ascii=False)
            logger.debug("Текущий change number успешно сохранен в файл.")
        except Exception as e:
            logger.error(f"Ошибка при сохранении текущего change number: {e}")

    async def check_for_updates(self):
        """
        Проверяет наличие новой версии игры каждые 60 минут.
        """
        while True:
            try:
                # Получаем последний change number через Steam CMD
                self.latest_change_number = await self._get_latest_change_number_from_steamcmd()
                logger.debug(f"Последний доступный change number: {self.latest_change_number}")

                # Сравниваем change number
                if self.latest_change_number and self.current_change_number != self.latest_change_number:
                    self.update_required = True
                    logger.warning(
                        f"Обнаружен новая версия игры: {self.latest_change_number}. Требуется обновление!"
                    )
                else:
                    self.update_required = False
                    logger.debug("Текущия версия игры актуалена.")

            except Exception as e:
                logger.error(f"Ошибка при проверке change number: {e}")

            # Ждем 60 минут перед следующей проверкой
            await asyncio.sleep(60 * 60)

    async def notify_about_update(self):
        """
        Уведомляет о необходимости обновления каждые 5 минут.
        """
        while True:
            if self.update_required:
                logger.warning(f"ТРЕБУЕТСЯ ОБНОВЛЕНИЕ! Новый change number: {self.latest_change_number}")
            await asyncio.sleep(5 * 60)

    async def _get_latest_change_number_from_steamcmd(self):
        """
        Получает последний change number игры через Steam CMD.
        Возвращает целое число с change number или None в случае ошибки.
        """
        try:
            # Команда для проверки информации о игре
            command = f'"{STEAMCMD_PATH}" +login anonymous +app_info_print {GAME_APP_ID} +quit'
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                logger.error(f"Steam CMD завершился с ошибкой: {stderr.decode()}")
                return None

            # Парсим вывод Steam CMD для получения change number
            output = stdout.decode()
            change_number_start = output.find("change number :") + len("change number :")
            change_number_end = output.find("/", change_number_start)
            latest_change_number = output[change_number_start:change_number_end].strip()
            return int(latest_change_number)

        except Exception as e:
            logger.error(f"Ошибка при получении change number через Steam CMD: {e}")
            return None

    def get_current_change_number(self):
        """
        Возвращает текущий change number.
        """
        return self.current_change_number

    def update_game_version(self, new_change_number):
        """
        Обновляет текущий change number.
        :param new_change_number: Новый change number.
        """
        self.current_change_number = new_change_number
        self._save_current_change_number()
        logger.info(f"Текущий change number обновлен: {new_change_number}")



