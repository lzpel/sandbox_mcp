import asyncio
from mcp import Client
import requests

async def main():
    # MCPサーバー接続
    client = await Client.connect_stdio("python server.py")

    # Ollamaに質問
    prompt = "次の数字を足し算して: 3 + 5"
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "phi4",
        "prompt": prompt
    })
    print("Ollama Response:", response.json()["response"])

    # MCPツール(add)呼び出し
    result = await client.call("add", {"a": 3, "b": 5})
    print("MCP Tool Result:", result["content"])

asyncio.run(main())