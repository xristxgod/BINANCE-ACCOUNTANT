# <------------------------------------------------------------------------------------------------------------------> #
import os.path
import datetime

from googleapiclient.discovery import build
from google.oauth2 import service_account
from calendar import monthrange

from dotenv import load_dotenv
# <------------------------------------------------------------------------------------------------------------------> #
load_dotenv()
# <------------------------------------------------------------------------------------------------------------------> #
class GoogleSheetsApp:
    ''' Google Sheets interaction class '''

    MONTH = {
        1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь',
        7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
    }
    YEAR = str(datetime.datetime.now().year) + '-' + str(datetime.datetime.now().year + 1)

    def __init__(self):
        self._SAMPLE_SPREADSHEET_ID = os.getenv("SAMPLE_SPREADSHEET_ID")
        self._SAMPLE_RANGE_NAME = os.getenv('SAMPLE_RANGE_NAME')
        self._SHEET_ID = os.getenv('SHEET_ID')
        self._SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self._BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self._CREDENTIALS = service_account.Credentials.from_service_account_file(os.path.join(self._BASE_DIR,
                                                                                               'config/credentials.json'),
                                                                                  scopes=self._SCOPES)
        self._service = build('sheets', 'v4', credentials=self._CREDENTIALS).spreadsheets()

    def create_base_sheet(self) -> None:
        ''' Creates a basic template '''

        try:
            self._service.batchUpdate(
                spreadsheetId=self._SAMPLE_SPREADSHEET_ID,
                body={
                    'requests': [
                        {
                            'updateBorders': {
                                "range": {
                                    "sheetId": self._SHEET_ID,
                                    "startRowIndex": 0,
                                    "endRowIndex": 5,
                                    "startColumnIndex": 0,
                                    "endColumnIndex": 3
                                },
                                "top": {
                                    "style": "SOLID",
                                    "color": {
                                        "red": 200,
                                        "green": 200,
                                        "blue": 200
                                    },
                                },

                                # Нижняя граница
                                "bottom": {
                                    "style": "SOLID",
                                    "color": {
                                        "red": 200,
                                        "green": 200,
                                        "blue": 200
                                    },
                                },
                                # Горизонтальная граница
                                "innerHorizontal": {
                                    "style": "SOLID",
                                    "color": {
                                        "red": 200,
                                        "green": 200,
                                        "blue": 200
                                    },
                                },
                                # Вертикальная граница
                                'innerVertical': {
                                    "style": "SOLID",
                                    "color": {
                                        "red": 200,
                                        "green": 200,
                                        "blue": 200
                                    },
                                }
                            }
                        },
                        {
                            "updateSpreadsheetProperties": {
                                "properties": {"title": f"{self.YEAR}.{self.MONTH[datetime.datetime.now().month]}"},
                                "fields": "title"
                            }
                        },
                        {
                            'updateBorders': {
                                "range": {
                                    "sheetId": self._SHEET_ID,
                                    "startRowIndex": 5,
                                    "endRowIndex": 22,
                                    "startColumnIndex": 0,
                                    "endColumnIndex": 3
                                },
                                "top": {
                                    "style": "SOLID",
                                    "color": {
                                        "red": 200,
                                        "green": 200,
                                        "blue": 200
                                    },
                                },
                                # Лево
                                "left": {
                                    "style": "SOLID",
                                    "color": {
                                        "red": 200,
                                        "green": 200,
                                        "blue": 200
                                    }
                                },
                                # Право
                                "right": {
                                    "style": "SOLID",
                                    "color": {
                                        "red": 200,
                                        "green": 200,
                                        "blue": 200
                                    }
                                },
                                # Нижняя граница
                                "bottom": {
                                    "style": "SOLID",
                                    "color": {
                                        "red": 200,
                                        "green": 200,
                                        "blue": 200
                                    },
                                },
                                # Горизонтальная граница
                                "innerHorizontal": {
                                    "style": "SOLID",
                                    "color": {
                                        "red": 200,
                                        "green": 200,
                                        "blue": 200
                                    },
                                },
                                # Вертикальная граница
                                'innerVertical': {
                                    "style": "SOLID",
                                    "color": {
                                        "red": 200,
                                        "green": 200,
                                        "blue": 200
                                    },
                                }
                            }
                        },
                        {
                            "mergeCells": {
                                "range": {
                                    "sheetId": self._SHEET_ID,
                                    "startRowIndex": 5,
                                    "endRowIndex": 22,
                                    "startColumnIndex": 0,
                                    "endColumnIndex": 2
                                },
                                "mergeType": "MERGE_COLUMNS"
                            },
                        },
                        {
                            'repeatCell': {
                                # Где она начинается и кончается
                                'range': {
                                    "sheetId": self._SHEET_ID,
                                    "startRowIndex": 5,
                                    "endRowIndex": 22,
                                    "endColumnIndex": 2
                                },
                                'cell': {
                                    "userEnteredFormat": {
                                        # Цвет колонки
                                        "backgroundColor": {
                                            "red": 20,
                                            "green": 20,
                                            "blue": 20
                                        },
                                        # Расположение по середине
                                        "horizontalAlignment": "CENTER",

                                    }
                                },
                                "fields": "userEnteredFormat(backgroundColor, horizontalAlignment)"
                            },
                        },
                        {
                            'repeatCell': {
                                'range': {
                                    "sheetId": self._SHEET_ID,
                                    "startRowIndex": 5,
                                    "endRowIndex": 22,
                                    "startColumnIndex": 2,
                                    "endColumnIndex": 26
                                },
                                "cell": {
                                    "userEnteredFormat": {
                                        "textFormat": {
                                            "bold": True
                                        }
                                    }
                                },
                                "fields": "userEnteredFormat(textFormat)"
                            }
                        }
                    ]
                }
            ).execute()
        except Exception as e:
            print('Error "GoogleSheetsApp.create_base_sheet": Step 37  {}'.format())

        try:
            self._service.values().batchUpdate(
                spreadsheetId=self._SAMPLE_SPREADSHEET_ID,
                body={
                    'valueInputOption': 'RAW',
                    'data': [
                        {
                            'range': self._SAMPLE_RANGE_NAME + '!A5:B5',
                            'majorDimension': 'ROWS',
                            'values': [['№', 'Наименование счета']]
                        },
                        {
                            'range': self._SAMPLE_RANGE_NAME + '!A6:B6',
                            'majorDimension': 'ROWS',
                            'values': [['', 'Все счета']]
                        },
                        {
                            'range': self._SAMPLE_RANGE_NAME + '!C6',
                            'majorDimension': 'COLUMNS',
                            'values': [[
                                'Баланс всех счетов, $', 'Прибыль (- убыток) по всем счетам, $',
                                'Прибыль (- убыток) по всем счетам, %',
                                'Суммы снятия всех счетов', 'Суммы пополнения всех счетов',
                                'Баланс Спота всех счетов, $', 'Переводы со Спот на Фьючерсы по всем счетам',
                                'Прибыль по всем счетам, в $',
                                'Прибыль по всем счетам, в %', 'Комиссии по всем счетам',
                                'Эквити по всем счетам, $',
                                'Баланс Фьючерсов всех счетов, $', 'Переводы с Фьючерсов на Спот по всем счетам',
                                'Прибыль по всем счетам, в $', 'Прибыль по всем счетам, в %',
                                'Комиссии по всем счетам',
                                'Эквити по всем счетам, $'
                            ]]
                        }
                    ]
                }
            ).execute()
        except Exception as e:
            print('Error "GoogleSheetsApp.create_base_sheet": Step 222 {}'.format(e))

        requests, data, sheet = [], [], 2
        now_month = datetime.datetime.now().month
        for j in range(2):
            for i in range(now_month, 13):
                date = self.MONTH[i]
                days = monthrange(datetime.datetime.now().year + j, i)[1]

                if requests:
                    if i != 1:
                        sheet += monthrange(datetime.datetime.now().year + j, i - 1)[1] + 3
                    else:
                        sheet += monthrange(datetime.datetime.now().year + j, 12)[1] + 3
                sheet += 1

                d = GoogleSheetsApp().get_date(sheet + 1, sheet + days)
                z = GoogleSheetsApp().get_date(sheet + days + 1, sheet + days + 3)

                requests.append({
                    "insertDimension": {
                        "range": {
                            "sheetId": self._SHEET_ID,
                            "dimension": "COLUMNS",
                            "startIndex": sheet,
                            "endIndex": sheet + days + 4
                        },
                        "inheritFromBefore": True
                    }
                })
                requests.append({
                    'updateBorders': {
                        "range": {
                            "sheetId": self._SHEET_ID,
                            "startRowIndex": 0,
                            "endRowIndex": 5,
                            "startColumnIndex": sheet,
                            "endColumnIndex": sheet + days + 4
                        },
                        "top": {
                            "style": "SOLID",
                            "color": {
                                "red": 200,
                                "green": 200,
                                "blue": 200
                            },
                        },

                        # Нижняя граница
                        "bottom": {
                            "style": "SOLID",
                            "color": {
                                "red": 200,
                                "green": 200,
                                "blue": 200
                            },
                        },
                        # Горизонтальная граница
                        "innerHorizontal": {
                            "style": "SOLID",
                            "color": {
                                "red": 200,
                                "green": 200,
                                "blue": 200
                            },
                        },
                        # Вертикальная граница
                        'innerVertical': {
                            "style": "SOLID",
                            "color": {
                                "red": 200,
                                "green": 200,
                                "blue": 200
                            },
                        }
                    }
                })
                requests.append({
                    'repeatCell': {
                        # Где она начинается и кончается
                        'range': {
                            "sheetId": self._SHEET_ID,
                            "startRowIndex": 3,
                            "endRowIndex": 4,
                            "startColumnIndex": sheet,
                            "endColumnIndex": sheet + days + 1
                        },
                        'cell': {
                            "userEnteredFormat": {
                                # Цвет колонки
                                "backgroundColor": {
                                    "red": 20,
                                    "green": 20,
                                    "blue": 20
                                },
                                # Расположение по середине
                                "horizontalAlignment": "CENTER",

                            }
                        },
                        "fields": "userEnteredFormat(backgroundColor, horizontalAlignment)"
                    },
                })

                data.append({
                    # Дни
                    'range': self._SAMPLE_RANGE_NAME + f'!{d[0]}{4}:{d[1]}{days}',
                    'majorDimension': 'ROWS',
                    'values': [[i for i in range(1, days + 1)]]
                })
                data.append({
                    # Обозначение месяца
                    'range': self._SAMPLE_RANGE_NAME + f'!{d[0]}{2}:{d[0]}{3}',
                    'majorDimension': 'COLUMNS',
                    'values': [[f'Месяц: {date} | Год: {datetime.datetime.now().year + j}']]
                })
                data.append({
                    # Месяц, Год, За весь период
                    'range': self._SAMPLE_RANGE_NAME + f'!{z[0]}{2}:{z[1]}{2}',
                    'majorDimension': 'COLUMNS',
                    'values': [['Месяц:'], ['Год:'], ['За весь период:']]
                })
            now_month = 1

        try:
            self._service.batchUpdate(
                spreadsheetId=self._SAMPLE_SPREADSHEET_ID,
                body={
                    "requests": requests,
                }
            ).execute()
        except Exception as e:
            print('Error "GoogleSheetsApp.create_base_sheet": Step 379  {}'.format(e))

        try:
            self._service.values().batchUpdate(
                spreadsheetId=self._SAMPLE_SPREADSHEET_ID,
                body={
                    "valueInputOption": 'RAW',
                    'data': data
                }
            ).execute()
        except Exception as e:
            print('Error "GoogleSheetsApp.create_base_sheet": Step 389  {}'.format(e))

    def create_new_account(self, title: str) -> None:
        ''' Add a new account '''

        next_index = self.get_index()

        try:
            result = len(self._service.values().get(
                spreadsheetId=self._SAMPLE_SPREADSHEET_ID,
                range=self._SAMPLE_RANGE_NAME + '!C:C'
            ).execute().get('values', []))
        except Exception as e:
            print('Error "GoogleSheetsApp.create_new_account": Step 405 {}'.format())

        count = result if result > 0 else 5

        try:
            self._service.batchUpdate(
                spreadsheetId=self._SAMPLE_SPREADSHEET_ID,
                body={
                    'requests': [
                        {
                            'updateBorders': {
                                "range": {
                                    "sheetId": self._SHEET_ID,
                                    "startRowIndex": count,
                                    "endRowIndex": count + 17,
                                    "startColumnIndex": 0,
                                    "endColumnIndex": 3
                                },
                                "top": {
                                    "style": "SOLID",
                                    "color": {
                                        "red": 200,
                                        "green": 200,
                                        "blue": 200
                                    },
                                },
                                # Лево
                                "left": {
                                    "style": "SOLID",
                                    "color": {
                                        "red": 200,
                                        "green": 200,
                                        "blue": 200
                                    }
                                },
                                # Право
                                "right": {
                                    "style": "SOLID",
                                    "color": {
                                        "red": 200,
                                        "green": 200,
                                        "blue": 200
                                    }
                                },
                                # Нижняя граница
                                "bottom": {
                                    "style": "SOLID",
                                    "color": {
                                        "red": 200,
                                        "green": 200,
                                        "blue": 200
                                    },
                                },
                                # Горизонтальная граница
                                "innerHorizontal": {
                                    "style": "SOLID",
                                    "color": {
                                        "red": 200,
                                        "green": 200,
                                        "blue": 200
                                    },
                                },
                                # Вертикальная граница
                                'innerVertical': {
                                    "style": "SOLID",
                                    "color": {
                                        "red": 200,
                                        "green": 200,
                                        "blue": 200
                                    },
                                }
                            }
                        },
                        {
                            "mergeCells": {
                                "range": {
                                    "sheetId": self._SHEET_ID,
                                    "startRowIndex": count,
                                    "endRowIndex": count + 17,
                                    "startColumnIndex": 0,
                                    "endColumnIndex": 2
                                },
                                "mergeType": "MERGE_COLUMNS"
                            },

                        },
                        {
                            'repeatCell': {
                                # Где она начинается и кончается
                                'range': {
                                    "sheetId": self._SHEET_ID,
                                    "startRowIndex": count,
                                    "endRowIndex": count + 17,
                                    "endColumnIndex": 2
                                },
                                'cell': {
                                    "userEnteredFormat": {
                                        # Цвет колонки
                                        "backgroundColor": {
                                            "red": 20,
                                            "green": 20,
                                            "blue": 20
                                        },
                                        # Расположение по середине
                                        "horizontalAlignment": "CENTER",

                                    }
                                },
                                "fields": "userEnteredFormat(backgroundColor, horizontalAlignment)"
                            },
                        },
                        {
                            'repeatCell': {
                                'range': {
                                    "sheetId": self._SHEET_ID,
                                    "startRowIndex": count,
                                    "endRowIndex": count + 1,
                                    "startColumnIndex": 2,
                                    "endColumnIndex": 26
                                },
                                "cell": {
                                    "userEnteredFormat": {
                                        "textFormat": {
                                            "bold": True
                                        }
                                    }
                                },
                                "fields": "userEnteredFormat(textFormat)"
                            }
                        },
                        {
                            'repeatCell': {
                                'range': {
                                    "sheetId": self._SHEET_ID,
                                    "startRowIndex": count + 5,
                                    "endRowIndex": count + 6,
                                    "startColumnIndex": 2,
                                    "endColumnIndex": 26
                                },
                                "cell": {
                                    "userEnteredFormat": {
                                        "textFormat": {
                                            "bold": True
                                        }
                                    }
                                },
                                "fields": "userEnteredFormat(textFormat)"
                            }
                        },
                        {
                            'repeatCell': {
                                'range': {
                                    "sheetId": self._SHEET_ID,
                                    "startRowIndex": count + 11,
                                    "endRowIndex": count + 12,
                                    "startColumnIndex": 2,
                                    "endColumnIndex": 26
                                },
                                "cell": {
                                    "userEnteredFormat": {
                                        "textFormat": {
                                            "bold": True
                                        }
                                    }
                                },
                                "fields": "userEnteredFormat(textFormat)"
                            }
                        }
                    ]
                }
            ).execute()
        except Exception as e:
            print('Error "GoogleSheetsApp.create_new_account": Step 415 {}'.format())

        try:
            self._service.values().batchUpdate(
                spreadsheetId=self._SAMPLE_SPREADSHEET_ID,
                body={'valueInputOption': 'RAW',
                      'data': [{'range': self._SAMPLE_RANGE_NAME + '!C' + str(count + 1),
                                'majorDimension': 'COLUMNS',
                                'values': [[
                                    'Баланс счёта, $', 'Прибыль (- убыток) по общему счету, $',
                                    'Прибыль (- убыток) по общему счету, %', 'Суммы снятия', 'Суммы пополнения',
                                    'Баланс Спота, $', 'Перевод со Спота на Фьючерс', 'Прибыль по счёту, в $',
                                    'Прибыль по счёту, в %', 'Комиссии', 'Эквити, $', 'Баланс Фьючерсов, $',
                                    'Перевод с Фьючерсов на Спот', 'Прибыль по счёту, в $', 'Прибыль по счёту, в %',
                                    'Комиссии', 'Эквити, $'
                                ]]
                                },
                               {
                                   'range': self._SAMPLE_RANGE_NAME + '!A' + str(count + 1) + ':B' + str(count + 1),
                                   'majorDimension': 'ROWS',
                                   'values': [[next_index, title]]
                               }]}
            ).execute()
        except Exception as e:
            print('Error "GoogleSheetsApp.create_new_account": Step 585 {}'.format(e))

        self.generate_tables_for_account(numStart=count, numEnd=count + 17)

    def generate_tables_for_account(self, numStart: int = None, numEnd: int = None) -> None:
        ''' Generate table '''
        dt, dt_2 = '', ''
        now_month = datetime.datetime.now().month
        now_year = datetime.datetime.now().year

        requests = []
        from_mya = []

        last_range = ''

        for j in range(2):
            for i in range(now_month, 13):
                try:
                    values = self._service.values().get(
                        spreadsheetId=self._SAMPLE_SPREADSHEET_ID,
                        range=self._SAMPLE_RANGE_NAME + f'!A2:ZZ2',
                    ).execute().get('values', [])
                except Exception as e:
                    print('Error "GoogleSheetsApp.generate_tables_for_account": Step 622 {}'.format())

                count, flag = -1, False
                for val in values[0]:
                    count += 1
                    if val == 'Месяц: ' + self.MONTH[i] + ' | Год: ' + str(datetime.datetime.now().year + j):
                        break

                year = datetime.datetime.now().year + j

                days = monthrange(year, i)[1]

                range_ = GoogleSheetsApp().get_date(count + days, count + days + 2)
                yest = GoogleSheetsApp().get_date(count, count + days - 1)

                requests.append({
                    'updateBorders': {
                        "range": {
                            "sheetId": self._SHEET_ID,
                            "startRowIndex": numStart,
                            "endRowIndex": numEnd,
                            "startColumnIndex": count - 1,
                            "endColumnIndex": count - 1 + days + 4
                        },
                        "top": {
                            "style": "SOLID",
                            "color": {
                                "red": 200,
                                "green": 200,
                                "blue": 200
                            },
                        },
                        "bottom": {
                            "style": "SOLID",
                            "color": {
                                "red": 200,
                                "green": 200,
                                "blue": 200
                            },
                        },
                        "innerHorizontal": {
                            "style": "SOLID",
                            "color": {
                                "red": 200,
                                "green": 200,
                                "blue": 200
                            },
                        },
                        'innerVertical': {
                            "style": "SOLID",
                            "color": {
                                "red": 200,
                                "green": 200,
                                "blue": 200
                            },
                        }
                    }
                })
                requests.append({
                    'addBanding': {
                        "bandedRange": {
                            "range": {
                                "sheetId": self._SHEET_ID,
                                "startRowIndex": numStart,
                                "endRowIndex": numEnd,
                                "startColumnIndex": count - 1,
                                "endColumnIndex": count + days
                            },

                            "rowProperties": {

                                "secondBandColorStyle": {
                                    "themeColor": 'BACKGROUND'
                                },

                                "firstBandColorStyle": {
                                    "themeColor": 'ACCENT6'
                                }
                            }

                        }
                    }
                })

                data = []
                for v in range(numStart + 1, numEnd + 1):
                    m = f"=SUM({yest[0]}{v}:{yest[1]}{v})"
                    if count > 5:
                        if year != now_year and i == 1:
                            y = f"=SUM({yest[0]}{v}:{yest[1]}{v})"
                        else:
                            y = f"=SUM({yest[0]}{v}:{yest[1]}{v})"
                        a = f"=SUM({yest[0]}{v}:{yest[1]}{v})"
                    else:
                        y = f"=SUM({yest[0]}{v}:{yest[1]}{v})"
                        a = f"=SUM({yest[0]}{v}:{yest[1]}{v})"
                    d = [m, y, a]
                    data.append(d)

                dt = GoogleSheetsApp().get_date(count + days + 1, 1)[0]
                dt_2 = GoogleSheetsApp().get_date(count + days + 2, 1)[0]
                data[0], data[5], data[10], data[11], data[-1] = ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', '']

                from_mya.append({
                    'range': self._SAMPLE_RANGE_NAME + f'!{range_[0]}{numStart + 1}',
                    'majorDimension': 'ROWS',
                    'values': data
                })
                last_range = numStart + 1
            now_month = 1

        try:
            self._service.batchUpdate(
                spreadsheetId=self._SAMPLE_SPREADSHEET_ID,
                body={
                    'requests': requests
                }
            ).execute()
        except Exception as e:
            print('Error "GoogleSheetsApp.generate_tables_for_account": Step 739 {}'.format())

        try:
            self._service.values().batchUpdate(
                spreadsheetId=self._SAMPLE_SPREADSHEET_ID,
                body={
                    'valueInputOption': 'USER_ENTERED',
                    'data': from_mya
                }
            ).execute()
        except Exception as e:
            print('Error "GoogleSheetsApp.generate_tables_for_account": Step 749 {}'.format())

    def close_or_open_account(self, name: str, status: bool) -> None:
        ''' Close or open an account '''
        try:
            result = self._service.values().get(
                spreadsheetId=self._SAMPLE_SPREADSHEET_ID,
                range=self._SAMPLE_RANGE_NAME + '!B:B'
            ).execute().get('values', [])
        except Exception as e:
            print('Error "GoogleSheetsApp.close_or_open_account": Step 762 {}'.format())
            return

        count, flag = 0, False
        for res in result:
            if res:
                count += 1
                if count > 6:
                    count += 10
                if name in res:
                    flag = True
                    break

        close_date = str(datetime.datetime.now()).split(' ')[0]

        if status:
            # Если статус True то его открчть
            body = {"requests": {
                'findReplace': {
                    'find': f'{name}-Закрыт',
                    'replacement': f'{name.split("-Закрыт")[0]}',
                    "range": {
                        "sheetId": self._SHEET_ID,
                        "startRowIndex": 1,
                        "endRowIndex": 1000,
                        "startColumnIndex": 0,
                        "endColumnIndex": 4
                    }

                }
            }}

        else:
            # Если статус False то его закрыть
            body = {"requests": {
                'findReplace': {
                    'find': f'{name}',
                    'replacement': f'{name}-Закрыт {close_date}',
                    # 'replacement': f'{name}-Закрыт',
                    "range": {
                        "sheetId": self._SHEET_ID,
                        "startRowIndex": 1,
                        "endRowIndex": 1000,
                        "startColumnIndex": 0,
                        "endColumnIndex": 4
                    }
                }

            }}

        try:
            self._service.batchUpdate(
                spreadsheetId=self._SAMPLE_SPREADSHEET_ID,
                body=body
            ).execute()
        except Exception as e:
            print('Error "GoogleSheetsApp.close_or_open_account": Step 818 {}'.format())

    def get_index(self) -> int:
        ''' Get index '''

        # Get prev index
        prev_index = self._service.values().get(
            spreadsheetId=self._SAMPLE_SPREADSHEET_ID,
            range=self._SAMPLE_RANGE_NAME + '!B21:B1000'
        ).execute().get('values', [])

        return len([prev for prev in prev_index if prev]) + 1

    @staticmethod
    def get_date(start: int, end: int) -> tuple:

        ''' Получить нужный день '''

        abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lst, fin = [], []
        for i in abc:
            lst.append(i)
            for j in abc:
                fin.append(f'{i}{j}')
        lst += fin
        return lst[start], lst[end]
# <------------------------------------------------------------------------------------------------------------------> #
if __name__ == '__main__':
    GoogleSheetsApp().create_new_account('Title')
# <------------------------------------------------------------------------------------------------------------------> #