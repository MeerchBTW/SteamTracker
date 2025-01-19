from playwright.async_api import async_playwright
import asyncio

from config.browser_settings import browser_settings

# Парсит сам скин на площадках
async def item(url, context, quality_skin="-"):
    try:
        page_skin = await context.new_page()
        # Не загружает не нужные элементы
        await page_skin.route("**/*", lambda route, request: route.abort() if request.resource_type in ["image", "stylesheet", "font", "media"] else route.continue_())
        await page_skin.goto(url, wait_until="load")

        try:
            # Ожидание кноки
            await page_skin.wait_for_selector("button#show-all-active-offers")
            more_playground = await page_skin.query_selector("button#show-all-active-offers")
            # Кнопка для прогрузки всех площадок
            await more_playground.click()
        except:
            pass

        # Ожилание площадок
        await page_skin.wait_for_selector("div.active-offer", timeout=7000)
        # Получение всех площадок
        items = await page_skin.query_selector_all("div.active-offer")
        for i in range(len(items)):
            # Площадка
            playground = await items[i].query_selector("a.hover\\:underline")
            # Сколько ордеров выставлено на этот предмет на площадке
            offers = await items[i].query_selector_all("div.w-full")
            # Цена предмета на этой площадке
            price = await items[i].query_selector("span.text-lg")
            with open("skins.txt", "a", encoding="utf-8") as file:
                file.write(f"Platform: {await playground.inner_text()}\n")
                file.write(f"Price: {await price.inner_text()}\n")
                file.write(f"Orders: {await offers[4].inner_text()}\n")
                file.write(f"Quality: {quality_skin}\n\n")
    except:
        print("There is no such thing")
    finally:
        # Закрытие вкладки
        await page_skin.close()


# Парсит качество скина и получает у него ссылку и передает ее в другую функцию
async def quality(name_skin):
    try:
        async with async_playwright() as p:
            # Браузер для парсинга качества скина
            driver_quality = await p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
            context_quality = await browser_settings(driver_quality)

            # Браузер для парсинга сайтов с скином
            driver_skin = await p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
            context_skin = await browser_settings(driver_skin)

            page_quality = await context_quality.new_page()
            # Не загружает не нужные элементы
            await page_quality.route("**/*", lambda route, request: route.abort() if request.resource_type in ["image", "stylesheet", "font", "media"] else route.continue_())
            await page_quality.goto(f"https://csgoskins.gg/items/{name_skin}", wait_until="load")

            # Ожидание прогрузки элемента с качество оружия
            await page_quality.wait_for_selector("a.version-link", timeout=7000)
            links = await page_quality.query_selector_all("a.version-link")

            tasks = []
            for link in links:
                # Получение ссылки у объекта
                link_quality = await link.get_attribute("href")
                # Получение последнего элемента в массиве
                quality_skin = link_quality.split("/")
                tasks.append(item(link_quality, context_skin, quality_skin[-1]))
            # Запуск всех задач одновременно
            await asyncio.gather(*tasks)

    except:
        print("There is no such thing")
    
    finally:
        # Закрытие вкладки
        await page_quality.close()
        # Закрытие браузера
        await driver_quality.close()
        # Закрытие браузера
        await driver_skin.close()