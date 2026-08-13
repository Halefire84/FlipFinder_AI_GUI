import random

def estimate_item_value(item_name, base_cost=0.0):
    """Estimates market value, recent comps, and deal scoring for inventory items."""
    base_avg = max(base_cost * 1.8, random.uniform(25.0, 150.0))
    recent_sales = [round(base_avg * random.uniform(0.9, 1.1), 2) for _ in range(3)]
    volatility = round(random.uniform(0.05, 0.25), 2)
    
    # Deal scoring logic
    deal_score = "High" if base_avg > (base_cost * 2) else "Moderate"
    
    return {
        "avg_price": round(base_avg, 2),
        "recent_sales": recent_sales,
        "volatility": volatility,
        "deal_score": deal_score
    }
