import discord

import aiohttp
import inspect

import xmljson

async def request(url, *, headers=None, payload=None, method='GET', attr='json'):
    # Make sure our User Agent is what's set, and ensure it's sent even if no headers are passed
    if headers == None:
        headers = {}
    headers['User-Agent'] = 'User-Agent/1.0.0'

    # Try 5 times
    for i in range(5):
        try:
            # Create the session with our headeres
            with aiohttp.ClientSession(headers=headers) as session:
                # Make the request, based on the method, url, and paramaters given
                async with session.request(method, url, params=payload) as response:
                    # If the request wasn't successful, re-attempt
                    if int(response.status) != 200:
                        continue

                    try:
                        # Get the attribute requested
                        return_value = getattr(response, attr)
                        # Next check if this can be called
                        if callable(return_value):
                            return_value = return_value()
                        # If this is awaitable, await it
                        if inspect.isawaitable(return_value):
                            return_value = await return_value

                        # Then return it
                        return return_value
                    except AttributeError:
                        # If an invalid attribute was requested, return None
                        return None
        # If an error was hit other than the one we want to catch, try again
        except:
            continue