import pandas as pd
import numpy as np
from collections import Counter
from datetime import datetime

# Load dataset
DF = pd.read_pickle("data/fashion_clean.pkl")

def analyze_seasonal_trends():
    """Analyze seasonal fashion trends from the dataset."""
    current_year = datetime.now().year
    
    # Group by season and analyze popular items
    seasonal_trends = {}
    
    for season in ['Spring', 'Summer', 'Fall', 'Winter']:
        season_data = DF[DF['season'] == season]
        
        if len(season_data) > 0:
            # Most popular categories
            top_categories = season_data['subCategory'].value_counts().head(5).to_dict()
            
            # Most popular colors
            top_colors = season_data['baseColour'].value_counts().head(5).to_dict()
            
            # Most popular article types
            top_articles = season_data['articleType'].value_counts().head(5).to_dict()
            
            seasonal_trends[season] = {
                'categories': top_categories,
                'colors': top_colors,
                'articles': top_articles,
                'total_items': len(season_data)
            }
    
    return seasonal_trends

def get_trending_items(limit=20):
    """Get currently trending items based on various factors."""
    # Simulate trending based on recent years and popular combinations
    recent_items = DF[DF['year'] >= 2015].copy() if 'year' in DF.columns else DF.copy()
    
    # Score items based on multiple factors
    trending_scores = []
    
    for _, item in recent_items.iterrows():
        score = 0
        
        # Recency bonus (newer items get higher scores)
        if 'year' in item and pd.notna(item['year']):
            year_score = (item['year'] - 2010) / 10  # Normalize to 0-1
            score += year_score * 30
        
        # Category popularity
        category_count = len(DF[DF['subCategory'] == item['subCategory']])
        category_score = min(category_count / 100, 1)  # Normalize
        score += category_score * 25
        
        # Color popularity
        color_count = len(DF[DF['baseColour'] == item['baseColour']])
        color_score = min(color_count / 50, 1)  # Normalize
        score += color_score * 20
        
        # Usage versatility (casual items tend to be more popular)
        if item['usage'] == 'Casual':
            score += 15
        elif item['usage'] == 'Formal':
            score += 10
        
        # Gender inclusivity bonus
        if item['gender'] in ['Men', 'Women']:
            score += 10
        
        trending_scores.append({
            'item': item.drop('embedding', errors='ignore').to_dict(),
            'trend_score': score,
            'factors': {
                'recency': year_score * 30 if 'year' in item and pd.notna(item['year']) else 0,
                'category_popularity': category_score * 25,
                'color_popularity': color_score * 20,
                'usage_appeal': 15 if item['usage'] == 'Casual' else 10,
                'gender_appeal': 10
            }
        })
    
    # Sort by trend score and return top items
    trending_scores.sort(key=lambda x: x['trend_score'], reverse=True)
    
    return {
        'trending_items': trending_scores[:limit],
        'analysis_date': datetime.now().isoformat(),
        'total_analyzed': len(trending_scores)
    }

def analyze_color_harmony(user_colors):
    """Analyze color harmony and suggest complementary colors."""
    
    # Color wheel relationships (simplified)
    color_relationships = {
        'Red': {
            'complementary': ['Green', 'Teal'],
            'analogous': ['Orange', 'Pink', 'Purple'],
            'triadic': ['Blue', 'Yellow']
        },
        'Blue': {
            'complementary': ['Orange', 'Yellow'],
            'analogous': ['Purple', 'Teal', 'Green'],
            'triadic': ['Red', 'Yellow']
        },
        'Green': {
            'complementary': ['Red', 'Pink'],
            'analogous': ['Blue', 'Yellow', 'Teal'],
            'triadic': ['Red', 'Purple']
        },
        'Yellow': {
            'complementary': ['Purple', 'Blue'],
            'analogous': ['Orange', 'Green'],
            'triadic': ['Red', 'Blue']
        },
        'Orange': {
            'complementary': ['Blue', 'Teal'],
            'analogous': ['Red', 'Yellow'],
            'triadic': ['Green', 'Purple']
        },
        'Purple': {
            'complementary': ['Yellow', 'Green'],
            'analogous': ['Red', 'Blue', 'Pink'],
            'triadic': ['Orange', 'Green']
        },
        'Pink': {
            'complementary': ['Green', 'Teal'],
            'analogous': ['Red', 'Purple'],
            'triadic': ['Blue', 'Yellow']
        },
        'Black': {
            'complementary': ['White', 'Grey'],
            'analogous': ['Grey', 'Navy'],
            'triadic': ['White', 'Silver']
        },
        'White': {
            'complementary': ['Black', 'Navy'],
            'analogous': ['Grey', 'Silver'],
            'triadic': ['Black', 'Grey']
        },
        'Grey': {
            'complementary': ['White', 'Black'],
            'analogous': ['Silver', 'Navy'],
            'triadic': ['White', 'Black']
        }
    }
    
    suggestions = {
        'complementary': set(),
        'analogous': set(),
        'triadic': set(),
        'neutral_pairs': set()
    }
    
    # Add neutral colors that go with everything
    neutrals = ['Black', 'White', 'Grey', 'Navy', 'Beige']
    
    for color in user_colors:
        if color in color_relationships:
            suggestions['complementary'].update(color_relationships[color]['complementary'])
            suggestions['analogous'].update(color_relationships[color]['analogous'])
            suggestions['triadic'].update(color_relationships[color]['triadic'])
        
        # Add neutrals for any color
        suggestions['neutral_pairs'].update(neutrals)
    
    # Remove colors user already has
    for key in suggestions:
        suggestions[key] = list(suggestions[key] - set(user_colors))
    
    return {
        'user_colors': user_colors,
        'color_suggestions': suggestions,
        'harmony_tips': [
            "Complementary colors create bold, high-contrast looks",
            "Analogous colors create harmonious, cohesive outfits",
            "Triadic colors offer vibrant yet balanced combinations",
            "Neutral colors are versatile and pair well with any color"
        ]
    }

def get_style_insights(liked_items_df):
    """Generate detailed style insights from user's liked items."""
    
    insights = {
        'dominant_style': None,
        'color_personality': None,
        'versatility_score': 0,
        'seasonal_preference': None,
        'formality_level': None,
        'recommendations': []
    }
    
    if len(liked_items_df) == 0:
        return insights
    
    # Analyze dominant style
    usage_counts = liked_items_df['usage'].value_counts()
    if len(usage_counts) > 0:
        insights['dominant_style'] = usage_counts.index[0]
        
        # Determine formality level
        casual_ratio = usage_counts.get('Casual', 0) / len(liked_items_df)
        if casual_ratio > 0.7:
            insights['formality_level'] = 'Casual-focused'
        elif casual_ratio < 0.3:
            insights['formality_level'] = 'Formal-focused'
        else:
            insights['formality_level'] = 'Balanced'
    
    # Analyze color personality
    color_counts = liked_items_df['baseColour'].value_counts()
    color_diversity = len(color_counts) / len(liked_items_df)
    
    if color_diversity > 0.6:
        insights['color_personality'] = 'Colorful Explorer'
    elif color_diversity < 0.3:
        insights['color_personality'] = 'Minimalist Palette'
    else:
        insights['color_personality'] = 'Balanced Color User'
    
    # Calculate versatility score
    category_diversity = len(liked_items_df['subCategory'].unique())
    max_categories = len(DF['subCategory'].unique())
    insights['versatility_score'] = min(100, (category_diversity / max_categories) * 100)
    
    # Seasonal preference
    if 'season' in liked_items_df.columns:
        season_counts = liked_items_df['season'].value_counts()
        if len(season_counts) > 0:
            insights['seasonal_preference'] = season_counts.index[0]
    
    # Generate recommendations
    recommendations = []
    
    if insights['versatility_score'] < 50:
        recommendations.append("Try exploring new categories to increase outfit versatility")
    
    if color_diversity < 0.4:
        recommendations.append("Consider adding more colors to create diverse looks")
    
    if insights['formality_level'] == 'Casual-focused':
        recommendations.append("Add some formal pieces for special occasions")
    elif insights['formality_level'] == 'Formal-focused':
        recommendations.append("Include casual pieces for everyday comfort")
    
    insights['recommendations'] = recommendations
    
    return insights
