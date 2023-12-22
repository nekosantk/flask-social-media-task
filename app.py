import aiohttp
from flask import Flask
import asyncio

app = Flask(__name__)

async def fetch_data(url):
    try:

        # Fetch data using aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:

                # Check for errors
                response.raise_for_status()

                # Return URL, JSON response
                return url, await response.json()

    # HTTP or JSON error
    except aiohttp.ClientError as ex:

        # Return URL, exception object
        return url, ex


@app.route("/")
def social_network_activity():

    # Endpoints to fetch data
    endpoints = [
        "https://takehome.io/twitter",
        "https://takehome.io/facebook",
        "https://takehome.io/instagram"
    ]

    # Build list of fetch tasks, one for each social media endpoint
    tasks = [fetch_data(endpoint) for endpoint in endpoints]

    # Run fetches in async
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    responses = loop.run_until_complete(asyncio.gather(*tasks))

    response_data = {}

    # Process results & build response data
    for url, response in responses:

        # HTTP or JSON issue maybe, don't process this
        if isinstance(response, Exception):
            print(f"Failed to fetch data from {response}: {response}", flush=True)

        # Looks good, add to response data
        else:
            print(f"Response from {url}: {response}...", flush=True)
            short_url = url.split("/")[-1]
            activity_level = len(response)
            response_data.update({ short_url: activity_level })

    return response_data


if __name__ == "__main__":
    app.run(debug=True)