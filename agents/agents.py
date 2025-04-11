# agents.py

import pandas as pd

class CustomerAgent:
    def __init__(self, customer_id, customer_df):
        self.customer_id = customer_id
        self.customer_df = customer_df
        self.profile = self.get_profile()

    def get_profile(self):
        return self.customer_df[self.customer_df['Customer_ID'] == self.customer_id].squeeze()

    def get_preferences(self):
        return self.profile.get('Preferred_Categories', '').split(',')

class ProductAgent:
    def __init__(self, product_df):
        self.product_df = product_df

    def get_similar_products(self, category):
        return self.product_df[self.product_df['Category'] == category]

    def filter_by_rating(self, threshold=4.0):
        return self.product_df[self.product_df['Product_Rating'] >= threshold]

class RecommendationAgent:
    def __init__(self, model, encoder, product_agent):
        self.model = model
        self.encoder = encoder
        self.product_agent = product_agent

    def recommend(self, category, product_features):
        encoded_cat = self.encoder.transform([[category]])
        features = pd.concat([
            product_features.reset_index(drop=True), 
            pd.DataFrame(encoded_cat, columns=self.encoder.get_feature_names_out())
        ], axis=1)

        features = features.drop(['Category'], axis=1, errors='ignore')
        features['Predicted_Probability'] = self.model.predict(features)
        return features.sort_values(by='Predicted_Probability', ascending=False)
