from tortoise.fields import BigIntField, BooleanField, DatetimeField
from tortoise import Tortoise, fields, Model


async def init_db_connection():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3", modules={"models": ["services.db_service"]}
    )
    await Tortoise.generate_schemas()


class Database(Model):
    user_id = fields.BigIntField(pk=True, unique=True)
    notifications_enabled = fields.BooleanField(default=True)

    class Meta:
        table = "Users"


async def turn_on_notifications(user_id: int):
    await Database.update_or_create(
        user_id=user_id, defaults={"notifications_enabled": True}
    )


async def turn_off_notifications(user_id: int):
    user = await Database.get(user_id=user_id)
    user.notifications_enabled = False
    await user.save()


async def get_all_notificated_users() -> list[int]:
    return await Database.filter(notifications_enabled=True).values_list(
        "user_id", flat=True
    )
