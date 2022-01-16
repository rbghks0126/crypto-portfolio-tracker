import pandas as pd


def get_mathcing_id(target_tokens_dict,
                    target_tokens_list,
                    all_coins_list):

    # match ticker with token id for API
    for target_name in target_tokens_list:
        for coin_info in all_coins_list:
            if coin_info['symbol'] == target_name.lower():
                target_tokens_dict[target_name] = coin_info['id']
                break
            target_tokens_dict[target_name] = 'NA'

    return target_tokens_dict


def get_market_info(df_f, cg):

    current_market_data = cg.get_coins_markets('usd', per_page=250, page=1)
    for i in range(2, 10):
        current_market_data_next = cg.get_coins_markets(
            'usd', per_page=250, page=i)
        current_market_data += current_market_data_next

    column_dicts = {'symbol': [], 'rank': [], 'market_cap': [], 'price': [],
                    'ATH_date': [], 'ATH': [], 'ATH_change_pct': [],
                    'low_24h': [], 'low_24h_change_pct': []}
    not_found = []

    for index, row in df_f.iterrows():
        found = 0
        for token_info in current_market_data:

            if token_info['symbol'].lower() == row['symbol']:
                found = 1
                column_dicts['symbol'].append(token_info['symbol'].lower())
                column_dicts['rank'].append(token_info['market_cap_rank'])
                column_dicts['market_cap'].append(token_info['market_cap'])
                column_dicts['price'].append(token_info['current_price'])
                column_dicts['ATH_date'].append(token_info['ath_date'])
                column_dicts['ATH'].append(token_info['ath'])
                column_dicts['ATH_change_pct'].append(
                    token_info['ath_change_percentage'])
                column_dicts['low_24h'].append(token_info['low_24h'])
                column_dicts['low_24h_change_pct'].append(
                    ((token_info['current_price'] / token_info['low_24h']) - 1) * 100)

                break
        if found == 0:
            # print(f'ERROR - {row["id"]} NOT FOUND IN CURRENT MARKET DATA')
            not_found.append((row['id']))

    return {'column_dicts': column_dicts,
            'not_found': not_found}


def get_market_info_not_found(not_found, cg):

    not_found_dict = {'symbol': [], 'rank': [], 'market_cap': [], 'price': [],
                      'ATH_date': [], 'ATH': [], 'ATH_change_pct': [],
                      'low_24h': [], 'low_24h_change_pct': []}
    for id_ in not_found:
        token_info = cg.get_coin_by_id(id_)
        not_found_dict['symbol'].append(token_info['symbol'])

        token_info = cg.get_coin_by_id(id_)['market_data']
        try:
            not_found_dict['rank'].append(token_info['market_cap_rank']['usd'])
        except:
            not_found_dict['rank'].append(9999)
        try:
            not_found_dict['market_cap'].append(
                token_info['market_cap']['usd'])
        except:
            not_found_dict['market_cap'].append(0)
        not_found_dict['price'].append(token_info['current_price']['usd'])
        not_found_dict['ATH_date'].append(token_info['ath_date']['usd'])
        not_found_dict['ATH'].append(token_info['ath']['usd'])
        not_found_dict['ATH_change_pct'].append(
            token_info['ath_change_percentage']['usd'])
        try:
            not_found_dict['low_24h'].append(token_info['low_24h']['usd'])
        except:
            not_found_dict['low_24h'].append(0)
        try:
            not_found_dict['low_24h_change_pct'].append(
                ((token_info['current_price']['usd'] /
                 not_found_dict['low_24h'][-1]) - 1) * 100
            )
        except:
            not_found_dict['low_24h_change_pct'].append(0)
    return not_found_dict


def swap_columns(df, col1, col2):
    df = df.copy()
    col_list = list(df)

    index1 = col_list.index(col1)
    index2 = col_list.index(col2)

    col_list[index1], col_list[index2] = col_list[index2], col_list[index1]
    df.columns = col_list
    df[col1], df[col2] = df[col2], df[col1]
    return df


def round_columns(df):
    df = df.copy()
    df['price'] = df.price.round(8).apply(lambda x: '{0:g}'.format(float(x)))
    df['ATH'] = df.ATH.round(8).apply(lambda x: '{0:g}'.format(float(x)))
    df['low_24h'] = df.low_24h.round(8).apply(
        lambda x: '{0:g}'.format(float(x)))
    df['ATH_change_pct'] = df['ATH_change_pct'].round(0).astype('int')
    df['low_24h_change_pct'] = df['low_24h_change_pct'].round(2)
    df['market_cap'] = df.market_cap.round(
        13).apply(lambda x: '{0:g}'.format(float(x)))
    return df


def calc_days_from_ath(df):
    df = df.copy()
    for i, row in df.iterrows():
        df.iloc[i, 4] = row['ATH_date'][:10] + ' ' + row['ATH_date'][11:19]
        df['ATH_date'] = pd.to_datetime(df.ATH_date, utc=True)
        # + (pd.Timestamp.now(tz='utc') - df.ATH_date).dt.seconds / 60 / 60 / 24
        df['ATH_days'] = (pd.Timestamp.now(tz='utc') - df['ATH_date']).dt.days
        df['ATH_days'] = df['ATH_days'].round(2)
    df = swap_columns(df, 'ATH_date', 'ATH_days')
    df.drop('ATH_date', 1, inplace=True)

    return df


def get_row(p_element):
    from datetime import datetime
    from selenium.webdriver.common.by import By

    protocols = p_element[1]
    protocols = protocols.find_elements(By.CLASS_NAME,
                                        'smart-asset-grid__item__header')
    summary = [protocol.text.split('\n') for protocol in protocols]
    protocol = [row[0] for row in summary]
    price = [row[-1][1:] for row in summary]

    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    out_dict = dict()
    out_dict['total'] = sum([float(item) for item in price])
    out_dict['date'] = today
    for col, val in zip(protocol, price):
        out_dict[col] = val
    return out_dict


def insert_row(row, df):
    from datetime import datetime

    if df.empty:
        df = pd.DataFrame()
        df = df.append(row, ignore_index=True)
        return df
    else:
        today = datetime.now().strftime("%Y-%m-%d")
        latest_date = df['date'].max()[:10]
        if today > latest_date:
            df = df.append(row, ignore_index=True)
        return df
