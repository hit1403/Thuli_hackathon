import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import random

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
    tops = df[(df["id"].isin(capsule)) & (df["subCategory"] == "Topwear")]
    bottoms = df[(df["id"].isin(capsule)) & (df["subCategory"] == "Bottomwear")]
    shoes = df[(df["id"].isin(capsule)) & (df["masterCategory"] == "Footwear")]
    return len(tops) * len(bottoms) * len(shoes)

def capsule_optimizer_fast(liked_ids, budget=8):
    """Fast capsule wardrobe selection optimized for mobile."""
    df = DF.copy()
    user_vec = get_user_profile(liked_ids, df).reshape(1, -1)
    
    # Pre-filter to top 200 most similar items for speed
    embeddings = np.array([np.array(e) for e in df["embedding"].tolist() if e is not None])
    similarities = cosine_similarity(user_vec, embeddings)[0]
    df['similarity'] = similarities
    df_filtered = df.nlargest(200, 'similarity')
    
    # Ensure category balance
    categories = ['Topwear', 'Bottomwear', 'Footwear', 'Accessories']
    capsule = []
    
    for category in categories:
        if len(capsule) >= budget:
            break
        cat_items = df_filtered[df_filtered['subCategory'] == category] if category != 'Footwear' else df_filtered[df_filtered['masterCategory'] == category]
        if not cat_items.empty:
            # Take top 2 items from each category
            top_items = cat_items.nlargest(min(2, budget - len(capsule)), 'similarity')
            capsule.extend(top_items['id'].tolist())
    
    # Fill remaining slots with highest similarity items
    remaining_budget = budget - len(capsule)
    if remaining_budget > 0:
        used_ids = set(capsule)
        remaining_items = df_filtered[~df_filtered['id'].isin(used_ids)]
        if not remaining_items.empty:
            top_remaining = remaining_items.nlargest(remaining_budget, 'similarity')
            capsule.extend(top_remaining['id'].tolist())
    
    return capsule[:budget]

def capsule_optimizer(liked_ids, budget=12, alpha=0.6, beta=0.3, gamma=0.1):
    """Use fast optimizer for mobile compatibility."""
    return capsule_optimizer_fast(liked_ids, budget)
        item_dict['explanation'] = explanation
        capsule_items_with_explanations.append(item_dict)
    
    return {
        "capsule_items": capsule_items_with_explanations,
        "outfits_possible": outfit_combinations(capsule, df),
        "optimization_stats": {
            "total_items": len(capsule),
            "categories_covered": len(capsule_df['subCategory'].unique()),
            "color_diversity": len(capsule_df['baseColour'].unique())
        }
    }

def get_recommendations_with_serendipity(liked_ids, serendipity=0.5, limit=20):
    """Get recommendations with serendipity control."""
    df = DF.copy()
    user_vec = get_user_profile(liked_ids, df).reshape(1, -1)
    
    # Remove already liked items
    available_items = df[~df["id"].isin(liked_ids)].copy()
    
    recommendations = []
    for _, row in available_items.iterrows():
        emb = row["embedding"]
        if emb is None:
            continue
            
        # Similarity score
        similarity = cosine_similarity(user_vec, np.array(emb).reshape(1, -1))[0][0]
        
        # Novelty score (distance from user preferences)
        novelty = 1 - similarity
        
        # Diversity score (how different from already selected items)
        diversity = calculate_diversity_score(row.to_dict(), recommendations, df)
        
        # Combined score with serendipity control
        # serendipity = 0: focus on similarity (safe recommendations)
        # serendipity = 1: focus on novelty and diversity (adventurous)
        alpha = 1 - serendipity  # similarity weight
        beta = serendipity * 0.7  # novelty weight
        gamma = serendipity * 0.3  # diversity weight
        
        score = alpha * similarity + beta * novelty + gamma * diversity
        
        # Create item dict without embedding
        item_dict = row.to_dict()
        if 'embedding' in item_dict:
            del item_dict['embedding']
        
        recommendations.append({
            "item": item_dict,
            "score": score,
            "similarity": similarity,
            "novelty": novelty,
            "diversity": diversity,
            "explanation": generate_recommendation_explanation(row, similarity, novelty, serendipity)
        })
    
    # Sort by score and return top items
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    
    return {
        "recommendations": recommendations[:limit],
        "serendipity_level": serendipity,
        "total_available": len(recommendations)
    }

def calculate_diversity_score(item, selected_items, df):
    """Calculate how diverse an item is compared to already selected items."""
    if not selected_items:
        return 1.0
    
    # Simplified diversity based on category and color differences
    item_category = item.get("subCategory", "")
    item_color = item.get("baseColour", "")
    
    category_matches = 0
    color_matches = 0
    
    for selected in selected_items:
        selected_item = selected["item"]
        if selected_item.get("subCategory") == item_category:
            category_matches += 1
        if selected_item.get("baseColour") == item_color:
            color_matches += 1
    
    total_selected = len(selected_items)
    category_diversity = 1 - (category_matches / total_selected)
    color_diversity = 1 - (color_matches / total_selected)
    
    # Average of category and color diversity
    return (category_diversity + color_diversity) / 2

def generate_item_explanation(item, liked_ids, df):
    """Generate explanation for why an item was selected for the capsule."""
    liked_items = df[df["id"].isin(liked_ids)]
    
    # Find similar categories
    same_category = liked_items[liked_items["subCategory"] == item["subCategory"]]
    same_color = liked_items[liked_items["baseColour"] == item["baseColour"]]
    same_usage = liked_items[liked_items["usage"] == item["usage"]]
    
    explanations = []
    
    if len(same_category) > 0:
        explanations.append(f"matches your preference for {item['subCategory'].lower()}")
    
    if len(same_color) > 0:
        explanations.append(f"complements your favorite {item['baseColour'].lower()} pieces")
    
    if len(same_usage) > 0:
        explanations.append(f"fits your {item['usage'].lower()} style")
    
    # Check versatility
    if item["subCategory"] in ["Topwear", "Bottomwear"]:
        explanations.append("creates multiple outfit combinations")
    
    if not explanations:
        explanations.append("adds variety to your wardrobe")
    
    return f"Selected because it {' and '.join(explanations)}."

def generate_recommendation_explanation(item, similarity, novelty, serendipity):
    """Generate explanation for recommendation based on scores."""
    if serendipity < 0.3:  # Safe recommendations
        if similarity > 0.7:
            return f"Perfect match for your style preferences in {item['subCategory'].lower()}"
        else:
            return f"Good fit based on your liked {item['baseColour'].lower()} items"
    elif serendipity > 0.7:  # Adventurous recommendations
        if novelty > 0.6:
            return f"Something new to explore - {item['articleType']} in {item['baseColour']}"
        else:
            return f"Expands your style with this unique {item['subCategory'].lower()}"
    else:  # Balanced recommendations
        return f"Balanced choice that matches your taste while adding variety"

def analyze_color_palette(liked_ids, df):
    """Analyze user's color preferences and suggest complementary colors."""
    liked_items = df[df["id"].isin(liked_ids)]
    color_counts = liked_items["baseColour"].value_counts()
    
    # Define color harmony rules (simplified)
    color_harmonies = {
        "Black": ["White", "Grey", "Red", "Blue"],
        "White": ["Black", "Blue", "Red", "Green"],
        "Blue": ["White", "Grey", "Yellow", "Orange"],
        "Red": ["Black", "White", "Blue", "Green"],
        "Green": ["White", "Brown", "Yellow", "Red"],
        "Grey": ["Black", "White", "Blue", "Pink"],
        "Brown": ["White", "Green", "Orange", "Yellow"],
        "Pink": ["Grey", "White", "Black", "Blue"],
        "Yellow": ["Blue", "Green", "Brown", "Purple"],
        "Orange": ["Blue", "Brown", "White", "Green"]
    }
    
    primary_colors = color_counts.head(3).index.tolist()
    suggested_colors = set()
    
    for color in primary_colors:
        if color in color_harmonies:
            suggested_colors.update(color_harmonies[color])
    
    # Remove colors user already likes
    suggested_colors = suggested_colors - set(primary_colors)
    
    return {
        "primary_colors": primary_colors,
        "suggested_colors": list(suggested_colors)[:5],
        "color_distribution": color_counts.to_dict()
    }
