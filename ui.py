import customtkinter
import tkinterDnD
import json
from engine import RestaurantRecommender

customtkinter.set_ctk_parent_class(tkinterDnD.Tk)
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


class GUI:
    def __init__(self) -> None:
        self.root = customtkinter.CTk()
        self.root.geometry(f"{800}x{600}")
        self.root.title("Recommendation System for restaurants")
        self.locations = ['Old City (Ancient Damascus)', 'Al-Midan', 'Abu Rummaneh', 'Malki', 'Mezzeh', 'Kafar Souseh',
                          'Baramkeh', 'Qanawat', 'Bab Touma', 'Rukn al-Din', 'Mazraa', 'Salhiyah', 'Jobar', 'Yarmouk',
                          'Bab Sharqi']
        self.cuisine = ['سوري', 'لبناني', 'متوسطي', 'إيطالي']
        self.recommender = RestaurantRecommender('restaurants.csv', 'neighborhood.csv')
        self.sliderVar = customtkinter.IntVar()

        self.inputFrame = customtkinter.CTkFrame(master=self.root)
        self.inputFrame.pack(pady=20, padx=60, fill='both', expand=True)

        self.label = customtkinter.CTkLabel(master=self.inputFrame, text='Chose Your Preference')
        self.label.pack(pady=12, padx=10)

        self.optionMenu = customtkinter.CTkOptionMenu(self.inputFrame, values=self.cuisine)
        self.optionMenu.pack(pady=10, padx=10)
        self.optionMenu.set(self.cuisine[0])

        self.slider = customtkinter.CTkSlider(self.inputFrame, command=self.slider_callback, from_=1000, to=10000,
                                              number_of_steps=12, variable=self.sliderVar)
        self.slider.pack(pady=10, padx=10)
        self.slider.set(5500)

        self.labelVar = customtkinter.CTkLabel(self.inputFrame, textvariable=self.sliderVar)
        self.labelVar.pack(pady=12, padx=10)

        self.optionMenu1 = customtkinter.CTkOptionMenu(self.inputFrame, values=self.locations)
        self.optionMenu1.pack(pady=10, padx=10)
        self.optionMenu1.set(self.locations[0])

        self.button = customtkinter.CTkButton(master=self.inputFrame, text='Insert', command=self.print_selections)
        self.button.pack(pady=12, padx=10)

        self.textbox = customtkinter.CTkTextbox(self.inputFrame, width=100, height=20)
        self.textbox.pack(pady=20, padx=10, fill="both", expand=True)

    def slider_callback(self, value):
        self.slider.set(value)

    def print_selections(self):
        selected_cuisine = self.optionMenu.get()
        selected_location = self.optionMenu1.get()
        selected_price = self.slider.get()

        recommended_restaurants = self.recommender.recommend_restaurants(selected_location, selected_cuisine,
                                                                         selected_price)
        self.recommender.save_recommendations_to_json(recommended_restaurants, 'recommended_restaurants.json')

        json_data = self.load_json_data()
        self.display_json_data(json_data)

    @staticmethod
    def load_json_data():
        # Replace with your JSON file path
        json_file = "recommended_restaurants.json"

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            return json_data
        except FileNotFoundError:
            print(f"Error: File '{json_file}' not found.")
            return []
        except Exception as e:
            print(f"Error loading JSON file: {str(e)}")
            return []

    def display_json_data(self, json_data):
        self.textbox.delete("1.0", "end")

        for item in json_data:
            restaurant_name = item.get("اسم المطعم", "")
            cuisine_type = item.get("نوع المأكولات", "")
            location = item.get("الموقع", "")
            distance = item.get("المسافة بالكيلو متر", "")
            distanceClassification = item.get("البعد", "")
            avg_price = item.get("متوسط سعر الوجبة (ليرة سورية)", "")
            suggestionValue = item.get("اقتراح", "")
            suggestion = item.get("التصنيف", "")

            self.textbox.insert("end", f"Restaurant: {restaurant_name}\n")
            self.textbox.insert("end", f"Cuisine: {cuisine_type}\n")
            self.textbox.insert("end", f"Location: {location}\n")
            self.textbox.insert("end", f"Distance: {distance} km\n")
            self.textbox.insert("end", f"Distance: {distanceClassification}\n")
            self.textbox.insert("end", f"Average Price: {avg_price} sp\n")
            self.textbox.insert("end", f"Suggestion Value: {suggestionValue}\n")
            self.textbox.insert("end", f"Suggestion: {suggestion}\n")
            self.textbox.insert("end", "\n")
