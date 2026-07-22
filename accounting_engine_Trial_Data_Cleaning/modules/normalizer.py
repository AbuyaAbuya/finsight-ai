"""
normalizer.py
-------------
Normalizes synthetic ledger journals into balanced double-entry journals.

Workflow
--------
1. Assign natural debit/credit direction using the Chart of Accounts.
2. Calculate journal totals.
3. If balanced -> keep.
4. Else search for the minimum number of sign flips.
5. If still not balanced -> insert ONE balancing line.
"""

from itertools import combinations
import pandas as pd


class LedgerNormalizer:

    def __init__(self, gl_df: pd.DataFrame, coa_df: pd.DataFrame):

        self.gl = gl_df.copy()
        self.coa = coa_df.copy()

        self._prepare_coa()

    # ---------------------------------------------------------
    # COA
    # ---------------------------------------------------------

    def _prepare_coa(self):

        lookup = self.coa[
            [
                "Account_key",
                "Account_Name",
                "Account_Type",
                "Normal_Balance",
            ]
        ].copy()

        self.gl = self.gl.merge(
            lookup,
            on="Account_key",
            how="left"
        )

    # ---------------------------------------------------------
    # INITIAL POSTING
    # ---------------------------------------------------------

    def _assign_posting(self, row):

        amount = abs(row["Amount"])

        debit = 0.0
        credit = 0.0

        nb = row["Normal_Balance"]

        if nb == "Debit":

            if row["Amount"] >= 0:
                debit = amount
            else:
                credit = amount

        else:

            if row["Amount"] >= 0:
                credit = amount
            else:
                debit = amount

        return pd.Series([debit, credit])

    # ---------------------------------------------------------
    # BALANCE
    # ---------------------------------------------------------

    @staticmethod
    def journal_difference(df):

        return round(df["Debit"].sum() - df["Credit"].sum(), 2)

    # ---------------------------------------------------------
    # FLIP ROWS
    # ---------------------------------------------------------

    @staticmethod
    def flip(df, rows):

        df = df.copy()

        for idx in rows:

            d = df.at[idx, "Debit"]
            c = df.at[idx, "Credit"]

            df.at[idx, "Debit"] = c
            df.at[idx, "Credit"] = d

        return df

    # ---------------------------------------------------------
    # OPTIMIZER
    # ---------------------------------------------------------

    def optimize_journal(self, journal):

        journal = journal.copy()

        journal[["Debit", "Credit"]] = journal.apply(
            self._assign_posting,
            axis=1
        )

        if self.journal_difference(journal) == 0:

            journal["AI_Action"] = "None"

            return journal

        idx = list(journal.index)

        # search minimum flips

        for flips in range(1, len(idx) + 1):

            for combo in combinations(idx, flips):

                test = self.flip(journal, combo)

                if self.journal_difference(test) == 0:

                    test["AI_Action"] = f"Flip {flips} row(s)"

                    return test

        # -------------------------------------------------
        # LAST RESORT
        # -------------------------------------------------

        diff = self.journal_difference(journal)

        balancing = journal.iloc[0].copy()

        balancing["Account_key"] = 9998
        balancing["Account_Name"] = "AI Balancing Adjustment"
        balancing["Details"] = "Generated balancing entry"

        balancing["Amount"] = 0

        if diff > 0:

            balancing["Debit"] = 0
            balancing["Credit"] = diff

        else:

            balancing["Debit"] = abs(diff)
            balancing["Credit"] = 0

        balancing["AI_Action"] = "Generated Balancing Entry"

        journal = pd.concat(
            [journal, balancing.to_frame().T],
            ignore_index=True
        )

        return journal

    # ---------------------------------------------------------
    # RUN
    # ---------------------------------------------------------

    def normalize(self):

        journals = []

        for _, journal in self.gl.groupby("EntryNo", sort=False):

            journals.append(
                self.optimize_journal(journal)
            )

        normalized = pd.concat(
            journals,
            ignore_index=True
        )

        return normalized