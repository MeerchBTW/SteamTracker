from tracker.moduls.cs2 import quality


async def item_weapon(name_weapon):
    try:
        await quality(name_weapon)
    except Exception as ex:
        print(ex)