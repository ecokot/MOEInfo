# handlers/player_handler.py

import struct
from utils.logger_config import get_logger
from log_parser.player_handler import PlayerHandler

logger = get_logger()
ph = PlayerHandler()


async def handle_player_query(data, addr, challenge_numbers, players):
    """
    Обрабатывает запрос A2S_PLAYER.
    """
    logger.info(f"Получен корректный запрос A2S_PLAYER от {addr}")

    # Преобразуем список игроков в словарь, если это необходимо
    if isinstance(players, list):
        players = {player["steam_id"]: player for player in players}

    # Извлекаем challenge number (последние 4 байта)
    challenge_number = data[-4:]
    received_challenge_number = struct.unpack('<I', challenge_number)[0]
    logger.debug(f"Challenge number: {received_challenge_number}")

    # Если challenge number не равен 0, проверяем его
    if received_challenge_number != 0:
        expected_challenge_number = challenge_numbers.get(addr)
        if expected_challenge_number is None or expected_challenge_number != received_challenge_number:
            logger.error(
                f"Некорректный challenge number: ожидался {expected_challenge_number}, получен {received_challenge_number}")
            return None

        # Удаляем challenge number из памяти после использования
        del challenge_numbers[addr]

    # Формируем ответ
    response = b'\xFF\xFF\xFF\xFFD' + struct.pack('B', len(players))  # Количество игроков
    for idx, (steam_id, player_data) in enumerate(players.items()):
        response += struct.pack('B', idx + 1)  # Идентификатор игрока
        response += player_data["name"].encode('utf-8') + b'\x00'  # Имя игрока
        response += struct.pack('<i', player_data["score"])  # Счет игрока (little-endian)
        response += struct.pack('<f', player_data["duration"])  # Время игры (little-endian)

    logger.debug(f"Отправлен ответ на запрос A2S_PLAYER: {response}")
    return response
