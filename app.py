import aiohttp
from flask import Flask
import asyncio

app = Flask(__name__)

async def fetch_data(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return url, await response.json()
    except aiohttp.ClientError as ex:
        return url, ex


@app.route("/")
def social_network_activity():
    endpoints = [
        "https://takehome.io/twitter",
        "https://takehome.io/facebook",
        "https://takehome.io/instagram"
    ]

    tasks = [fetch_data(endpoint) for endpoint in endpoints]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    responses = loop.run_until_complete(asyncio.gather(*tasks))

    response_data = {}

    for url, response in responses:
        if isinstance(response, Exception):
            print(f"Failed to fetch data from {response}: {response}", flush=True)
        else:
            print(f"Response from {url}: {response}...", flush=True)
            short_url = url.split("/")[-1]
            activity_level = len(response)
            response_data.update({ short_url: activity_level })

    return response_data


if __name__ == "__main__":
    app.run(debug=True)