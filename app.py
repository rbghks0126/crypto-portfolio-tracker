import util_functions
import gsheet_functions


def update_target_list():
    import pandas as pd
    from pycoingecko import CoinGeckoAPI

    # 70 tokens from cryptobanter's youtube video
    target_tokens_list = ['btc', 'eth', 'sol', 'ada', 'luna', 'dot', 'avax', 'matic', 'algo',
                          'ftm', 'uni', 'egld', 'one', 'ar', 'ksm', 'rune', 'rose', 'cel',
                          'sushi', 'jewel', 'spell', 'yfi', 'deso', 'tshare', 'audio',
                          'flux', 'rndr', 'dydx', 'anc', 'tomb', 'any', 'movr', 'ufo',
                          'metis', 'boba', 'ygg', 'uos', 'vr', 'vader', 'soul', 'super',
                          'ewt', 'inj', 'akt', 'pyr', 'rmrk', 'joe', 'qrdo', 'ldo', 'astro',
                          'aioz', 'alu', 'eden', 'stt', 'gog', 'spool', 'unic', 'kuji',
                          'fara', 'prism', 'realm', 'rin', 'don', 'pickle', 'sunny', 'hol',
                          'nii', 'uxp', 'spin', 'bbs']
    token_category = ['sov',
                      'layer 1',
                      'layer 1',
                      'layer 1',
                      'layer 1',
                      'layer 1',
                      'layer 1',
                      'layer 1',
                      'layer 1',
                      'layer 1',
                      'dex',
                      'layer 1',
                      'layer 1',
                      'web 3',
                      'layer 1',
                      'layer 1',
                      'layer 1',
                      'defi',
                      'dex',
                      'defi',
                      'defi',
                      'defi',
                      'social',
                      'defi',
                      'social',
                      'web 3',
                      'web 3',
                      'defi',
                      'defi',
                      'defi',
                      'cross chain',
                      'layer 1',
                      'gaming',
                      'layer 1',
                      'layer 1',
                      'gaming',
                      'gaming/nft',
                      'gaming/nft',
                      'defi',
                      'gaming/nft',
                      'gaming',
                      'other',
                      'cross chain',
                      'web 3',
                      'gaming/nft', 'gaming/nft', 'dex', 'defi', 'defi', 'defi', 'web 3', 'gaming/nft', 'defi', 'launchpad', 'gaming/nft',
                      'defi', 'gaming/nft', 'defi', 'gaming/nft', 'defi', 'gaming/nft', 'dex', 'defi', 'defi', 'defi', 'gaming/nft', 'layer 1',
                      'defi', 'gaming/nft', 'social']

    cg = CoinGeckoAPI()
    all_coins_list = cg.get_coins_list()

    target_tokens_dict = dict()

    # match ticker with token id for API
    target_tokens_dict = util_functions.get_mathcing_id(target_tokens_dict,
                                                        target_tokens_list,
                                                        all_coins_list)

    # initialize dataframe
    df = pd.DataFrame()
    df['symbol'] = list(target_tokens_dict.keys())
    df['symbol'] = df.symbol.str.lower()
    df['id'] = list(target_tokens_dict.values())

    # print(df)

    current_market_data = cg.get_coins_markets('usd')

    # make dataframes for tickers taht exist in current market data and for those that do not
    df_columns_to_add = util_functions.get_market_info(df, cg)
    not_found = util_functions.get_market_info_not_found(
        df_columns_to_add['not_found'], cg)
    df_exist = pd.DataFrame(df_columns_to_add['column_dicts'])
    df_not_found = pd.DataFrame(not_found)

    df_all = df_exist.append(df_not_found)

    # merge price 'df' and info 'df_all'
    df_merge = df.merge(df_all, on='symbol')
    df_merge.drop('id', 1, inplace=True)

    # clean final dataframe
    df_merge = util_functions.swap_columns(df_merge, 'rank', 'symbol')
    df_merge = util_functions.round_columns(df_merge)
    df_merge['category'] = token_category
    df_merge = util_functions.calc_days_from_ath(df_merge)

    df_merge.sort_values(by='rank', inplace=True)
    df_merge.set_index('rank', inplace=True)

    # get target_list sheet
    gsheet_instance_main, df_gsheet = gsheet_functions.get_gsheet_df(
        'gsheet_coin_tracker', 0)
    update_info_main = [row.tolist()
                        for i, row in df_merge.reset_index().iterrows()]
    # update gsheet target_list
    gsheet_functions.update_gsheet(
        gsheet_instance_main, update_info_main, 'A2:J71')

    return '200'


def update_farming():
    import sel_scraper
    from datetime import datetime
    # scrape stake wallet balance from zapper
    url = 'https://zapper.fi/account/0x2638d7d069ee603dc8838ee6710c8e94e130265f'
    sleep_time = 2
    p_element, driver = sel_scraper.get_staking_element(url, sleep_time)

    # get farming sheet instance
    gsheet_instance_farming, df_farming = gsheet_functions.get_gsheet_df(
        'gsheet_coin_tracker', 2)

    row = util_functions.get_row(p_element)
    driver.quit()
    df_farming = util_functions.insert_row(row, df_farming)
    df_farming = df_farming.set_index('total')

    farming_update_info = [row.tolist()
                           for i, row in df_farming.reset_index().iterrows()]

    end_letter = chr(ord('B') + (df_farming.shape[1]) - 1)

    gsheet_functions.update_gsheet(gsheet_instance_farming,
                                   farming_update_info,
                                   f'A2:{end_letter}{df_farming.shape[0]+1}')

    # today = datetime.now().strftime("%Y-%m/%d, %H:%M:%S")
    # latest_date = df_farming.date.max()
    # if today > latest_date:
    #     gsheet_functions.update_gsheet(gsheet_instance_farming,
    #                                    [datetime.now()],
    #                                    f'K2:K2')
    return '200'
