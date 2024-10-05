import json
from collections import defaultdict

def process_data(data):
    portfolio = defaultdict(lambda: defaultdict(dict))
    for item in data:
        for summary in item.get('dtSummary', []):
            folio = summary['folio']
            isin = summary['isin']
            units = float(summary['closingBalance'])
            cost_value = float(summary['costValue'])
            nav = float(summary['nav'])
            
            portfolio[folio][isin] = {
                'units': units,
                'cost': cost_value,
                'nav': nav
            }
    return portfolio

def calculate_portfolio_value_and_gain(portfolio):
    total_value = 0
    total_gain = 0
    fund_details = {}

    for folio, funds in portfolio.items():
        for isin, details in funds.items():
            units = details['units']
            cost = details['cost']
            nav = details['nav']
            
            current_value = units * nav
            gain = current_value - cost
            
            total_value += current_value
            total_gain += gain
            
            fund_details[isin] = {
                "total_units": units,
                "current_value": current_value,
                "gain": gain,
                "cost": cost,
                "nav": nav
            }

    return total_value, total_gain, fund_details

def main(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        if 'data' not in data or not isinstance(data['data'], list):
            raise ValueError("Invalid JSON structure: 'data' key not found or not a list")
        
        portfolio = process_data(data['data'])
        total_value, total_gain, fund_details = calculate_portfolio_value_and_gain(portfolio)

        print(f"Total Portfolio Value: ₹{total_value:.2f}")
        print(f"Total Portfolio Gain: ₹{total_gain:.2f}")
        print("\nFund-wise details:")
        for isin, details in fund_details.items():
            print(f"ISIN: {isin}")
            print(f"  Total Units: {details['total_units']:.4f}")
            print(f"  Current NAV: ₹{details['nav']:.4f}")
            print(f"  Current Value: ₹{details['current_value']:.2f}")
            print(f"  Cost: ₹{details['cost']:.2f}")
            print(f"  Gain: ₹{details['gain']:.2f}")
            print()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main("transaction_detail.json")
