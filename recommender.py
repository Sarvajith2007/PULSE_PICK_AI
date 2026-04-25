import pandas as pd
from sentence_transformers import SentenceTransformer, util
import time
import os

# 1. Load the model first
print("Initializing PulsePick AI Engine...")
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_recommendation():
    # Load the data
    try:
        df = pd.read_csv("laptops_with_scores.csv")
    except FileNotFoundError:
        print("Error: laptops_with_scores.csv not found! Run sentiment_engine.py first.")
        return

    # Combine data for semantic matching
    df['search_profile'] = df['Product Name'] + " " + df['Expert_Insight']
    product_embeddings = model.encode(df['search_profile'].tolist(), convert_to_tensor=True)

    # CLEAR THE TERMINAL for a clean look
    os.system('cls' if os.name == 'nt' else 'clear')

    print("====================================================")
    print("           WELCOME TO PULSEPICK AI                  ")
    print("      Your Intelligent Electronics Consultant       ")
    print("====================================================")

    while True:
        print("\n[Type 'exit' to quit the program]")
        # THIS IS THE PART THAT WAITS FOR YOU
        user_query = input("\nWhat is your requirement? (e.g. 'coding', 'gaming', 'lightweight'): ").strip()

        if user_query.lower() == 'exit':
            print("Thank you for using PulsePick AI!")
            break
        
        if not user_query:
            print("Please enter a valid requirement.")
            continue

        print(f"\nSearching for the best match for: '{user_query}'...")
        time.sleep(1) # Visual delay for a "processing" feel

        # Calculate Similarity
        query_embedding = model.encode(user_query, convert_to_tensor=True)
        cosine_scores = util.cos_sim(query_embedding, product_embeddings)[0]

        df['match_score'] = cosine_scores.tolist()
        
        # Ranking Logic: 70% Context Match + 30% User Pulse Score
        df['final_rank'] = (df['match_score'] * 0.7) + ((df['Pulse_Score']/100) * 0.3)
        
        results = df.sort_values(by='final_rank', ascending=False).head(3)

        print("\n--- TOP 3 INTELLIGENT RECOMMENDATIONS ---")
        for idx, row in results.iterrows():
            print(f"\n> {row['Product Name']}")
            print(f"  Price: {row['Price (INR)']}")
            print(f"  Pulse Score: {row['Pulse_Score']}/100")
            print(f"  AI Insight: {row['Expert_Insight']}")
        print("\n" + "="*50)

if __name__ == "__main__":
    get_recommendation()