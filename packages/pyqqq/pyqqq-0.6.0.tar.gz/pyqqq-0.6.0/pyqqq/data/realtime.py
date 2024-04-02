from pyqqq.utils.logger import get_logger
import datetime as dtm
import pandas as pd
import pyqqq
import pyqqq.config as c
import pytz
import requests

logger = get_logger("realtime")

def get_all_last_trades():
    '''
    모든 종목의 최근 체결 정보를 반환합니다.

    Returns:
        list:
        - dict:
            - chetime (str): 체결시간
            - sign (str): 전일대비구분
            - change (int): 전일대비가격
            - drate (float): 전일대비등락율
            - price (int): 체결가
            - opentime (str): 시가시간
            - open (int): 시가
            - hightime (str): 고가시간
            - high (int): 고가
            - lowtime (str): 저가시간
            - low (int): 저가
            - cgubun (str): 체결구분
            - cvolume (int): 체결량
            - value (int): 누적거래대금
            - mdvolume (int): 매도체결수량
            - mdchecnt (int): 매도체결건수
            - msvolume (int): 매수체결수량
            - mschecnt (int): 매수체결건수
            - cpower (float): 체결강도
            - offerho (int): 매도호가
            - bidho (int): 매수호가
            - status (str): 장정보
            - jnilvolume (int): 전일거래량
            - shcode (str): 종목코드

    '''

    r = requests.get(f'https://qupiato.com/api/domestic-stock/trades')
    r.raise_for_status()

    data = r.json()
    result = [data[k] for k in data.keys()]

    return result


def get_all_minute_data(
    time: dtm.datetime, include_empty: bool = False
) -> pd.DataFrame:
    """
    모든 종목의 분봉 데이터를 반환합니다.

    Args:
        time (dtm.datetime): 조회할 시간
        include_empty (bool): 거래가 없는 종목 데이터도 포함할지 여부 (기본값: False)

    Returns:
        pd.DataFrame: 요청한 시간의 모든 종목의 분봉 데이터를 담은 DataFrame

        - code (str): 종목 코드
        - time (dtm.datetime): 시간
        - open (int): 시가
        - high (int): 고가
        - low (int): 저가
        - close (int): 종가
        - volume (int): 거래량

    Examples:
        >>> df = get_all_minute_data(dtm.datetime(2024, 4, 2, 13, 0))
        >>> print(df)
                                time    open    high     low   close  volume
        code
        310210 2024-04-02 13:00:00   33400   33450   33400   33450      11
        000270 2024-04-02 13:00:00  104300  104500  104300  104500    7386
        359090 2024-04-02 13:00:00    1449    1456    1447    1451   21871
        003670 2024-04-02 13:00:00  288000  288000  287500  288000      91
        028300 2024-04-02 13:00:00  100400  100500  100300  100500    4701
        ...                    ...     ...     ...     ...     ...     ...
        002600 2024-04-02 13:00:00  171900  171900  171900  171900       1
        001725 2024-04-02 13:00:00   63400   63400   63400   63400      83
        005745 2024-04-02 13:00:00    9770    9770    9770    9770     400
        032685 2024-04-02 13:00:00   10090   10090   10090   10090      12
        003075 2024-04-02 13:00:00   13790   13790   13790   13790       1

        [1981 rows x 6 columns]
    """
    tz = pytz.timezone("Asia/Seoul")

    url = f"{c.PYQQQ_API_URL}/domestic-stock/ohlcv/minutes/all/{time.date()}/{time.strftime('%H%M')}"
    if include_empty:
        url += "?includeEmpty=true"

    r = requests.get(url, headers={"Authorization": f"Bearer {pyqqq.get_api_key()}"})
    if r.status_code != 200 and r.status_code != 201:
        logger.error(f"Failed to get minute data: {r.text}")
        return

    rows = r.json()
    for data in rows:
        time = (
            dtm.datetime.fromisoformat(data["time"]).astimezone(tz).replace(tzinfo=None)
        )
        data["time"] = time

    df = pd.DataFrame(rows)
    if not df.empty:
        df.set_index("code", inplace=True)

    return df
