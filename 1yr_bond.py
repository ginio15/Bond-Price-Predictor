def price_bond(
    face_amount,
    coupon_rate,
    periods_per_year,
    maturity_years,
    daycount_convention,
    market_discount_rate
):
    """
    Returns the price of the bond (expressed as a fraction of the Face Amount),
    i.e., Price = Present Value of all coupon & principal payments / Face Amount.
    """


    # Determine the number of coupon periods over the bond's life.
    # For a 4-year bond with 4 periods per year (quarterly), that's 16 periods total.
    total_periods = int(maturity_years * periods_per_year)

    #   Calculate the coupon payment per period.
    #   The ANNUAL coupon is face_amount * coupon_rate.
    #   The PERIODIC coupon is (annual coupon) / periods_per_year.
    # Example: If face_amount = 24,000, interest_rate = 10%, periods_per_year = 4,
    #           then each period coupon = 24,000 * 0.10 / 4 = 600
    coupon_per_period = face_amount * (coupon_rate / periods_per_year)

    #  Sum the present value of each cash flow (coupon or principal).
    # We'll use standard compounding: discount factor = 1 / (1 + i/m)^n,
    #   where i = market discount rate, m = periods_per_year, and n = period index
    # For bullet bonds:
    #   - Every period: you get a coupon (except for possible day-count adjustments).
    #   - Final period: you also get the face_amount (principal) repaid.

    present_value_of_cash_flows = 0.0

    # Loop over each coupon period (t = 1 to total_periods)
    for t in range(1, total_periods + 1):
        # Period t in years. If ignoring exact daycount logic, each period is 1/periods_per_year years.
        # For more accurate daycount: we could multiply by actual days/360, etc.
        # But we'll keep it simple here.
        period_fraction_of_year = 1.0 / periods_per_year

        # The discount rate per period:
        # (market_discount_rate / periods_per_year).
        # The exponent is t (the period number).
        discount_factor = 1.0 / ((1.0 + (market_discount_rate / periods_per_year)) ** t)

        # Coupon payment in this period (same every period for a vanilla coupon).
        # If your bond structure had changing coupons or daycount-based changes, we'd adjust here.
        coupon_cash_flow = coupon_per_period

        # Principal payment is 0 in every period except the last one (for a bullet bond).
        if t == total_periods:
            principal_payment = face_amount
        else:
            principal_payment = 0.0

        # Total payment in this period = coupon + principal
        total_payment = coupon_cash_flow + principal_payment

        # Present value of this period's payment
        present_value_of_payment = total_payment * discount_factor

        # Accumulate into the total present value of all cash flows
        present_value_of_cash_flows += present_value_of_payment

    # --------------------------------------------------------------------
    # STEP D: Compute the bond price as a fraction of face amount.
    # Price (often expressed as "percentage of par")
    #   = (PV of all coupon & principal) / face_amount.
    # --------------------------------------------------------------------
    bond_price = present_value_of_cash_flows / face_amount

    return bond_price


# ------------------------------------------------------------------------------
# EXAMPLE OF USING THE price_bond FUNCTION
# ------------------------------------------------------------------------------
if __name__ == "__main__":

    face_amount_input          = 200
    coupon_rate_input          = 0.10
    periods_per_year_input     = 4
    maturity_years_input       = 4
    daycount_convention_input  = "Actual/360"

    for discount_rate_percent in range(7, 14):

        market_discount_rate_input = discount_rate_percent / 100.0

        price_as_fraction_of_par = price_bond(
            face_amount_input,
            coupon_rate_input,
            periods_per_year_input,
            maturity_years_input,
            daycount_convention_input,
            market_discount_rate_input
        )


        price_percentage = price_as_fraction_of_par * 100.0

        print(f"Market Discount Rate = {discount_rate_percent}%  =>  Bond Price = {price_percentage:.2f}% of Face Amount")