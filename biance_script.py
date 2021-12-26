# <------------------------------------------------------------------------------------------------------------------> #
import os.path
import asyncio
import datetime as dt
from time import time
from datetime import datetime

import psycopg2
import psycopg2.extras
from binance.client import AsyncClient
from binance.client import BinanceAPIException

from googleapiclient.discovery import build
from google.oauth2 import service_account
from calendar import monthrange
from dotenv import load_dotenv

from mainapp.google_views import GoogleSheetsApp
# <------------------------------------------------------------------------------------------------------------------> #
load_dotenv()
# <------------------------------------------------------------------------------------------------------------------> #
class DB:
    '''
        The class is used to provide accounts from the database,
                    for further data processing
    '''
    def __init__(self):
        try:
            self._connection = psycopg2.connect(os.getenv('DATABASE_URL'))
        except Exception as err:
            raise RuntimeError('Error: Step 29 {}'.format(err))

        self._cursor = self._connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def select_data(self) -> dict:
        '''
            Returns a list of all accounts
            :return: dict(account1, account2 ... accountN)
        '''
        try:
            self._cursor.execute('''SELECT * FROM accounts;''')
            res = self._cursor.fetchall()
            self._connection.close()
            if res: return res
        except Exception as e:
            raise RuntimeError('Error: Step 41 {}'.format(e))
        return []
# <------------------------------------------------------------------------------------------------------------------> #
class GoogleSheetsForBinance(GoogleSheetsApp):
    '''
        This class is used to write to Google Sheets
    '''
    def get_yesterday_balance(self, title: str) -> dict:
        '''
            This method returns yesterday's balance
            :param title: Account name
            :param accounts: {'FUTURE': True or False, 'MARGIN': True or False}
        '''
        # Yesterday's date
        yesterday = dt.datetime.now() - dt.timedelta(1)
        day = yesterday.day
        month = 'Месяц: ' + self.MONTH[yesterday.month] + ' | Год: ' + str(datetime.now().year)

        # Return all months
        try:
            values: list = self._service.values().get(
                spreadsheetId=self._SAMPLE_SPREADSHEET_ID,
                range=self._SAMPLE_RANGE_NAME + f'!A2:ZZ2',
            ).execute().get('values', [])
        except Exception as e:
            print('Error "GoogleSheetsForBinance.get_yesterday_balance": Step 66 {}'.format(e))

        # Looking for the right month
        count, flag = -2, False
        for val in values[0]:
            count += 1
            if month in val:
                flag = True
                break

        if flag:
            # Yesterday's number by index
            yest: tuple = super().get_date(count+day, 0)[0]

            try:
                # We are looking for the right account
                result: list = self._service.values().get(
                    spreadsheetId=self._SAMPLE_SPREADSHEET_ID,
                    range=self._SAMPLE_RANGE_NAME + '!B:B'
                ).execute().get('values', [])
            except Exception as e:
                print('Error "GoogleSheetsForBinance.get_yesterday_balance": Step 87 {}'.format(e))

            # The index in which the account name is located
            c = 0
            for res in result:
                c += 1
                if title in res:
                    break

            range_names = [
                # Total score
                self._SAMPLE_RANGE_NAME + f'!{yest}{c}',
                # SPOT account
                self._SAMPLE_RANGE_NAME + f'!{yest}{c + 5}',
                # Balance FUTURES
                self._SAMPLE_RANGE_NAME + f'!{yest}{c + 10}'
            ]

            try:
                # We get yesterday's balance
                get_yesterday_balance: list = self._service.values().batchGet(
                    spreadsheetId=self._SAMPLE_SPREADSHEET_ID,
                    ranges=range_names
                ).execute().get('valueRanges', [])
            except Exception as e:
                print('Error "GoogleSheetsForBinance.get_yesterday_balance": Step 112 {}'.format(e))

            # Overall balance
            overall_balance = float(get_yesterday_balance[0]['values'][0][0].replace(',', '.')) if 'values' in \
                                                                                                   get_yesterday_balance[
                                                                                                       0] else 0
            # SPOT balance
            spot_balance = float(get_yesterday_balance[1]['values'][0][0].replace(',', '.')) if 'values' in \
                                                                                                get_yesterday_balance[
                                                                                                    1] else 0
            # FUTURES balance
            futures_balance = float(get_yesterday_balance[2]['values'][0][0].replace(',', '.')) if 'values' in \
                                                                                                   get_yesterday_balance[
                                                                                                       2] else 0
            allBalances = {
                'BALANCE': overall_balance,
                'SPOT': spot_balance,
                'FUTURES': futures_balance
            }

            return allBalances
        else:
            allBalances = {
                'BALANCE': 0,
                'SPOT': 0,
                'FUTURE': 0,
            }
            return allBalances

    def add_data(self, args: dict) -> str:
        '''
            The function adds data for today

            :param args: Data to be entered into the table
        '''
        print('Account: "{}" | Start recording'.format(args['title']))

        now = datetime.now()
        day = now.day
        month = 'Месяц: ' + self.MONTH[now.month] + ' | Год: ' + str(datetime.now().year)
        days = monthrange(datetime.now().year, now.month)[1]

        try:
            values: list = self._service.values().get(
                spreadsheetId=self._SAMPLE_SPREADSHEET_ID,
                range=self._SAMPLE_RANGE_NAME + f'!A2:ZZ2',
            ).execute().get('values', [])
        except Exception as e:
            print('Error "GoogleSheetsForBinance.add_data": Step 160 {}'.format(e))

        count = -2
        for val in values[0]:
            count += 1
            if month in val:
                break

        yest: tuple = super().get_date(count + day, 0)[0]

        try:
            result: list = self._service.values().get(
                spreadsheetId=self._SAMPLE_SPREADSHEET_ID,
                range=self._SAMPLE_RANGE_NAME + '!B:B'
            ).execute().get('values', [])
        except Exception as e:
            print('Error "GoogleSheetsForBinance.add_data": Step 176 {}'.format(e))

        c = 0
        for res in result:
            c += 1
            if args['title'] in res:
                break

        j: list = GoogleSheetsForBinance().get_date(count + days + 1, count + days + 3)

        try:
            self._service.values().batchUpdate(
                spreadsheetId=self._SAMPLE_SPREADSHEET_ID,
                body={
                    'valueInputOption': 'RAW',
                    'data': [
                        {
                            'range': self._SAMPLE_RANGE_NAME + f'!{yest}{c}:{yest}{c + 15}',
                            'majorDimension': 'COLUMNS',
                            'values': [[args['overall_balance'], args['profit_account_usdt'], args['profit_account_percent'],
                                        args['withdraw'], args['deposit'], args['balance_spot'], args['profit_spot_usdt'],
                                        args['profit_spot_percent'], args['commission_spot'], args['equity_spot'],
                                        args['balance_future'], args['profit_future_usdt'],
                                        args['profit_future_percent'], args['commission_future'], args['equity_futures']]]},
                        {
                            'range': self._SAMPLE_RANGE_NAME + f'!{j[0]}{c}',
                            'majorDimension': 'COLUMNS',
                            'values': [[args['overall_balance']], [args['overall_balance']], [args['overall_balance']]]
                        },
                        {
                            'range': self._SAMPLE_RANGE_NAME + f'!{j[0]}{c + 5}',
                            'majorDimension': 'COLUMNS',
                            'values': [[args['balance_spot']], [args['balance_spot']], [args['balance_spot']]]
                        },
                        {
                            'range': self._SAMPLE_RANGE_NAME + f'!{j[0]}{c + 9}',
                            'majorDimension': 'COLUMNS',
                            'values': [[args['equity_spot']], [args['equity_spot']], [args['equity_spot']]]
                        },
                        {
                            'range': self._SAMPLE_RANGE_NAME + f'!{j[0]}{c + 10}',
                            'majorDimension': 'COLUMNS',
                            'values': [[args['balance_future']], [args['balance_future']], [args['balance_future']]]
                        },
                        {
                            'range': self._SAMPLE_RANGE_NAME + f'!{j[0]}{c + 14}',
                            'majorDimension': 'COLUMNS',
                            'values': [[args['equity_futures']], [args['equity_futures']], [args['equity_futures']]]
                        }
                    ]
                }
            ).execute()

            print('Account: "{}" | recorded by'.format(args["title"]))

            return yest
        except Exception as e:
            print('Error "GoogleSheetsForBinance.add_data": Step 192 {}'.format(e))

    def add_all_balance_for_all_accounts(self, args: dict) -> None:
        '''
            This method adds to the "All accounts" field
            The sum of all accounts, namely: Total Balance, Spot Balance, Spot Equity, Futures Balance, Futures Equity
        '''
        try:
            self._service.values().batchUpdate(
                spreadsheetId=self._SAMPLE_SPREADSHEET_ID,
                body={
                    'valueInputOption': 'USER_ENTERED',
                    'data': [
                        {
                            'range': self._SAMPLE_RANGE_NAME + '!{}6'.format(args['now_day']),
                            'majorDimension': 'COLUMNS',
                            'values': [[args['all_balance']]]
                        },
                        {
                            'range': self._SAMPLE_RANGE_NAME + '!{}7'.format(args['now_day']),
                            'majorDimension': 'COLUMNS',
                            'values': [[args['all_profit_sum']]]
                        },
                        {
                            'range': self._SAMPLE_RANGE_NAME + '!{}8'.format(args['now_day']),
                            'majorDimension': 'COLUMNS',
                            'values': [[args['all_profit_percent']]]
                        },
                        {
                            'range': self._SAMPLE_RANGE_NAME + '!{}9'.format(args['now_day']),
                            'majorDimension': 'COLUMNS',
                            'values': [[args['all_withdraw']]]
                        },
                        {
                            'range': self._SAMPLE_RANGE_NAME + '!{}10'.format(args['now_day']),
                            'majorDimension': 'COLUMNS',
                            'values': [[args['all_deposits']]]
                        },
                        {
                            'range': self._SAMPLE_RANGE_NAME + '!{}11'.format(args['now_day']),
                            'majorDimension': 'COLUMNS',
                            'values': [[args['all_spot_balance']]]
                        },
                        {
                            'range': self._SAMPLE_RANGE_NAME + '!{}12'.format(args['now_day']),
                            'majorDimension': 'COLUMNS',
                            'values': [[args['all_spot_profit_sum']]]
                        },
                        {
                            'range': self._SAMPLE_RANGE_NAME + '!{}13'.format(args['now_day']),
                            'majorDimension': 'COLUMNS',
                            'values': [[args['all_spot_profit_percent']]]
                        },
                        {
                            'range': self._SAMPLE_RANGE_NAME + '!{}14'.format(args['now_day']),
                            'majorDimension': 'COLUMNS',
                            'values': [[args['all_spot_commissions']]]
                        },
                        {
                            'range': self._SAMPLE_RANGE_NAME + '!{}15'.format(args['now_day']),
                            'majorDimension': 'COLUMNS',
                            'values': [[args['all_spot_equity']]]
                        },
                        {
                            'range': self._SAMPLE_RANGE_NAME + '!{}16'.format(args['now_day']),
                            'majorDimension': 'COLUMNS',
                            'values': [[args['all_futures_balance']]]
                        },
                        {
                            'range': self._SAMPLE_RANGE_NAME + '!{}17'.format(args['now_day']),
                            'majorDimension': 'COLUMNS',
                            'values': [[args['all_futures_profit_sum']]]
                        },
                        {
                            'range': self._SAMPLE_RANGE_NAME + '!{}18'.format(args['now_day']),
                            'majorDimension': 'COLUMNS',
                            'values': [[args['all_futures_profit_percent']]]
                        },
                        {
                            'range': self._SAMPLE_RANGE_NAME + '!{}19'.format(args['now_day']),
                            'majorDimension': 'COLUMNS',
                            'values': [[args['all_futures_commissions']]]
                        },
                        {
                            'range': self._SAMPLE_RANGE_NAME + '!{}20'.format(args['now_day']),
                            'majorDimension': 'COLUMNS',
                            'values': [[args['all_futures_equity']]]
                        },
                    ]
                }
            ).execute()
        except Exception as e:
            print('Error "GoogleSheetsForBinance.add_all_balance_for_all_accounts": Step 246 {}'.format(e))
# <------------------------------------------------------------------------------------------------------------------> #
class BinanceAppScript:
    '''
                    Binance script
        For daily collection of information | At 3:30 Moscow time
    '''
    def __init__(self):

        # For the field all accounts
        self.for_all_accounts = {
            'now_day': '', 'all_balance': 0, 'all_profit_sum': 0, 'all_profit_percent': 0, 'all_withdraw': 0,
            'all_deposits': 0, 'all_spot_balance': 0, 'all_spot_profit_sum': 0, 'all_spot_profit_percent': 0,
            'all_spot_commissions': 0, 'all_spot_equity': 0, 'all_futures_balance': 0, 'all_futures_profit_sum': 0,
            'all_futures_profit_percent': 0, 'all_futures_commissions': 0, 'all_futures_equity': 0
        }

        # startTime.
        self.start_event = int(dt.datetime.strptime(
            str(dt.date.fromordinal(dt.date.today().toordinal() - 1)) + ' 00:00:00.000000',
            '%Y-%m-%d %H:%M:%S.%f').timestamp() * 1000)
        # endTime
        self.end_event = int(dt.datetime.strptime(
            str(dt.date.fromordinal(dt.date.today().toordinal() - 1)) + ' 23:59:59.000000',
            '%Y-%m-%d %H:%M:%S.%f').timestamp() * 1000)

        self.loop = asyncio.new_event_loop()
        # self.loop = asyncio.get_event_loop()
        asyncio.set_event_loop(self.loop)
        self._queue = asyncio.Queue()
        self.loop.run_until_complete(self.run())

    async def _get_data(self, acc: dict) -> None:
        '''
            This method looks for information on the Api for the desired account

            :param acc: Account information, name, api, secret api
        '''
        try:
            # Connecting to AsyncClient
            client = await AsyncClient.create(api_key=acc['api_key'], api_secret=acc['secret_api_key'])
            print('Account: "{}"| Check started'.format(acc["name"]))
        except BinanceAPIException as e:
            print('Account: "{}" | Error: Step 370 {}'.format(acc["name"], e))
            await client.close_connection()
            return []
        except Exception as e:
            print('Account: "{}" | Error: Step 370'.format(acc["name"], e))
            await client.close_connection()
            return []
        # Если перестанет рабоать то верни values['title'] = acc['name']
        values = {'title': acc['name']}

        # Overall balance
        overall_balance = 0.0

        try:
            # Withdrawal amount
            values['withdraw']: float = await self._get_withdraw(client)
        except BinanceAPIException as e:
            print('------>Account: "{}" | Error "BinanceAppScript._get_withdraw": Step 388 {}'.format(values["title"], e))
            if e.status_code == 429 and e.code == -1003:
                await asyncio.sleep(70)
                values['withdraw']: float = await self._get_withdraw(client)
            else:
                values['withdraw'] = 0
        except Exception as e:
            print('------>Account: "{}" | Error "BinanceAppScript._get_withdraw": Step 388 {}'.format(values["title"], e))
            values['withdraw'] = 0

        try:
            # Deposit amount
            values['deposit']: float = await self._get_deposit(client)
        except BinanceAPIException as e:
            print('------>Account: "{}" | Error "BinanceAppScript._get_deposit": Step 402 {}'.format(values["title"], e))
            if e.status_code == 429 and e.code == -1003:
                await asyncio.sleep(70)
                values['deposit']: float = await self._get_deposit(client)
            else:
                values['deposit'] = 0
        except Exception as e:
            print('------>Account: "{}" | Error "BinanceAppScript._get_deposit": Step 402 {}'.format(values["title"], e))
            values['deposit'] = 0

        try:
            # SPOT Balance and SPOT Equity | BTC => USDT
            balance_equity_spot: tuple = await self._get_spot_balance_equity(client)
            values['balance_spot']: float = round(balance_equity_spot[0], 2)
            values['equity_spot']: float = round(balance_equity_spot[1], 2)
            # Add SPOT balance to the general account
            overall_balance += float(values['balance_spot'])
        except BinanceAPIException as e:
            print('------>Account: "{}" | Error "BinanceAppScript._get_spot_balance_equity": Step 416 {}'.format(values["title"], e))
            if e.status_code == 429 and e.code == -1003:
                await asyncio.sleep(70)
                balance_equity_spot: tuple = await self._get_spot_balance_equity(client)
                values['balance_spot']: float = round(balance_equity_spot[0], 2)
                values['equity_spot']: float = round(balance_equity_spot[1], 2)
                overall_balance += float(values['balance_spot'])
            else:
                values['equity_spot'], values['balance_spot'] = 0, 0
        except Exception as e:
            print('------>Account: "{}" | Error "BinanceAppScript._get_spot_balance_equity": Step 416 {}'.format(values["title"], e))
            values['equity_spot'], values['balance_spot'] = 0, 0

        # If the SPOT balance is more than 0, then we will check orders
        if float(values['balance_spot']) > 0:
            try:
                # SPOT account commission
                # values['commission_spot']: float = await self._get_spot_commissions(client)
                values['commission_spot']: float = 0
            except BinanceAPIException as e:
                print('------>Account: "{}" | Error "BinanceAppScript._get_spot_commissions": Step 439 {}'.format(values["title"], e))
                if e.status_code == 429 and e.code == -1003:
                    await asyncio.sleep(70)
                    values['commission_spot']: float = await self._get_spot_commissions(client)
                else:
                    values['commission_spot'] = 0
            except Exception as e:
                print('------>Account: "{}" | Error "BinanceAppScript._get_spot_commissions": Step 439 {}'.format(values["title"], e))
                values['commission_spot'] = 0
        else:
            values['commission_spot'] = 0

        # Checking for a FUTURES account
        try:
            # Balance FUTURES | USDS-M OR COIN-M => USDT
            balance_futures: tuple = await self._get_future_balance_equity(client)
            values['balance_future']: float = round(balance_futures[0], 2)
            values['equity_futures']: float = round(balance_futures[1], 2)
            # Add FUTURES balance to the general account
            overall_balance += float(values['balance_future'])
        except BinanceAPIException as e:
            print('------>Account: "{}" | Error "BinanceAppScript._get_future_balance_equity": Step 456 {}'.format(values["title"], e))
            if e.status_code == 429 and e.code == -1003:
                await asyncio.sleep(70)
                balance_futures: tuple = await self._get_future_balance_equity(client)
                values['balance_future']: float = round(balance_futures[0], 2)
                values['equity_futures']: float = round(balance_futures[1], 2)
                overall_balance += float(values['balance_future'])
            else:
                values['balance_future'], values['equity_futures'] = 0, 0
        except Exception:
            print('------>Account: "{}" | No futures account found'.format(values["title"]))
            values['balance_future'], values['equity_futures'] = 0, 0

        await asyncio.sleep(10)

        # If there is a FUTURES account
        if values['balance_future'] > 0:
            try:
                # values['commission_future']: float = await self._get_futures_commissions(client)
                values['commission_future']: float = 0
            except BinanceAPIException as e:
                print('------>Account: "{}" | Error "BinanceAppScript._get_futures_commissions": Step 480 {}'.format(values["title"], e))
                if e.status_code == 429 and e.code == -1003:
                    await asyncio.sleep(70)
                    values['commission_future']: float = await self._get_futures_commissions(client)
                else:
                    values['commission_future'] = 0
            except Exception as e:
                print('------>Account: "{}" | Error "BinanceAppScript._get_futures_commissions": Step 480 {}'.format(values["title"], e))
                values['commission_future'] = 0
        else:
            values['commission_future'] = 0

        try:
            # We check transfers from account to account
            transfer: tuple = await self._get_transfer(client)
            SPOT_to_FUTURES, FUTURES_to_SPOT = round(transfer[0], 2), round(transfer[1], 2)
        except BinanceAPIException as e:
            print('------>Account: "{}" | Error "BinanceAppScript._get_transfer": Step 496 {}'.format(values["title"], e))
            if e.status_code == 429 and e.code == -1003:
                await asyncio.sleep(70)
                transfer: tuple = await self._get_transfer(client)
                SPOT_to_FUTURES, FUTURES_to_SPOT = round(transfer[0], 2), round(transfer[1], 2)
            else:
                SPOT_to_FUTURES, FUTURES_to_SPOT = 0, 0
        except Exception as e:
            print('------>Account: "{}" | Error "BinanceAppScript._get_transfer": Step 496 {}'.format(values["title"], e))
            SPOT_to_FUTURES, FUTURES_to_SPOT = 0, 0

        # Adding general balance
        values['overall_balance']: float = overall_balance

        # Closing connections
        await client.close_connection()

        try:
            # Yesterday's balance
            yesterday_balance: dict = GoogleSheetsForBinance().get_yesterday_balance(values['title'])
        except Exception as e:
            print('------>Account: "{}" | Error "GoogleSheetsForBinance.get_yesterday_balance": Step 497 {}'.format(values["title"], e))
            yesterday_balance = {'SPOT': values['balance_spot'], 'FUTURES': values['balance_future'], 'BALANCE': values['overall_balance']}

        if yesterday_balance['SPOT']:
            profit_spot: float = values['balance_spot'] - values['deposit'] + values['withdraw'] - SPOT_to_FUTURES + FUTURES_to_SPOT
            # Profit on SPOT account USDT = (today's SPOT balance - deposit - withdrawal) - yesterday's SPOT balance
            values['profit_spot_usdt']: float = await self._get_profit_usdt(profit_spot, float(yesterday_balance['SPOT']))
            # Profit on SPOT account% = (today's SPOT balance - replenishment - withdrawal) / (yesterday's SPOT balance / 100) / 100
            values['profit_spot_percent']: float = await self._get_profit_percent(profit_spot, float(yesterday_balance['SPOT']))
        else:
            values['profit_spot_usdt'], values['profit_spot_percent'] = 0, 0

        # If there are FUTURES
        if yesterday_balance['FUTURES']:
            profit_futures: float = values['balance_future'] - FUTURES_to_SPOT + SPOT_to_FUTURES
            # Profit on FUTURES account USDT = today's FUTURES balance - yesterday's FUTURES balance
            values['profit_future_usdt']: float = await self._get_profit_usdt(profit_futures, float(yesterday_balance['FUTURES']))
            # Profit on FUTURES account USDT = today's FUTURES balance / (yesterday's FUTURES balance / 100) / 100
            values['profit_future_percent']: float = await self._get_profit_percent(profit_futures,  float(yesterday_balance['FUTURES']))
        else:
            values['profit_future_usdt'], values['profit_future_percent'] = 0, 0

        # Checking the profit on the total account
        if yesterday_balance['BALANCE']:
            profit_account: float = values['overall_balance'] + values['withdraw'] - values['deposit']
            # Profit on account USDT = (today's balance - replenishment - withdrawal) - yesterday's balance
            values['profit_account_usdt']: float = await self._get_profit_usdt(profit_account, float(yesterday_balance['BALANCE']))
            # Account profit% = (today's balance - replenishment - withdrawal) / (yesterday's balance / 100) / 100
            values['profit_account_percent']: float = await self._get_profit_percent(profit_account, float(yesterday_balance['BALANCE']))
        else:
            values['profit_account_usdt'], values['profit_account_percent'] = 0, 0

        self.for_all_accounts['all_balance'] += float(values['overall_balance'])
        self.for_all_accounts['all_profit_sum'] += float(values['profit_account_usdt'])
        self.for_all_accounts['all_profit_percent'] += float(values['profit_account_percent'])
        self.for_all_accounts['all_withdraw'] += float(values['withdraw'])
        self.for_all_accounts['all_deposits'] += float(values['deposit'])
        self.for_all_accounts['all_spot_balance'] += float(values['balance_spot'])
        self.for_all_accounts['all_spot_profit_sum'] += float(values['profit_spot_usdt'])
        self.for_all_accounts['all_spot_profit_percent'] += float(values['profit_spot_percent'])
        self.for_all_accounts['all_spot_commissions'] += float(values['commission_spot'])
        self.for_all_accounts['all_spot_equity'] += float(values['equity_spot'])
        self.for_all_accounts['all_futures_balance'] += float(values['balance_future'])
        self.for_all_accounts['all_futures_profit_sum'] += float(values['profit_future_usdt'])
        self.for_all_accounts['all_futures_profit_percent'] += float(values['profit_future_percent'])
        self.for_all_accounts['all_futures_commissions'] += float(values['commission_future'])
        self.for_all_accounts['all_futures_equity'] += float(values['equity_futures'])

        try:
            # Write an invoice in Google Sheets
            self.for_all_accounts['now_day']: str = GoogleSheetsForBinance().add_data(values)
        except Exception as e:
            print('------>Account: "{}" was not recorded | Error "GoogleSheetsForBinance.add_data": Step 569 {}'.format(values["title"], e))

    async def _get_withdraw(self, client: AsyncClient) -> float:
        ''' Receive withdrawal amount | COIN => USDT '''
        sum_withdraw = 0.0
        total_withdraws: dict = await client.get_withdraw_history(startTime=self.start_event, endTime=self.end_event)

        for withdraw in total_withdraws:
            if withdraw['coin'] == 'USDT':
                sum_withdraw += float(withdraw['amount'])
            else:
                try:
                    coin_price: dict = await client.get_symbol_ticker(symbol=f'{withdraw["coin"]}USDT')
                    sum_withdraw += float(withdraw['amount']) * float(coin_price['price'])
                except BinanceAPIException as e:
                    if e.status_code == 429 and e.code == -1003:
                        await asyncio.sleep(70)
                        coin_price: dict = await client.get_symbol_ticker(symbol=f'{withdraw["coin"]}USDT')
                        sum_withdraw += float(withdraw['amount']) * float(coin_price['price'])
                    else:
                        continue
                except Exception:
                    continue

        return sum_withdraw

    async def _get_deposit(self, client: AsyncClient) -> float:
        ''' Get the amount of the deposit | COIN => USDT'''
        sum_deposit = 0.0
        total_deposit: dict = await client.get_deposit_history(startTime=self.start_event, endTime=self.end_event)

        for deposit in total_deposit:
            if deposit['coin'] == 'USDT':
                sum_deposit += float(deposit['amount'])
            else:
                try:
                    coin_price: dict = await client.get_symbol_ticker(symbol=f'{deposit["coin"]}USDT')
                    sum_deposit += float(deposit['amount']) * float(coin_price['price'])
                except BinanceAPIException as e:
                    if e.status_code == 429 and e.code == -1003:
                        await asyncio.sleep(70)
                        coin_price: dict = await client.get_symbol_ticker(symbol=f'{deposit["coin"]}USDT')
                        sum_deposit += float(deposit['amount']) * float(coin_price['price'])
                    else:
                        continue
                except Exception:
                    continue

        return sum_deposit

    async def _get_spot_balance_equity(self, client: AsyncClient) -> tuple:
        ''' Getting the balance and equity of the SPOT account | BTC => USDT '''
        balance = await client.get_account()
        info: dict = balance['balances']
        balanceAccounts = 0
        equity = 0

        for i in info:
            # If there is a free balance and a locked balance
            if float(i['locked']) > 0 or float(i['free']) > 0:
                assetLocked = float(i['locked'])
                assetFree = float(i['free'])

                if i['asset'] == 'USDT':
                    equity += assetFree
                    balanceAccounts += assetFree + assetLocked
                    continue
                try:
                    # We transfer from COIN => USDT
                    priceUSDT: dict = await client.get_symbol_ticker(symbol=f'{i["asset"]}USDT')
                    priceUSDT = float(priceUSDT['price'])

                    assetLocked *= priceUSDT
                    assetFree *= priceUSDT

                    equity += assetFree
                    balanceAccounts += assetFree + assetLocked
                except Exception:
                    # If it does not work then from COIN => BTC => USDT
                    try:
                        priceBTC: dict = await client.get_symbol_ticker(symbol=f'{i["asset"]}BTC')
                        priceBTC = float(priceBTC['price'])

                        assetBTCLocked = assetLocked * priceBTC
                        assetBTCFree = assetFree * priceBTC

                        priceUSDT: dict = await client.get_symbol_ticker(symbol='BTCUSDT')
                        priceUSDT = float(priceUSDT['price'])

                        assetBTCLocked *= priceUSDT
                        assetBTCFree *= priceUSDT

                        equity += assetBTCFree
                        balanceAccounts += assetBTCFree + assetBTCLocked
                    except Exception:
                        continue

        return balanceAccounts, equity

    async def _get_spot_commissions(self, client: AsyncClient) -> float:
        ''' Get SPOT commission today | COIN => USDT '''
        commission = 0
        tickers: dict = await client.get_all_tickers()

        for i in tickers:
            try:
                trade: dict = await client.get_my_trades(
                    symbol=i['symbol'], startTime=self.start_event, endTime=self.end_event)
            except BinanceAPIException as e:
                if e.status_code == 429 and e.code == -1003:
                    await asyncio.sleep(70)
                    trade: dict = await client.get_my_trades(
                        symbol=i['symbol'], startTime=self.start_event, endTime=self.end_event)
                else:
                    continue
            except Exception:
                await asyncio.sleep(7)
                continue
            if trade:
                for trd in trade:
                    if trd["commissionAsset"] == 'USDT': commission += float(trd["commission"])
                    else:
                        try:
                            coin_price: dict = await client.get_symbol_ticker(symbol=f'{trd["commissionAsset"]}USDT')
                            commission += float(trd["commission"]) * float(coin_price['price'])
                        except BinanceAPIException as e:
                            if e.status_code == 429 and e.code == -1003:
                                await asyncio.sleep(70)
                                coin_price: dict = await client.get_symbol_ticker(symbol=f'{trd["commissionAsset"]}USDT')
                                commission += float(trd["commission"]) * float(coin_price['price'])
                            else:
                                continue
                        except Exception:
                            await asyncio.sleep(7)
                            continue
        return commission

    async def _get_future_balance_equity(self, client: AsyncClient) -> tuple:
        ''' Get FUTURES account balance | USDS-M AND COIN-M => USDT '''
        balance = 0.0
        equity = 0.0

        # Checking USD-M Futures
        futures_usd_m: dict = await client.futures_account()
        balance += float(futures_usd_m['totalWalletBalance'])
        equity += float(futures_usd_m['totalMarginBalance'])

        # Checking COIN-M Futures
        futures_coin_m: dict = await client.futures_coin_account()
        for coin in futures_coin_m['assets']:
            if float(coin['walletBalance']) > 0:
                try:
                    price: dict = await client.get_symbol_ticker(symbol=f'{coin["asset"]}USDT')
                    balance += float(coin['walletBalance']) * float(price['price'])
                except BinanceAPIException as e:
                    if e.status_code == 429 and e.code == -1003:
                        await asyncio.sleep(70)
                        price: dict = await client.get_symbol_ticker(symbol=f'{coin["asset"]}USDT')
                        balance += float(coin['walletBalance']) * float(price['price'])
                    else:
                        continue
                except Exception:
                    continue
            if float(coin['marginBalance']) > 0:
                try:
                    price: dict = await client.get_symbol_ticker(symbol=f'{coin["asset"]}USDT')
                    equity += float(coin['marginBalance']) * float(price['price'])
                except BinanceAPIException as e:
                    if e.status_code == 429 and e.code == -1003:
                        await asyncio.sleep(70)
                        price: dict = await client.get_symbol_ticker(symbol=f'{coin["asset"]}USDT')
                        equity += float(coin['marginBalance']) * float(price['price'])
                    else:
                        continue
                except Exception:
                    continue
        return balance, equity

    async def _get_futures_commissions(self, client) -> float:
        ''' Get commission on FUTURES account | COIN => USDT '''
        commission = 0
        tickers: dict = await client.futures_coin_symbol_ticker()

        for ticker in tickers:
            try:
                orders: dict = await client.futures_coin_account_trades(
                    symbol=ticker['symbol'],
                    startTime=self.start_event,
                    endTime=self.end_event)
            except BinanceAPIException as e:
                if e.status_code == 429 and e.code == -1003:
                    await asyncio.sleep(70)
                    orders: dict = await client.futures_coin_account_trades(
                        symbol=ticker['symbol'], startTime=self.start_event, endTime=self.end_event)
                else:
                    continue
            except Exception:
                continue
            if orders:
                for order in orders:
                    if order['commissionAsset'] == 'USDT': commission += float(order['commission'])
                    else:
                        try:
                            coin_price: dict = await client.get_symbol_ticker(symbol=f"{order['commissionAsset']}USDT")
                            commission += float(coin_price['price']) * float(order['commission'])
                        except BinanceAPIException as e:
                            if e.status_code == 429 and e.code == -1003:
                                await asyncio.sleep(70)
                                coin_price: dict = await client.get_symbol_ticker(symbol=f"{order['commissionAsset']}USDT")
                                commission += float(coin_price['price']) * float(order['commission'])
                            else:
                                continue
                        except Exception:
                            continue
        return commission

    async def _get_transfer(self, client: AsyncClient) -> tuple:
        ''' This method shows transfers from account to account '''
        from_spot_to_futures, from_futures_to_spot = 0, 0
        coins: dict = await client.get_all_coins_info()

        for coin in coins:
            try:
                transfer: dict = await client.transfer_history(
                    asset=coin['coin'], startTime=self.start_event, endTime=self.end_event)
            except BinanceAPIException as e:
                if e.status_code == 429 and e.code == -1003:
                    await asyncio.sleep(70)
                    transfer: dict = await client.transfer_history(
                        asset=coin['coin'], startTime=self.start_event, endTime=self.end_event)
                else:
                    continue
            except Exception:
                continue
            if transfer['total'] > 0:
                if 'rows' in transfer:
                    for rows in transfer['rows']:
                        if rows['status'] == 'CONFIRMED':
                            if int(rows['type']) == 1 or int(rows['type']) == 3:
                                # From Spot to Futures
                                if rows['asset'] == 'USDT': from_spot_to_futures += float(rows['amount'])
                                else:
                                    try:
                                        price: dict = await client.get_symbol_ticker(symbol=f'{rows["asset"]}USDT')
                                        from_spot_to_futures += float(rows['amount']) * float(price['price'])
                                    except BinanceAPIException as e:
                                        if e.status_code == 429 and e.code == -1003:
                                            await asyncio.sleep(70)
                                            price: dict = await client.get_symbol_ticker(symbol=f'{rows["asset"]}USDT')
                                            from_spot_to_futures += float(rows['amount']) * float(price['price'])
                                        else:
                                            continue
                                    except Exception:
                                        continue
                            elif int(rows['type']) == 2 or int(rows['type']) == 4:
                                # From Futures to Spot
                                if rows['asset'] == 'USDT': from_futures_to_spot += float(rows['amount'])
                                else:
                                    try:
                                        price: dict = await client.get_symbol_ticker(symbol=f'{rows["asset"]}USDT')
                                        from_futures_to_spot += float(rows['amount']) * float(price['price'])
                                    except BinanceAPIException as e:
                                        if e.status_code == 429 and e.code == -1003:
                                            await asyncio.sleep(70)
                                            price: dict = await client.get_symbol_ticker(symbol=f'{rows["asset"]}USDT')
                                            from_futures_to_spot += float(rows['amount']) * float(price['price'])
                                        else:
                                            continue
                                    except Exception:
                                        continue
        return from_spot_to_futures, from_futures_to_spot

    async def _get_profit_usdt(self, today: float, yesterday: float) -> float:
        ''' Get profit on the account $ '''
        return today - yesterday

    async def _get_profit_percent(self, today: float, yesterday: float) -> float:
        ''' Get a profit on the account% '''
        return today / (yesterday / 100) - 100

    async def run(self):
        '''  Startup of the screen | Calling from outside is not possible '''
        accounts: dict = DB().select_data()
        task_list = []
        # If the data is in the database
        if accounts:
            print('The script is running!\nGetting started: {}\n'.format(str(datetime.now()).split(".")[0]))
            start = time()

            for acc in accounts:
                if acc['status']:
                    task = asyncio.create_task(self._get_data(acc))
                    task_list.append(task)

            await self._queue.join()
            await asyncio.gather(*task_list, return_exceptions=True)

            try:
                print("Let's write in the field 'All accounts'")
                GoogleSheetsForBinance().add_all_balance_for_all_accounts(self.for_all_accounts)
            except Exception as e:
                print('------>Error "GoogleSheetsForBinance.add_all_balance_for_all_accounts": Step 873 {}'.format(e))

            end = time() - start
            end = str(dt.timedelta(seconds=int(end)))
            print('\n{}\nAll accounts have been verified and added to GoogleSheets!\nTime taken: {} sec'.format(
                str(datetime.now()).split(".")[0], end))
# <------------------------------------------------------------------------------------------------------------------> #
def start():
    '''
            BinanceAppScript script
            Receives data from the database, and via API / SECRET-API receives
            access to the user's account, then collects the necessary data and
            sends to GoogleSheetsApp to enter data into Google Sheets

            For the script to start working, you need to synchronize the time

            Windows Settings -> Time & Language -> Date & Time -> Synchronize
    '''
    BinanceAppScript()
# <------------------------------------------------------------------------------------------------------------------> #
if __name__ == '__main__':
    start()