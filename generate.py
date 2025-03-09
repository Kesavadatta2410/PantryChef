import google.generativeai as genai
import json
from predict import predict_image # Import the function to predict ingredients
genai.configure(api_key="AIzaSyAcyv0PJR_2RzyfiuDKQ9gGpyZFXwnkqMg")


# Use an available Gemini model from your list
model = genai.GenerativeModel("models/gemini-1.5-pro")

def get_recipes(ingredients):
    """Generate recipes based on a list of ingredients."""
    prompt = f"Suggest 5-10 recipes using {', '.join(ingredients)} with step-by-step instructions."
    response = model.generate_content(prompt)
    
    return response.text if response else "No recipes found."

if __name__ == "__main__":
    # Step 1: Get manually entered ingredients
    manual_ingredients = input("Enter ingredients separated by commas: ").strip().split(',')

    # Step 2: Get recognized ingredient from an image
    image_path = "C:/Users/datta/OneDrive/Documents/pics/test/turnip/Image_9.jpg"  # Update as needed
    predicted_label, confidence = predict_image(image_path)

    print(f"\nPredicted Ingredient: {predicted_label} (Confidence: {confidence:.2f})")

    # Step 3: Combine both lists, remove duplicates
    all_ingredients = list(set([item.strip().lower() for item in manual_ingredients + [predicted_label]]))

    print(f"\nFinal Ingredients List: {all_ingredients}")

    # Step 4: Fetch recipes using Gemini API
    recipes = get_recipes(all_ingredients)
    print("\nGenerated Recipes:\n", recipes)
