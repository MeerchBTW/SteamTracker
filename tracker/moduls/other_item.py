from playwright.async_api import async_playwright

from config.browser_settings import browser_settings
from tracker.moduls.cs2 import item 


async def other_item(name_item):
    try:
        async with async_playwright() as p:
            driver = await p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
            context = await browser_settings(driver)

            await item(f"https://csgoskins.gg/items/{name_item}", context)
    except Exception as ex:
        print(ex)