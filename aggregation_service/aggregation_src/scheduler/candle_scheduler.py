from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aggregation_src.services.candle_service import build_candles
from aggregation_src.utils.logger import get_logger

logger = get_logger(__name__)

class CandleScheduler:
    """
    Scheduler responsible for triggering candle generation jobs.

    This class periodically triggers candle_service.build_candles(), aggregating
    raw crypto price data into 1-minute candle.

    """
    def __init__(self):
        self.scheduler = AsyncIOScheduler()  # APScheduler instance initialization

    def start(self):
        """
        Start the candle generation scheduler service.

        The job runs at every minute.
        """

        logger.info("Starting candle scheduler")

        self.scheduler.add_job(
            build_candles,

            # runs at every minute (second 0)
            trigger="cron",
            second=0,

            # prevention of overlapping executions if the previous job is still running.
            max_instances=1,

            # if execution falls behind, merge pending executions into 1.
            coalesce=True  # the pending jobs will be executed at once, but not to aggregate them.
        )

        self.scheduler.start()  # job activation

        logger.info("Candle scheduler started")

