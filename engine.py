import numpy as np
import skfuzzy as fuzz
from geopy.distance import geodesic
from skfuzzy import control as ctrl
import pandas as pd


class RestaurantRecommender:
    def __init__(self, restaurants_file, neighborhoods_file):
        self.restaurants = pd.read_csv(restaurants_file)
        self.neighborhoods = pd.read_csv(neighborhoods_file)
        self._setup_fuzzy_logic()

    def _setup_fuzzy_logic(self):
        self.cuisine = ctrl.Antecedent(np.arange(0, 4, 1), 'cuisine')
        self.price = ctrl.Antecedent(np.arange(0, 10000, 500), 'price')
        self.location = ctrl.Antecedent(np.arange(0, 5, 1), 'location')

        self.cuisine['سوري'] = fuzz.trimf(self.cuisine.universe, [0, 0, 1])
        self.cuisine['لبناني'] = fuzz.trimf(self.cuisine.universe, [1, 1, 2])
        self.cuisine['متوسطي'] = fuzz.trimf(self.cuisine.universe, [2, 2, 3])
        self.cuisine['إيطالي'] = fuzz.trimf(self.cuisine.universe, [3, 3, 3])

        # self.price['cheap'] = fuzz.trimf(self.price.universe, [-5000, 1000, 4000])
        # self.price['moderate'] = fuzz.trimf(self.price.universe, [2000, 5000, 8000])
        # self.price['expensive'] = fuzz.trimf(self.price.universe, [6000, 10000, 10000])

        self.price['cheap'] = fuzz.trimf(self.price.universe, [-5000, 1000, 2000])
        self.price['moderate'] = fuzz.trimf(self.price.universe, [1000, 3000, 5000])
        self.price['expensive'] = fuzz.trimf(self.price.universe, [4000, 10000, 10000])

        self.location['near'] = fuzz.trimf(self.location.universe, [0, 1, 1.5])
        self.location['medium'] = fuzz.trimf(self.location.universe, [1, 2, 2.5])
        self.location['far'] = fuzz.trimf(self.location.universe, [2, 3, 3])

        self.recommendation = ctrl.Consequent(np.arange(0, 11, 1), 'recommendation')

        self.recommendation['not_recommended'] = fuzz.trimf(self.recommendation.universe, [0, 0, 4])
        self.recommendation['recommended'] = fuzz.trimf(self.recommendation.universe, [2, 5, 8])
        self.recommendation['highly_recommended'] = fuzz.trimf(self.recommendation.universe, [6, 10, 10])

        self.rules = [
            ctrl.Rule(self.cuisine['سوري'] & self.price['cheap'] & self.location['near'],
                      self.recommendation['highly_recommended']),
            ctrl.Rule(self.cuisine['سوري'] & self.price['cheap'] & self.location['medium'],
                      self.recommendation['recommended']),
            ctrl.Rule(self.cuisine['سوري'] & self.price['cheap'] & self.location['far'],
                      self.recommendation['not_recommended']),
            ctrl.Rule(self.cuisine['سوري'] & self.price['moderate'] & self.location['near'],
                      self.recommendation['recommended']),
            ctrl.Rule(self.cuisine['سوري'] & self.price['moderate'] & self.location['medium'],
                      self.recommendation['recommended']),
            ctrl.Rule(self.cuisine['سوري'] & self.price['moderate'] & self.location['far'],
                      self.recommendation['not_recommended']),
            ctrl.Rule(self.cuisine['سوري'] & self.price['expensive'] & self.location['near'],
                      self.recommendation['recommended']),
            ctrl.Rule(self.cuisine['سوري'] & self.price['expensive'] & self.location['medium'],
                      self.recommendation['not_recommended']),
            ctrl.Rule(self.cuisine['سوري'] & self.price['expensive'] & self.location['far'],
                      self.recommendation['not_recommended']),

            ctrl.Rule(self.cuisine['لبناني'] & self.price['cheap'] & self.location['near'],
                      self.recommendation['highly_recommended']),
            ctrl.Rule(self.cuisine['لبناني'] & self.price['cheap'] & self.location['medium'],
                      self.recommendation['recommended']),
            ctrl.Rule(self.cuisine['لبناني'] & self.price['cheap'] & self.location['far'],
                      self.recommendation['not_recommended']),
            ctrl.Rule(self.cuisine['لبناني'] & self.price['moderate'] & self.location['near'],
                      self.recommendation['recommended']),
            ctrl.Rule(self.cuisine['لبناني'] & self.price['moderate'] & self.location['medium'],
                      self.recommendation['recommended']),
            ctrl.Rule(self.cuisine['لبناني'] & self.price['moderate'] & self.location['far'],
                      self.recommendation['not_recommended']),
            ctrl.Rule(self.cuisine['لبناني'] & self.price['expensive'] & self.location['near'],
                      self.recommendation['recommended']),
            ctrl.Rule(self.cuisine['لبناني'] & self.price['expensive'] & self.location['medium'],
                      self.recommendation['not_recommended']),
            ctrl.Rule(self.cuisine['لبناني'] & self.price['expensive'] & self.location['far'],
                      self.recommendation['not_recommended']),

            ctrl.Rule(self.cuisine['متوسطي'] & self.price['cheap'] & self.location['near'],
                      self.recommendation['highly_recommended']),
            ctrl.Rule(self.cuisine['متوسطي'] & self.price['cheap'] & self.location['medium'],
                      self.recommendation['highly_recommended']),
            ctrl.Rule(self.cuisine['متوسطي'] & self.price['cheap'] & self.location['far'],
                      self.recommendation['recommended']),
            ctrl.Rule(self.cuisine['متوسطي'] & self.price['moderate'] & self.location['near'],
                      self.recommendation['highly_recommended']),
            ctrl.Rule(self.cuisine['متوسطي'] & self.price['moderate'] & self.location['medium'],
                      self.recommendation['recommended']),
            ctrl.Rule(self.cuisine['متوسطي'] & self.price['moderate'] & self.location['far'],
                      self.recommendation['recommended']),
            ctrl.Rule(self.cuisine['متوسطي'] & self.price['expensive'] & self.location['near'],
                      self.recommendation['recommended']),
            ctrl.Rule(self.cuisine['متوسطي'] & self.price['expensive'] & self.location['medium'],
                      self.recommendation['recommended']),
            ctrl.Rule(self.cuisine['متوسطي'] & self.price['expensive'] & self.location['far'],
                      self.recommendation['recommended']),
            
            ctrl.Rule(self.cuisine['إيطالي'] & self.price['cheap'] & self.location['near'],
                      self.recommendation['highly_recommended']),
            ctrl.Rule(self.cuisine['إيطالي'] & self.price['cheap'] & self.location['medium'],
                      self.recommendation['highly_recommended']),
            ctrl.Rule(self.cuisine['إيطالي'] & self.price['cheap'] & self.location['far'],
                      self.recommendation['recommended']),
            ctrl.Rule(self.cuisine['إيطالي'] & self.price['moderate'] & self.location['near'],
                      self.recommendation['recommended']),
            ctrl.Rule(self.cuisine['إيطالي'] & self.price['moderate'] & self.location['medium'],
                      self.recommendation['recommended']),
            ctrl.Rule(self.cuisine['إيطالي'] & self.price['moderate'] & self.location['far'],
                      self.recommendation['not_recommended']),
            ctrl.Rule(self.cuisine['إيطالي'] & self.price['expensive'] & self.location['near'],
                      self.recommendation['recommended']),
            ctrl.Rule(self.cuisine['إيطالي'] & self.price['expensive'] & self.location['medium'],
                      self.recommendation['not_recommended']),
            ctrl.Rule(self.cuisine['إيطالي'] & self.price['expensive'] & self.location['far'],
                      self.recommendation['not_recommended']),
        ]

        self.restaurant_ctrl = ctrl.ControlSystem(self.rules)
        self.restaurant_sim = ctrl.ControlSystemSimulation(self.restaurant_ctrl)

    @staticmethod
    def calculate_location(user_location, restaurant_location):
        return geodesic(user_location, restaurant_location).kilometers

    def get_restaurants_by_type(self, cuisine_type):
        return self.restaurants[self.restaurants['نوع المأكولات'] == cuisine_type].copy()

    @staticmethod
    def calculate_price_difference(user_price, res):
        res['(ليرة سورية) فرق السعر'] = res['متوسط سعر الوجبة (ليرة سورية)'].subtract(user_price)
        print(res['(ليرة سورية) فرق السعر'])
        return res

    @staticmethod
    def classify_distance(distance):
        if distance <= 1.5:
            return 'Close to you'
        elif distance <= 2.5:
            return 'Not that Far'
        else:
            return 'Far from Here'

    def calculate_distances(self, res, user_location):
        distances = []
        distances_classification = []
        for _, row in res.iterrows():
            restaurant_location = (row['y'], row['x'])
            distance = geodesic(user_location, restaurant_location).kilometers
            classification = self.classify_distance(distance)
            distances.append(distance)
            distances_classification.append(classification)
        res['المسافة بالكيلو متر'] = distances
        res['البعد'] = distances_classification

    def get_neighborhood_location(self, neighborhood):
        temp = self.neighborhoods[self.neighborhoods['Neighborhood'] == neighborhood]
        return [temp['Latitude'].values[0], temp['Longitude'].values[0]]

    @staticmethod
    def get_cuisine_type_index(cuisine_type):
        cuisine_types = {'سوري': 0, 'لبناني': 1, 'متوسطي': 3, 'إيطالي': 4}
        return cuisine_types.get(cuisine_type, 0)

    @staticmethod
    def classify_recommendation(fuzzy_value):
        if fuzzy_value <= 4:
            return 'Not Recommended'
        elif fuzzy_value <= 8:
            return 'Recommended'
        else:
            return 'Highly Recommended'

    def fuzz_input(self, res, cuisine_type):
        n = self.get_cuisine_type_index(cuisine_type)
        recommendations = []
        classifications = []
        for _, row in res.iterrows():
            self.restaurant_sim.input['cuisine'] = n
            self.restaurant_sim.input['location'] = row['المسافة بالكيلو متر']
            self.restaurant_sim.input['price'] = row['(ليرة سورية) فرق السعر']

            try:
                self.restaurant_sim.compute()
                fuzzy_output = self.restaurant_sim.output['recommendation']
                recommendations.append(fuzzy_output)
                classification = self.classify_recommendation(fuzzy_output)
                classifications.append(classification)
            except ValueError as e:
                print(f"Error computing fuzzy output for restaurant {row['اسم المطعم']}: {str(e)}")
                recommendations.append(np.nan)
                classifications.append('Error')

        res['اقتراح'] = recommendations
        res['التصنيف'] = classifications

    def recommend_restaurants(self, user_location, cuisine_type, user_price):
        user_location_coords = self.get_neighborhood_location(user_location)
        res = self.get_restaurants_by_type(cuisine_type)
        self.calculate_distances(res, user_location_coords)
        self.calculate_price_difference(user_price, res)
        self.fuzz_input(res, cuisine_type)
        return res

    @staticmethod
    def save_recommendations_to_json(recommendations_df, filename):
        recommendations_df.to_json(filename, orient='records', force_ascii=False)
