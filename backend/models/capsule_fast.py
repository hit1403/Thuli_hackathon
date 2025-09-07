import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any
import random

def get_local_image_url(item_id, base_url="http://10.173.129.6:8001"):
    """Generate local image URL for an item"""
    return f"{base_url}/images/{item_id}.jpg"

# Load dataset globally (only once at startup)
DF = pd.read_pickle("data/fashion_clean.pkl")

def get_user_profile(liked_ids, df):
    """Compute user preference vector (centroid of liked items)."""
    liked_embeds = df[df["id"].isin(liked_ids)]["embedding"].tolist()
    liked_embeds = [e for e in liked_embeds if e is not None]
    if not liked_embeds:
        return np.zeros((512,))
    # Convert list embeddings to numpy arrays
    liked_embeds = [np.array(e) for e in liked_embeds]
    return np.mean(np.vstack(liked_embeds), axis=0)

def outfit_combinations(capsule, df):
    """Count how many valid outfits can be formed from capsule items."""
    if not capsule:
        return 0
    capsule_df = df[df["id"].isin(capsule)]
    tops = len(capsule_df[capsule_df["subCategory"] == "Topwear"])
    bottoms = len(capsule_df[capsule_df["subCategory"] == "Bottomwear"])
    shoes = len(capsule_df[capsule_df["masterCategory"] == "Footwear"])
    return max(1, tops * bottoms * shoes)

def capsule_optimizer(liked_ids, budget=8,alpha=0.6, beta=0.3, gamma=0.1):
    """Fast capsule wardrobe selection optimized for mobile (< 5 seconds)."""
    return capsule_optimizer_fast(liked_ids, budget,alpha,beta,gamma)

def capsule_optimizer_fast(liked_ids, budget=8,alpha=0.6, beta=0.3, gamma=0.1):
    """Fast capsule wardrobe selection optimized for mobile (< 5 seconds)."""
    try:
        df = DF.copy()
        print(f"Starting capsule optimization for {len(liked_ids)} liked items...")
        
        if not liked_ids:
            print("No liked items provided, returning empty capsule")
            return []
            
        user_vec = get_user_profile(liked_ids, df).reshape(1, -1)
        
        # Pre-filter to top 500 most similar items for speed
        print(f"Processing {len(df)} items for capsule optimization...")
        
        # Calculate similarities for all items at once (vectorized)
        embeddings = []
        valid_indices = []
        for idx, emb in enumerate(df["embedding"].tolist()):
            if emb is not None and len(emb) > 0:
                try:
                    embeddings.append(np.array(emb))
                    valid_indices.append(idx)
                except Exception as e:
                    print(f"Error processing embedding at index {idx}: {e}")
                    continue
        
        if not embeddings:
            print("No valid embeddings found, returning random items")
            return df.sample(min(budget, len(df)))['id'].tolist()
        
        embeddings_matrix = np.vstack(embeddings)
        similarities = cosine_similarity(user_vec, embeddings_matrix)[0]
        
        # Add similarities back to dataframe
        df_valid = df.iloc[valid_indices].copy()
        df_valid['similarity'] = similarities
        
        # Filter to top 500 for speed
        df_filtered = df_valid.nlargest(min(500, len(df_valid)), 'similarity')
        
        # Ensure category balance for a complete wardrobe
        capsule = []
        
        # Priority categories for a functional wardrobe
        category_priorities = [
            ('Topwear', 3),      # 3 tops
            ('Bottomwear', 2),   # 2 bottoms  
            ('Footwear', 2),     # 2 shoes
            ('Accessories', 1)   # 1 accessory
        ]
        
        for category, target_count in category_priorities:
            if len(capsule) >= budget:
                break
                
            if category == 'Footwear':
                cat_items = df_filtered[df_filtered['masterCategory'] == category]
            else:
                cat_items = df_filtered[df_filtered['subCategory'] == category]
            
            if not cat_items.empty:
                # Take top items from this category
                slots_available = min(target_count, budget - len(capsule))
                top_items = cat_items.nlargest(slots_available, 'similarity')
                capsule.extend(top_items['id'].tolist())
        
        # Fill remaining slots with highest similarity items
        remaining_budget = budget - len(capsule)
        if remaining_budget > 0:
            used_ids = set(capsule)
            remaining_items = df_filtered[~df_filtered['id'].isin(used_ids)]
            if not remaining_items.empty:
                top_remaining = remaining_items.nlargest(remaining_budget, 'similarity')
                capsule.extend(top_remaining['id'].tolist())
        
        print(f"Generated capsule with {len(capsule)} items")
        return capsule[:budget]
        
    except Exception as e:
        print(f"Error in capsule optimization: {e}")
        # Fallback: return random items if optimization fails
        try:
            return DF.sample(min(budget, len(DF)))['id'].tolist()
        except:
            return []

def generate_capsule_explanation(item, similarity_score):
    """Generate explanation for why item was selected."""
    explanations = [
        f"Selected for {item['usage'].lower()} occasions",
        f"Matches your preference for {item['baseColour'].lower()} items",
        f"Perfect {item['articleType'].lower()} for your style",
        f"Essential {item['subCategory'].lower()} piece",
        f"Versatile {item['season'].lower()} item"
    ]
    return random.choice(explanations)

def get_capsule_wardrobe(liked_ids, budget=8,alpha=0.6, beta=0.3, gamma=0.1):
    """Main function to get capsule wardrobe with explanations."""
    print(f"Starting capsule optimization for {len(liked_ids)} liked items with budget {budget}")
    
    # Get optimized capsule
    capsule = capsule_optimizer_fast(liked_ids, budget,alpha,beta,gamma)
    
    if not capsule:
        return {
            "capsule_items": [],
            "outfits_possible": 0,
            "optimization_stats": {
                "total_items": 0,
                "categories_covered": 0,
                "color_diversity": 0
            }
        }
    
    # Get item details with explanations
    df = DF.copy()
    capsule_df = df[df["id"].isin(capsule)]
    capsule_items_with_explanations = []
    
    for _, row in capsule_df.iterrows():
        item_dict = row.drop('embedding').to_dict()
        explanation = generate_capsule_explanation(item_dict, 0.8)
        item_dict['explanation'] = explanation
        
        # Add local image URL
        item_id = item_dict.get('id', 10000)  # Default fallback ID
        item_dict['imageUrl'] = get_local_image_url(item_id)
        
        capsule_items_with_explanations.append(item_dict)
    
    # Calculate statistics
    outfits = outfit_combinations(capsule, df)
    categories = len(capsule_df['subCategory'].unique())
    colors = len(capsule_df['baseColour'].unique())
    
    print(f"Capsule complete: {len(capsule)} items, {outfits} outfits possible")
    
    return {
        "capsule_items": capsule_items_with_explanations,
        "outfits_possible": outfits,
        "optimization_stats": {
            "total_items": len(capsule),
            "categories_covered": categories,
            "color_diversity": colors
        }
    }

def calculate_diversity_score(item, existing_recommendations, df):
    """Simple diversity calculation."""
    if not existing_recommendations:
        return 1.0
    return 0.5  # Simplified for speed

def get_recommendations_with_serendipity(liked_ids, serendipity=0.5, limit=20):
    """Get recommendations with serendipity control (optimized)."""
    df = DF.copy()
    user_vec = get_user_profile(liked_ids, df).reshape(1, -1)
    
    # Remove already liked items and pre-filter for speed
    available_items = df[~df["id"].isin(liked_ids)].copy()
    
    # Calculate similarities for all items at once
    embeddings = []
    valid_indices = []
    for idx, emb in enumerate(available_items["embedding"].tolist()):
        if emb is not None:
            embeddings.append(np.array(emb))
            valid_indices.append(idx)
    
    if not embeddings:
        return {"recommendations": []}
    
    embeddings_matrix = np.vstack(embeddings)
    similarities = cosine_similarity(user_vec, embeddings_matrix)[0]
    
    # Add similarities to dataframe
    available_valid = available_items.iloc[valid_indices].copy()
    available_valid['similarity'] = similarities
    
    # Apply serendipity and get top recommendations
    available_valid['novelty'] = 1 - available_valid['similarity']
    available_valid['diversity'] = 0.5  # Simplified
    
    # Serendipity weighting
    alpha = 1 - serendipity
    beta = serendipity * 0.7
    gamma = serendipity * 0.3
    
    available_valid['score'] = (alpha * available_valid['similarity'] + 
                               beta * available_valid['novelty'] + 
                               gamma * available_valid['diversity'])
    
    # Get top recommendations
    top_recs = available_valid.nlargest(limit, 'score')
    
    recommendations = []
    for _, row in top_recs.iterrows():
        item_dict = row.drop(['embedding', 'similarity', 'novelty', 'diversity', 'score']).to_dict()
        
        # Add local image URL
        item_id = item_dict.get('id', 10000)  # Default fallback ID
        item_dict['imageUrl'] = get_local_image_url(item_id)
        
        recommendations.append({
            "item": item_dict,
            "score": float(row['score']),
            "similarity": float(row['similarity']),
            "novelty": float(row['novelty']),
            "diversity": float(row['diversity']),
            "explanation": f"Recommended based on your style preferences"
        })
    
    return {"recommendations": recommendations}
