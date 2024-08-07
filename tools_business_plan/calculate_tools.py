from langchain.tools import tool

class CalculateTools:
    @tool("build_income_statement")
    def build_income_statement(cogs_percentage: float, expenses_percentage: float) -> str:
        """Build a financial projection for the next 3 years."""
        years = [1, 2, 3]
        initial_revenue = 250000  # Example initial revenue
        growth_rate = 0.25  # Example growth rate

        revenue = [initial_revenue * ((1 + growth_rate) ** year) for year in years]
        cogs = [rev * cogs_percentage / 100 for rev in revenue]
        expenses = [rev * expenses_percentage / 100 for rev in revenue]
        gross_profit = [rev - cog for rev, cog in zip(revenue, cogs)]
        net_income = [gp - exp for gp, exp in zip(gross_profit, expenses)]

        statement = "Year | Revenue | COGS | Gross Profit | Expenses | Net Income\n"
        statement += "--- | --- | --- | --- | --- | ---\n"
        for year, rev, cog, gp, exp, ni in zip(years, revenue, cogs, gross_profit, expenses, net_income):
            statement += f"{year} | ${rev:,.2f} | ${cog:,.2f} | ${gp:,.2f} | ${exp:,.2f} | ${ni:,.2f}\n"

        return statement
