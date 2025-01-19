import asyncio
import re

from tracker.moduls.weapon import item_weapon
from tracker.moduls.other_item import other_item

async def main():
    name_skin = str(input("Enter a title (Example:\n"
                          "\tSkin (Desert Eagle Mecha Industries, SG 553 Integrale)\n"
                          "\tSticker(Sticker Kimberly)\n"
                          "\tCase (Kilowatt Case)\n"
                          "\tCapsule (Paris 2023 Contenders Sticker Capsule)): "))

    name_skin = re.sub(r'[^a-zA-Z0-9\s-]', '', name_skin).lower().replace("  ", " ").replace(" ", "-")

    print("Please wait...")
    if name_skin.find("sticker") != -1 or name_skin.find("case") != -1 or name_skin.find("package") != -1 or name_skin.find("capsule") != -1 or name_skin.find("pack") != -1 or \
        name_skin.find("box") != -1 or name_skin.find("charm") != -1 or name_skin.find("music") != -1 or name_skin.find("key") != -1 or name_skin.find("patch") != -1 or  \
        name_skin.find("graffiti") != -1:
        await other_item(name_skin)
    else:
        await item_weapon(name_skin)

if __name__ == "__main__":
    asyncio.run(main())