class DealScorer:
    def __init__(self, acquisition_cost, estimated_resale_value, shipping_cost=0.0, platform_fee_percent=0.13, repair_cost=0.0):
        self.acquisition_cost = float(acquisition_cost)
        self.estimated_resale_value = float(estimated_resale_value)
        self.shipping_cost = float(shipping_cost)
        self.platform_fee_percent = float(platform_fee_percent)
        self.repair_cost = float(repair_cost)
        
    def calculate_net_profit(self):
        platform_fees = self.estimated_resale_value * self.platform_fee_percent
        total_investment = self.acquisition_cost + self.shipping_cost + self.repair_cost
        net_profit = self.estimated_resale_value - (platform_fees + total_investment)
        return round(net_profit, 2)
        
    def calculate_roi(self):
        total_investment = self.acquisition_cost + self.shipping_cost + self.repair_cost
        if total_investment <= 0:
            return 0.0
        net_profit = self.calculate_net_profit()
        roi = (net_profit / total_investment) * 100
        return round(roi, 2)
        
    def evaluate_deal(self):
        net_profit = self.calculate_net_profit()
        roi = self.calculate_roi()
        
        # Heuristic grading framework for automated inventory tracking
        if roi >= 100 and net_profit >= 50:
            rating = "A+ (High Priority Flip)"
        elif roi >= 50 and net_profit >= 25:
            rating = "B (Solid Margin)"
        elif roi > 0:
            rating = "C (Low Margin / Risky)"
        else:
            rating = "F (Loss Expected)"
            
        return {
            "net_profit": net_profit,
            "roi_percentage": roi,
            "deal_rating": rating
        }
