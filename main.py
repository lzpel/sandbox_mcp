#!/usr/bin/env python3
import asyncio
import json
import os
import requests
from mcp.server import Server
from mcp.server.stdio import stdio_server

API_KEY = os.getenv("OPENWEATHER_API_KEY", "YOUR_API_KEY")  # 環境変数または直書き
CITY = os.getenv("WEATHER_CITY", "Tokyo")

server = Server("weather-mcp-server")

@server.tool("get_weather", description="今日の天気を取得する")
async def get_weather() -> str:
    """現在の天気と気温を返す"""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&lang=ja&units=metric"
    resp = requests.get(url)
    if resp.status_code != 200:
        return f"天気情報を取得できませんでした (status={resp.status_code})"
    data = resp.json()
    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    return f"{CITY}の天気: {weather}, 気温: {temp}℃"

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())