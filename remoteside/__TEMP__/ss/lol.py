import aiohttp
import asyncio

async def fetch_data():
    url = "https://ms32-c67b.onrender.com/control"
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    print(data)
                else:
                    print(f"Failed to fetch data. Status code: {response.status}")
                await asyncio.sleep(0.5)  # Add a small delay to avoid overwhelming the server

# Run the asynchronous function
if __name__ == "__main__":
    asyncio.run(fetch_data())
