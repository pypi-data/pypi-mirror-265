import os
import pandas as pd
import datetime
from staticObject import COLUMN_LABELS, STRING_OBJECTS, NUMERIC_OBJECTS

script_dir = os.path.dirname(__file__)

assert 'static' in os.listdir(script_dir), f'No static folder in path: {script_dir}'
static_dir = os.path.join(script_dir, 'static')

assert 'excel' in os.listdir(static_dir), f'No excel folder in path: {static_dir}'
excel_dir = os.path.join(static_dir, 'excel')

static_group_header_csv_file = os.path.join(excel_dir, 'staticGroup_header.csv')
static_stamp_csv_file = os.path.join(excel_dir, 'stamp_by_hs_code.csv')

class BudgetAccount:
    """
    - This class is created an object based on pandas library and excel file downloaded from https://stats-admin.customs.gov.kh/
        So, in order to make this class work properly, pandas library have to be installed.
    - file_path: is path to xlsx file.
    """

    def __init__(self, file_path: str):
        self.df = pd.read_excel(file_path)
        self.df["Receipt Date"] = pd.to_datetime(
            self.df["Receipt Date"], format="%Y-%m-%d"
        )

        self.column_label = self.df.columns.to_list()

    def get_total_amount(self, income_code: str):
        """
        Args:
            - income_code (str): income code in GDCE Report Balance or other report patterns.
        Return:
            - int: total amount of specified income.
        """
        return self.df[self.df["Budget Code"] == income_code.upper()]["Amount"].sum()

    def get_total_amount_by_source(self, income_code: str, source: str):
        """
        Args:
            - income_code (str): income code in GDCE Report Balance or other report patterns.
            - sources: ASYCUDA (ASW) ans E-Customs (ECS).
        Return:
            - Return: Total amount of income in each source.
        """
        assert source.upper() in [
            "ASW",
            "ECS",
        ], "Invalid Source, Valid Source: ASW, ECS"

        source_dataframe = self.df["source"] == source.upper().strip()
        income_datafram = self.df["Budget Code"] == income_code.upper().strip()
        return self.df[source_dataframe & income_datafram]["Amount"].sum()

    def get_total_amount_by_date(
        self, income_code: str = None, date_: datetime.datetime = None
    ):
        return self.df[self.df["Budget Code"] == "VAP"]["Receipt Date"]


class GroupID:
    def __init__(self):
        self.__df = pd.read_csv(
            static_group_header_csv_file,
            usecols=[COLUMN_LABELS["hs_code"], "group_id", "transaction"],
            dtype={COLUMN_LABELS["hs_code"]: str},
        )
        self.__IM = self.__df[self.__df["transaction"] == "IM"]
        self.__EX = self.__df[self.__df["transaction"] == "EX"]

    def get_dataframe(self):
        return self.__df

    def add_group_id_to_df(self, raw_data: pd.DataFrame):
        """
        Use for generating Import and Export Statistic Report.
        Arg:
        - raw_data (pd.DataFrame): SAD Detail
        Return:
        - raw_data (pd.DataFrame): Original dataframe with extra two columns IM_group_id and EX_group_id.
        """
        raw_data = raw_data.merge(
            self.__IM, on=COLUMN_LABELS["hs_code"], how="left"
        ).rename(columns={"group_id": "IM_group_id"})
        raw_data = raw_data.merge(
            self.__EX, on=COLUMN_LABELS["hs_code"], how="left"
        ).rename(columns={"group_id": "EX_group_id"})
        raw_data["IM_group_id"] = raw_data["IM_group_id"].fillna(52)
        raw_data["EX_group_id"] = raw_data["EX_group_id"].fillna(29)
        raw_data.drop(
            ["transaction_x", "transaction_y"], axis=1, inplace=True
        )  # suffix is used for distinguish between columns from each dataframe.
        return raw_data


class Stamp:
    def __init__(self):
        self._df = pd.read_csv(
            static_stamp_csv_file, usecols=[0, 1], dtype={"hs_code": str}
        )

    def get_dataframe(self):
        return self._df

    def available_stamp(self):
        return [stamp for stamp in self._df["stamp_kind"].unique() if pd.notna(stamp)]
    


    