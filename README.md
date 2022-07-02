# historical-data-downloader

Python scripts to download historical data from cryptocurrency exchanges.

## Binance

```bash
mkdir -p futures/um/monthly/aggTrades
aws --no-sign-request s3 sync s3://data.binance.vision/data/futures/um/monthly/aggTrades futures/um/monthly/aggTrades
```

## OKX

```bash
python3 okx-data-downloader.py 2022-06 ./data
```

## References

* <https://github.com/binance/binance-public-data/>
* <https://help.ftx.com/hc/en-us/articles/360045023032-Historical-Data>
* <https://www.okx.com/historical-data>
