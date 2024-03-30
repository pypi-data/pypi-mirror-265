import datetime
import logging
import time
import typing as T

import tinkoff.invest as ti

from market_database.common import utils
from market_database.seeker import utils as seeker_utils


logger = utils.get_logger(__name__)


class BatchingPeriod:
    BATCHING_MONTH = "month"
    BATCHING_3_MONTH = "3 month"
    BATCHING_6_MONTH = "6 month"


BATCHING_PERIOD_DELTA = {
    BatchingPeriod.BATCHING_MONTH: datetime.timedelta(days=30),
    BatchingPeriod.BATCHING_3_MONTH: datetime.timedelta(days=90),
    BatchingPeriod.BATCHING_6_MONTH: datetime.timedelta(days=180),
}


class HistorySeeker:
    def __init__(self, api_token: str, batching_period: str = BatchingPeriod.BATCHING_MONTH):
        self._api_token = api_token
        self._batching_period = batching_period

    def seek(
        self,
        ticker: str,
        from_date: datetime.date,
        to_date: datetime.date,
        interval_name: str,
    ) -> T.Set[ti.schemas.HistoricCandle]:
        figi = seeker_utils.get_ticker_figi(ticker)
        interval = utils.get_interval_from_name(interval_name)

        logger.info(f"Use batching period {self._batching_period}")

        candle_data = set()
        current_from_date = from_date
        previous_from_date = None
        current_to_date = None
        with ti.Client(self._api_token) as client:
            while previous_from_date != current_from_date or current_to_date != to_date:
                previous_from_date = current_from_date
                current_to_date = min(current_from_date + BATCHING_PERIOD_DELTA[self._batching_period], to_date)

                logger.info(f"Current request interval: {current_from_date} - {current_to_date}")
                try:
                    current_candles = list(
                        client.get_all_candles(figi=figi, from_=current_from_date, to=current_to_date, interval=interval)
                    )
                    candle_data.update(current_candles)

                    current_from_date = max(candle.time for candle in current_candles).replace(tzinfo=None)
                except ti.exceptions.RequestError as e:
                    sleep_time = e.metadata.ratelimit_reset
                    logger.info(f"Wait {sleep_time} seconds")
                    time.sleep(sleep_time)

        return candle_data
