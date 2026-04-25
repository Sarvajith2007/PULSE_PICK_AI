import pandas as pd
from transformers import pipeline

# 1. Load the Sentiment Analysis Model (Pre-trained RoBERTa)
print("Loading AI Model (RoBERTa)... This may take a minute on first run.")
# We use 'sentiment-analysis' pipeline which is beginner-friendly for labs
analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")

def calculate_pulse_score():
    # 2. Load your 10-laptop CSV
    try:
        df = pd.read_csv("laptops_data.csv")
    except FileNotFoundError:
        print("Error: laptops_data.csv not found. Run the scraper first!")
        return

    # 3. 10 Sample Reviews for your 10 Laptops
    # (In the final project, these will be scraped from Reddit/Amazon)
    reviews = [
        "Amazing performance, but the battery life is quite poor.",
        "Best gaming laptop for the price. Build quality is solid.",
        "Heating issues after 2 hours of gaming. Disappointed.",
        "Great screen and keyboard, highly recommend for coders.",
        "Too heavy to carry around, but the GPU is a beast.",
        "Excellent thermals, never goes above 70 degrees while gaming.",
        "The display is color accurate, perfect for video editing.",
        "Average build quality, feels a bit plastic-y for the price.",
        "Incredible refresh rate, games look butter smooth.",
        "The fan noise is way too loud, sounds like a jet engine."
    ]

    print(f"Analyzing {len(df)} laptops with AI...")
    
    pulse_scores = []
    reasoning_summaries = []

    # 4. Process each laptop with its corresponding review
    for i in range(len(df)):
        # If you have more laptops than reviews, this prevents errors
        review_text = reviews[i] if i < len(reviews) else "Good all-rounder laptop."
        
        result = analyzer(review_text)[0]
        label = result['label']
        confidence = result['score']

        # Logic to calculate the "Pulse Score" (0 to 100)
        if label.lower() == 'positive':
            score = 75 + (confidence * 25) # Scores between 75-100
        elif label.lower() == 'neutral':
            score = 50 + (confidence * 20) # Scores between 50-70
        else:
            score = 20 + (confidence * 30) # Scores between 20-50
            
        pulse_scores.append(round(score, 1))
        reasoning_summaries.append(review_text)

    # 5. Add new columns to your DataFrame
    df['Pulse_Score'] = pulse_scores
    df['Expert_Insight'] = reasoning_summaries

    # 6. Save the results
    df.to_csv("laptops_with_scores.csv", index=False)
    print("--------------------------------------------------")
    print("SUCCESS: Intelligent Pulse Scores calculated for all 10 laptops!")
    print("New file created: laptops_with_scores.csv")
    print("--------------------------------------------------")

if __name__ == "__main__":
    calculate_pulse_score()