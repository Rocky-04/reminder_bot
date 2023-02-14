from tgbot.models.models import UserManager, PeriodicityManager, NotificationManager


async def get_default_data(bot) -> None:
    print('-----------------create_test_data---------------------------')
    session = bot['session_maker']
    periodicity_manager = PeriodicityManager(session=session)

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
    return