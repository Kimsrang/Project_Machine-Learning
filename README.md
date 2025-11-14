# RTE Generation Forecast – Data Lake (src layout)

## Medallions
- **Bronze**: raw JSON by YYYY/MM/DD
- **Silver**: SQLite timeseries tables per production type
- **Gold**: data-health %missing + D+1 min/max timestamps

## Run order
1) src/rte_forecast/bronze/ingest.py
2) src/rte_forecast/silver/build_timeseries.py
3) src/rte_forecast/gold/indicators.py
