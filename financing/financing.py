import numpy as np
from scipy.optimize import root_scalar
from functools import cached_property


class MortgageCalculator:
    MONTHS_IN_A_YEAR = 12

    def __init__(
        self,
        total_amount: float,
        number_of_years: int,
        interest_rate: float,
        fees_every: int = 3,
        fees: float = 35.0,
    ):
        self.total_amount = total_amount
        self.number_of_years = number_of_years
        self.interest_rate = interest_rate
        self.fees_every = fees_every
        self.fees = fees
        self.monthly_rate = self.compute_monthly_rate()
        self.monthly_debt = np.empty(self.number_of_months + 1, dtype=float)
        self.monthly_interests = np.empty(self.number_of_months, dtype=float)
        self.monthly_debt[0] = self.total_amount
        for i in range(1, self.number_of_months + 1):
            self.monthly_debt[i] = self.balance_of_month(
                self.monthly_debt[i - 1], self.monthly_rate, i
            )
        debt_variation = np.diff(self.monthly_debt)
        self.monthly_interests = self.monthly_rate + debt_variation
        self.monthly_debt = self.monthly_debt[1:]

    @property
    def number_of_months(self) -> int:
        return self.number_of_years * self.MONTHS_IN_A_YEAR

    @cached_property
    def total_interest_lost(self) -> float:
        return self.monthly_rate * self.number_of_months - self.total_amount

    @cached_property
    def money_payed(self) -> np.ndarray:
        return self.monthly_rate * np.ones(self.number_of_months).cumsum()

    @cached_property
    def interest_payed(self) -> np.ndarray:
        return self.monthly_interests.cumsum()

    def balance_of_month(self, start_amount: float, monthly_rate: float, month_id: int):
        interest_to_pay = (
            start_amount * self.interest_rate * 1e-2 / self.MONTHS_IN_A_YEAR
        )
        left_amount = start_amount + interest_to_pay - monthly_rate
        if month_id % self.fees_every == 0:
            left_amount += self.fees
        return left_amount

    def compute_monthly_rate(self) -> float:
        def would_be_left(monthly_rate: float):
            left_amount = self.total_amount
            for i in range(self.number_of_months):
                left_amount = self.balance_of_month(left_amount, monthly_rate, i)
            return left_amount

        root_result = root_scalar(
            would_be_left,
            x0=(
                self.total_amount
                * (1 + self.interest_rate * 1e-2 * self.number_of_years)
            )
            / self.number_of_months,
            x1=(
                self.total_amount
                * (1 + self.interest_rate * 1e-2) ** self.number_of_years
            )
            / self.number_of_months,
        )
        return root_result.root


def compute_left_over_debt(
    total_amount: float, number_of_years: int, monthly_rate: float, interest: float
) -> list[float]:
    monthly_debt_evolution = [
        total_amount,
    ]
    monthly_interest = interest * 1e-2 / 12
    for _ in range(number_of_years * 12):
        left_amount = monthly_debt_evolution[-1]
        monthly_debt_evolution.append(
            left_amount * (1 + monthly_interest) - monthly_rate
        )
    return monthly_debt_evolution[1:]


def compute_monthly_rate_in_interest(
    total_amount: float, number_of_years: int, monthly_rate: float, interest: float
) -> list[float]:
    monthly_interest = interest * 1e-2 / 12
    monthly_rate_in_interest = list()
    left_amount = total_amount
    for _ in range(number_of_years * 12):
        monthly_rate_in_interest.append(left_amount * monthly_interest)
        left_amount = left_amount + monthly_rate_in_interest[-1] - monthly_rate
    return monthly_rate_in_interest
