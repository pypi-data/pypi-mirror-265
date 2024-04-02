import os
import sys
import pandas as pd
from pathlib import Path
from staticObject import COLUMN_LABELS, NUMERIC_OBJECTS, STRING_OBJECTS
from budget import GroupID, Stamp


class SADDetail:
    """
    - This class is created an object based on pandas library and excel file in .xlsx format from https://stats-admin.customs.gov.kh/
    - You can calculate total amount of value in each column label from the object.
    """

    def __init__(self, file_path: str):
        assert (
            Path(file_path).suffix.lower() == ".xlsx"
        ), f"Invalid file extension: {Path(file_path).suffix}"
        self.df = pd.read_excel(
            file_path, dtype={COLUMN_LABELS[key]: str for key in STRING_OBJECTS}
        )

        self._convert_to_datetime()

    # @classmethod
    def _convert_to_datetime(self):
        """
        Converts specific columns in the DataFrame to datetime format.
        The columns are converted using the format "%Y-%m-%d".
        """
        date_columns = [COLUMN_LABELS["reg_date"], COLUMN_LABELS["receipt_date"]]
        for col in date_columns:
            self.df[col] = pd.to_datetime(self.df[col], format="%Y-%m-%d")

    def get_value_by_serial(self, value_code: str, serial: str):
        """
        - value_code: Column label selected for performing calculation.
        - serial: Registration Serial
        - Return:
            int: Total Amount in column selected by value_code.
        """
        return self.df[self.df[COLUMN_LABELS["reg_serial"]] == serial.upper()][
            COLUMN_LABELS[value_code.lower()]
        ].sum()

    def get_value_SI(self, value_code):
        """
        Arg:
        - value_code (str) : Numeric Column Label
        Return:
        - numpy.float64 : Total amount of numeric column labels where Registration Serial are SI.
        """
        filter_df = self.df[self.df[COLUMN_LABELS["reg_serial"]] == "SI"][
            COLUMN_LABELS[value_code.lower()]
        ]
        return filter_df.sum()

    def get_min_serial(self, serial_key: str):
        """
        Returns the minimum registration number for a given serial type.
        Args:
            serial (str): The serial type (I, SI, D, E, or SE).
        Raises:
            AssertionError: If the provided serial type is invalid.
        Returns:
            str: The minimum registration number for the specified serial type.
        """
        valid_serial = ("I", "SI", "D", "E", "SI")
        assert serial_key.upper() in valid_serial, f"Invalid serial type: {serial_key}"
        return self.df[self.df["Reg. Serial"] == serial_key]["Reg. Number"].min()

    def get_max_serial(self, serial_key: str):
        """
        Returns the maximum registration number for a given serial type.
        Args:
            serial (str): The serial type (I, SI, D, E, or SE).
        Raises:
            AssertionError: If the provided serial type is invalid.
        Returns:
            str: The maximum registration number for the specified serial type.
        """
        valid_serial = ("I", "SI", "D", "E", "SI")
        assert serial_key.upper() in valid_serial, f"Invalid serial type: {serial_key}"

        return self.df[self.df["Reg. Serial"] == serial_key.upper()][
            "Reg. Number"
        ].max()

    def tax_amount_in_receipt(self, tax_code: str, serial: dict):
        """
        This function is used for calculating Amount of Tax only, not for calculating Non-Tax values.
        Args:
         - tax_code (str): tax_code available in Balance Report.
         - serial (dict): List of string ['E', 'I', 'SI', 'D']
        Return:
         - float: Total amount of tax (specified by tax_code)
        """
        try:
            _tax_mop = COLUMN_LABELS[f"{tax_code.lower()}_mop"]
            _tax_amount = COLUMN_LABELS[f"{tax_code.lower()}"]
            _serial = COLUMN_LABELS["reg_serial"]
        except:
            # raise KeyError(f"Column {tax_code} is not for Accounting Purpose.")
            valid_tax_code = [
                key
                for key in COLUMN_LABELS.keys()
                if COLUMN_LABELS[key].endswith("Amount")
            ]
            assert (
                tax_code in valid_tax_code
            ), f"Invalid tax_code: {tax_code}. tax_code should be in {valid_tax_code}"
        # Add tax amount where its MOP=1.
        filter_df = self.df[self.df[_tax_mop] == 1 & self.df[_serial].isin(serial)]
        return filter_df[_tax_amount].sum()

    def bur_tax_amount(self, tax_code: str, serial: dict):
        try:
            _tax_mop = COLUMN_LABELS[f"{tax_code.lower()}_mop"]
            _tax_amount = COLUMN_LABELS[f"{tax_code.lower()}"]
            _serial = COLUMN_LABELS["reg_serial"]
        except:
            # raise KeyError(f"Column {tax_code} is not for Accounting Purpose.")
            valid_tax_code = [
                key
                for key in COLUMN_LABELS.keys()
                if COLUMN_LABELS[key].endswith("Amount")
            ]
            assert (
                tax_code in valid_tax_code
            ), f"Invalid tax_code: {tax_code}. tax_code should be in {valid_tax_code}"

        filter_df = self.df[self.df[_tax_mop] != 1 & self.df[_serial].isin(serial)]
        return filter_df[_tax_amount].sum()

    def other_bur_tax_amount(self):
        filter_df = self.df[
            self.df[COLUMN_LABELS["national_procedure"]].isin(["007", "032", "033"])
        ]
        return filter_df[COLUMN_LABELS["bur"]].sum()

    def value_by_group_id(self, value_code: str, group_id: int, transaction: str):
        """
        Args:
         - value_code (str): Column name where we want to calculate
         - group_id (int): For import, rangge from 1-52 and export, range from 1-29.
         - transaction (dict): Valid transaction are 'I' (1 - 52) and 'E' (1 - 29)
        Raises:
         - KeyError: If value_code is not a numeric column.
         - KeyError: If trasaction key is not I or E.
        Return:
         - float: Total value in column for GroupType (Import or Export) that specified by value_code.
        """
        if value_code not in NUMERIC_OBJECTS:
            raise KeyError(
                f"Invalid conlumn: {value_code}. Valid value_code: {[item for item in NUMERIC_OBJECTS]}"
            )
        # # Not used
        # tax_MOP_cols = [COLUMN_LABELS['cop_mop'], COLUMN_LABELS['cpp_mop'], COLUMN_LABELS['atp_mop'], COLUMN_LABELS['spp_mop'], COLUMN_LABELS['sop_mop'], COLUMN_LABELS['vop_mop'], COLUMN_LABELS['vpp_mop']]
        added_group_id_df = GroupID()
        df = added_group_id_df.add_group_id_to_df(self.df)

        transaction_map = {
            "IM": ["I", "SI", "D"],
            "EX": ["E", "SE"],
        }
        if transaction.upper() not in transaction_map.keys():
            raise KeyError(
                f"Invalid transaction key: {transaction}. Two valid transaction keys: IM, EX (Any uppercase or lowercase)"
            )

        filter_df = df[
            df[f"{transaction.upper()}_group_id"].isin([int(group_id)])
            & df[COLUMN_LABELS["reg_serial"]].isin(transaction_map[transaction.upper()])
            & (
                df[COLUMN_LABELS["national_procedure"]].isin(["", " ", "000"])
                | df[COLUMN_LABELS["national_procedure"]].isnull()
            )
        ]

        return filter_df[COLUMN_LABELS[value_code.lower()]].sum()

    def stamp_used(self):
        """
        Args:
         -
        Return:
         - Total number of stamp used.
        """
        stamp_list = Stamp()
        stamp_df = stamp_list.get_dataframe()
        available_stamp = stamp_list.available_stamp()

        self.df = self.df.merge(
            stamp_df, how="left", left_on=COLUMN_LABELS["hs_code"], right_on="hs_code"
        )
        stamp_used_kind = [
            kind for kind in self.df["stamp_kind"].unique() if pd.notna(kind)
        ]
        filter_for_stamp = self.df[self.df["stamp_kind"].isin(stamp_used_kind)]

        return filter_for_stamp[COLUMN_LABELS["package"]].sum()



script_dir = os.path.dirname(__file__)
input_files = os.path.join(script_dir, 'inputFiles')
path_to_SAD_Detail = os.path.join(input_files, "SAD_Detail.xlsx")
data = SADDetail(path_to_SAD_Detail)
dara = data.value_by_group_id(value_code="khr_value", group_id=52, transaction="im")

"""
Continue here to find out SAD_Detail.xlsx file directory
"""