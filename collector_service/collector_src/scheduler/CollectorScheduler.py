from apscheduler.schedulers.asyncio import AsyncIOScheduler

from collector_src.collectors.collector_factory import CollectorFactory
from collector_src.services.price_service import save_prices
from collector_src.utils.logger import get_logger
logger = get_logger(__name__)

"""
CollectorScheduler

This component is mainly responsible for triggering the collection job.
It integrates APScheduler at a fixed time boundary 

Current schedule:
    - every minute and 30s

Pipeline:
    Scheduler (triggered) -> CoingeckoCollector -> prices persistence -> DB
"""
class CollectorScheduler:

    def __init__(self):
        # APScheduler instance declaration
        self.scheduler = AsyncIOScheduler()

        # Factory pattern declaration to create configured collector instance
        # Expandable to other collectors in the future
        self.collector = CollectorFactory().create()

    async def collect(self):
        """
        Main scheduled task
        Steps:
        1. Fetch the prices.
        2. Validate the response data.
        3. Persist the data to the database.
        """
        logger.info("Starting price collector job")
        prices = await self.collector.fetch_prices()
        if not prices:
            logger.warning("no price data collected")
            return
        await save_prices(prices)

    def start(self):
        logger.info("Scheduler running at second 00 and 30")

        self.scheduler.add_job(
            self.collect,
            trigger="cron",
            second="0,30",
            max_instances=1,
            coalesce=True
        )

        self.scheduler.start()
