# API Документация для Minecraft Checker

## Описание
Веб-приложение предоставляет REST API для проверки различных аспектов Minecraft серверов и игроков.

## Базовый URL
`http://127.0.0.1:5000`

## Методы API

### 1. Проверка версии игры
- **URL**: `/api/check_version`
- **Метод**: `POST`
- **Тип контента**: `application/json`
- **Описание**: Проверяет текущую и последнюю версию игры
- **Пример запроса**:
```json
{}
```
- **Пример ответа**:
```json
{
  "success": true,
  "data": "Текущая версия: 1.20.1\nПоследняя версия: 1.20.4\nДата последнего обновления: 2023-10-24"
}
```

### 2. Получение информации об игроке
- **URL**: `/api/get_player_info`
- **Метод**: `POST`
- **Тип контента**: `application/json`
- **Описание**: Получает информацию об игроке по его имени
- **Пример запроса**:
```json
{
  "player_name": "Notch"
}
```
- **Пример ответа**:
```json
{
  "success": true,
  "data": "Информация об игроке Notch:\nplayer_name: Notch\nplayer_uuid: 069a79f444e...283767344b45"
}
```

### 3. Получение информации о сервере
- **URL**: `/api/get_server_info`
- **Метод**: `POST`
- **Тип контента**: `application/json`
- **Описание**: Получает информацию о сервере по его IP-адресу
- **Пример запроса**:
```json
{
  "server_ip": "play.hypixel.net"
}
```
- **Пример ответа**:
```json
{
  "success": true,
  "data": "Информация о сервере play.hypixel.net:\nip: play.hypixel.net\nport: 25565\nonline: True\nmotd: Hypixel Network\nplayers_online: 12500\nplayers_max: 200000\nversion: 1.8-1.20.4"
}
```

### 4. Проверка IP-адреса
- **URL**: `/api/check_ip`
- **Метод**: `POST`
- **Тип контента**: `application/json`
- **Описание**: Проверяет информацию о IP-адресе
- **Пример запроса**:
```json
{
  "ip_address": "8.8.8.8"
}
```
- **Пример ответа**:
```json
{
  "success": true,
  "data": "Результат проверки IP 8.8.8.8:\nip: 8.8.8.8\ncountry: United States\ncountry_code: US\nregion: California\ncity: Mountain View\nlatitude: 37.4056\nlongitude: -122.0775\ntimezone: America/Los_Angeles\nisp: Google LLC"
}
```

## Обработка ошибок
Все API методы возвращают унифицированный формат ответа:
- `success`: boolean - указывает на успешность выполнения операции
- `data`: string - данные в случае успеха
- `error`: string - сообщение об ошибке в случае неудачи