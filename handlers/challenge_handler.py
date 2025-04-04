# handlers/challenge_handler.py

import random
import struct
from utils.logger_config import get_logger

logger = get_logger()


async def handle_challenge_query(data, addr, challenge_numbers):
    """
    Обрабатывает запрос A2S_SERVERQUERY_GETCHALLENGE.
    """
    logger.info(f"Получен корректный запрос A2S_SERVERQUERY_GETCHALLENGE от {addr}")

    # Генерируем случайный challenge number
    challenge_number = random.randint(1, 2 ** 32 - 1)
    packed_challenge_number = struct.pack('<I', challenge_number)  # Little-endian

    # Сохраняем challenge number для этого адреса
    challenge_numbers[addr] = challenge_number
    logger.debug(f"Сгенерирован challenge number: {challenge_number}")

    # Формируем ответ
    response = b'\xFF\xFF\xFF\xFFA' + packed_challenge_number
    logger.debug(f"Отправлен ответ на запрос A2S_SERVERQUERY_GETCHALLENGE: {response}")
    return response
