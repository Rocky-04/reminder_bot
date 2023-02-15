import logging

from tgbot.models.models import PeriodicityManager

logger = logging.getLogger(__name__)


async def get_default_data(bot) -> None:
    """
    Create default periodicity records if none exist in the database.

    :param bot: The bot instance.
    :return: None
    """
    session = bot['db']
    periodicity_manager = PeriodicityManager(session=session)
    if await periodicity_manager.get_all():
        return
    await periodicity_manager.create(name='Do not repeat', interval=0)
    await periodicity_manager.create(name='One time per half hour', interval=30)
    await periodicity_manager.create(name='One time per hour"', interval=60)
    await periodicity_manager.create(name='One time per 3 hour', interval=3 * 60)
    await periodicity_manager.create(name='One time per 1 day ', interval=24 * 60)
    await periodicity_manager.create(name='One time per 3 days', interval=24 * 60 * 3)
    await periodicity_manager.create(name='One time per 7 days', interval=24 * 60 * 7)
    await periodicity_manager.create(name='One time per 30 day', interval=24 * 60 * 30)
    await periodicity_manager.create(name='One time per 90 day', interval=24 * 60 * 90)
    await periodicity_manager.create(name='One time per 180 day', interval=24 * 60 * 180)
    await periodicity_manager.create(name='One time per 365 day', interval=24 * 60 * 365)
    logger.info("----------create_default_data----------")
    return
