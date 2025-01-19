from playwright.async_api import async_playwright
from fake_useragent import UserAgent


async def browser_settings(driver):
    async with async_playwright() as p:
        context = await driver.new_context(
            user_agent=UserAgent().random,
            viewport={"width": 1280, "height": 720},
            locale="en-US",
            timezone_id="America/New_York",
        )

    return context