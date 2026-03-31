import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_ndvi_data(n_records: int = 10):
    """Generate synthetic NDVI sensor data at 15-minute intervals."""
    # Remove this sample code and write the data generation function here
    # now = datetime.now().replace(second=0, microsecond=0)
    # timestamps = [now - timedelta(minutes=15 * i) for i in range(n_records - 1, -1, -1)]

    # NDVI_avg = np.clip(np.random.normal(0.65, 0.08, n_records), -1, 1)
    # LowWatts_m2_avg = np.random.uniform(10, 150, n_records)
    # HighWatts_m2_avg = np.random.uniform(300, 900, n_records)
    # Battery_V_avg = np.random.uniform(12.0, 13.5, n_records)
    # TS_min = np.random.uniform(5.0, 30.0, n_records)

    # df = pd.DataFrame(
    #     {
    #         "LocalDateTime": timestamps,
    #         "NDVI_avg": np.round(NDVI_avg, 4),
    #         "LowWatts_m2_avg": np.round(LowWatts_m2_avg, 2),
    #         "HighWatts_m2_avg": np.round(HighWatts_m2_avg, 2),
    #         "Battery_V_avg": np.round(Battery_V_avg, 2),
    #         "TS_min": np.round(TS_min, 2),
    #     }
    # )

    # return df
