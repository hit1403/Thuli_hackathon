from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np
import os
from models.capsule_fast import capsule_optimizer, get_recommendations_with_serendipity,get_capsule_wardrobe
from models.trend_analysis import analyze_seasonal_trends, get_trending_items, analyze_color_harmony, get_style_insights
import random

def get_local_image_url(item_id, base_url="http://10.173.129.6:8001"):
    """Generate local image URL for an item"""
    return f"{base_url}/images/{item_id}.jpg"

app = FastAPI(title="Style Quiz Backend", version="1.0")

# Mount static files for images
app.mount("/images", StaticFiles(directory="data/images"), name="images")

# Add CORS middleware for React Native
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load dataset
DF = pd.read_pickle("data/fashion_clean.pkl")

class CapsuleRequest(BaseModel):
    liked_ids: List[int]
    budget: Optional[int] = 12
    alpha: Optional[float] = 0.6  # similarity weight
    beta: Optional[float] = 0.3   # coverage weight
    gamma: Optional[float] = 0.1  # diversity weight

class QuizFeedback(BaseModel):
    item_id: int
    liked: bool

class RecommendationRequest(BaseModel):
    liked_ids: List[int]
    serendipity: Optional[float] = 0.5  # 0 = safe, 1 = adventurous
    limit: Optional[int] = 10

@app.get("/")
def root():
    return {"message": "Style Quiz Backend is running 🚀"}

@app.get("/quiz/items")
def get_quiz_items(count: int = 20):
    """Get random items for the style quiz"""
    try:
        # Get a diverse sample across categories
        sample_items = []
        categories = DF['subCategory'].unique()
        
        items_per_category = max(1, count // len(categories))
        
        for category in categories:
            category_items = DF[DF['subCategory'] == category].sample(
                min(items_per_category, len(DF[DF['subCategory'] == category])),
                random_state=None  # Remove fixed seed for randomization
            )
            sample_items.append(category_items)
        
        # If we need more items, sample randomly
        if len(pd.concat(sample_items)) < count:
            remaining = count - len(pd.concat(sample_items))
            additional = DF.sample(remaining, random_state=None)  # Remove fixed seed
            sample_items.append(additional)
        
        # Concatenate and remove embedding before drop_duplicates to avoid hashing issues
        result_df = pd.concat(sample_items)
        result_df = result_df.drop(columns=['embedding'], errors='ignore').drop_duplicates().head(count)
        
        # Add local image URLs and convert to dict for JSON serialization
        items_dict = []
        for _, row in result_df.iterrows():
            item = row.to_dict()
            
            # Add local image URL
            item_id = item.get('id', 10000)  # Default fallback ID
            item['imageUrl'] = get_local_image_url(item_id)
            
            items_dict.append(item)
        
        return {
            "items": items_dict,
            "total": len(result_df)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/quiz/feedback")
def submit_quiz_feedback(feedback_list: List[QuizFeedback]):
    """Store quiz feedback and return user profile insights"""
    try:
        liked_ids = [f.item_id for f in feedback_list if f.liked]
        disliked_ids = [f.item_id for f in feedback_list if not f.liked]
        
        if not liked_ids:
            return {"message": "No liked items to analyze", "profile": {}}
        
        # Analyze user preferences
        liked_items = DF[DF['id'].isin(liked_ids)]
        
        # Get style insights
        top_categories = liked_items['subCategory'].value_counts().head(3).to_dict()
        top_colors = liked_items['baseColour'].value_counts().head(3).to_dict()
        preferred_usage = liked_items['usage'].value_counts().head(2).to_dict()
        
        # Get advanced style insights
        style_insights = get_style_insights(liked_items)
        
        # Get color harmony suggestions
        user_colors = list(top_colors.keys())
        color_analysis = analyze_color_harmony(user_colors)
        
        profile = {
            "liked_count": len(liked_ids),
            "disliked_count": len(disliked_ids),
            "top_categories": top_categories,
            "favorite_colors": top_colors,
            "style_usage": preferred_usage,
            "style_personality": determine_style_personality(liked_items),
            "style_insights": style_insights,
            "color_analysis": color_analysis
        }
        
        return {
            "message": "Quiz completed successfully!",
            "profile": profile,
            "liked_ids": liked_ids
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommendations")
def get_recommendations(req: RecommendationRequest):
    """Get personalized recommendations with serendipity control"""
    try:
        print(f"DEBUG: Getting recommendations for liked_ids: {req.liked_ids}")
        recommendations = get_recommendations_with_serendipity(
            liked_ids=req.liked_ids,
            serendipity=req.serendipity,
            limit=req.limit
        )
        print(f"DEBUG: Got {len(recommendations.get('recommendations', []))} recommendations")
        return recommendations
    except Exception as e:
        print(f"DEBUG: Error in recommendations endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/capsule")
def get_capsule(req: CapsuleRequest):
    """Generate optimized capsule wardrobe"""
    try:
        print(f"DEBUG: Getting capsule for liked_ids: {req.liked_ids}, budget: {req.budget}, alpha: {req.alpha}, beta: {req.beta}, gamma: {req.gamma}")
        result = get_capsule_wardrobe(
            liked_ids=req.liked_ids,
            budget=req.budget,
            alpha=req.alpha,
            beta=req.beta,
            gamma=req.gamma
        )
        print(f"DEBUG: Capsule generation successful")
        return result
    except Exception as e:
        print(f"DEBUG: Error in capsule endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/item/{item_id}")
def get_item_details(item_id: int):
    """Get detailed information about a specific item"""
    try:
        item = DF[DF['id'] == item_id]
        if item.empty:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # Convert to dict and remove embedding for JSON serialization
        item_dict = item.drop(columns=['embedding'], errors='ignore').iloc[0].to_dict()
        return item_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trends/seasonal")
def get_seasonal_trends():
    """Get seasonal fashion trends analysis"""
    try:
        trends = analyze_seasonal_trends()
        return trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trends/trending")
def get_trending_items_endpoint(limit: int = 20):
    """Get currently trending fashion items"""
    try:
        trending = get_trending_items(limit)
        return trending
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analysis/color-harmony")
def analyze_user_colors(colors: List[str]):
    """Analyze color harmony for user's color preferences"""
    try:
        analysis = analyze_color_harmony(colors)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def determine_style_personality(liked_items):
    """Determine user's style personality based on liked items"""
    casual_count = len(liked_items[liked_items['usage'] == 'Casual'])
    formal_count = len(liked_items[liked_items['usage'] == 'Formal'])
    
    color_diversity = len(liked_items['baseColour'].unique())
    category_diversity = len(liked_items['subCategory'].unique())
    
    total_items = len(liked_items)
    
    if casual_count > formal_count * 2:
        if color_diversity > total_items * 0.6:
            return "Adventurous Casual"
        else:
            return "Classic Casual"
    elif formal_count > casual_count:
        return "Professional Minimalist"
    else:
        if category_diversity > total_items * 0.5:
            return "Versatile Explorer"
        else:
            return "Balanced Stylist"
