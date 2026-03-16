from apscheduler.schedulers.asyncio import AsyncIOScheduler

from feature_src.services.feature_service import build_features
from feature_src.utils.logger import get_logger

logger = get_logger(__name__)

class FeatureScheduler:
    """
    Scheduler class responsible for periodically generating techinical
    indicators from candle data.
    """

    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    def start(self):
        logger.info("Starting feature scheduler")
        # the calculation executed every minute
        self.scheduler.add_job(
            build_features,
            trigger="cron",
            second=10,  # delay 10s, making sure the candles are properly generated.
            max_instances=1,
            coalesce=True
            )

        self.scheduler.start()
        logger.info("Feature scheduler started")