class RecommendationAgent:
    def recommend(self, customer_agent, product_agents):
        # Recommend products matching customer's category preferences
        recommended = []
        for product in product_agents:
            if product.category in customer_agent.preferences:
                recommended.append(product)
        # Sort by rating and return top 3
        recommended.sort(key=lambda x: x.rating, reverse=True)
        return recommended[:3]
