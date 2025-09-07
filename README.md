# StyleGenius - AI-Powered Fashion Recommendation App

A React Native mobile application that delivers personalized fashion recommendations through an intelligent style quiz and capsule wardrobe optimization system.

## Demo
Watch the DEMO here : https://drive.google.com/file/d/1KYw-1R_t8StdfBXZawt7kLeCjS0JpHhv/view?usp=drive_link

## 🚀 Features

### Core Functionality
- **Interactive Style Quiz**: 20-item quiz to understand user fashion preferences
- **AI-Powered Capsule Wardrobe**: Optimized selection of 8-20 items that maximize outfit combinations
- **Style Personality Analysis**: Detailed insights into user's fashion preferences

### Advanced Features
- **Outfit Visualizer**: Interactive mannequin showing outfit combinations with compatibility scoring
- **Color Harmony Analysis**: Smart color palette suggestions based on color theory

## 🏗️ Architecture

### Backend (FastAPI)
- **Dataset**: 2000+ fashion items with CLIP embeddings
- **ML Models**: Cosine similarity for style matching, greedy optimization for capsule selection
- **APIs**: RESTful endpoints for quiz, recommendations, capsule generation, and trend analysis

### Frontend (React Native + Expo)
- **Navigation**: Stack-based navigation between screens
- **State Management**: React hooks for local state
- **UI Components**: Custom components with modern design
- **Responsive Design**: Optimized for mobile devices

## 📱 Screens

1. **Welcome Screen**: App introduction with gradient design
2. **Quiz Screen**: Interactive style quiz with progress tracking
3. **Profile Screen**: Style personality analysis and color preferences
4. **Capsule Screen**: Optimized wardrobe with outfit visualizer and serendipity controls

## 🛠️ Installation & Setup

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Prerequisites
- Python 3.8+
- Node.js 16+
- Expo CLI
- Fashion dataset with embeddings (included)

## 📊 Dataset

The app uses a curated fashion dataset with:
- **2000+ items** across multiple categories
- **CLIP embeddings** for semantic similarity
- **Attributes**: Color, category, usage, season, gender
- **Metadata**: Brand names, product descriptions

## 🤖 AI/ML Components

### Recommendation Algorithm
```python
score = α * similarity + β * novelty + γ * diversity
```
- **Similarity**: Cosine similarity to user preferences
- **Novelty**: Distance from familiar items (serendipity)
- **Diversity**: Variety in recommendations

### Capsule Optimization
- **Greedy Algorithm**: Iteratively selects items that maximize outfit combinations
- **Multi-objective**: Balances similarity, coverage, and diversity
- **Constraints**: Budget limits and category requirements

### Style Analysis
- **Color Theory**: Complementary, analogous, and triadic color relationships
- **Personality Types**: 5 distinct style personalities based on preferences
- **Trend Detection**: Seasonal and temporal pattern analysis


## 🔧 API Endpoints

### Quiz & Profile
- `GET /quiz/items` - Get quiz items
- `POST /quiz/feedback` - Submit quiz responses
- `GET /item/{id}` - Get item details

### Recommendations
- `POST /recommendations` - Get personalized recommendations
- `POST /capsule` - Generate capsule wardrobe


## 🚀 Deployment

### Backend Deployment
```bash
# Using uvicorn for production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend Deployment
```bash
# Build for production
expo build:android
expo build:ios
```

## 📈 Performance Optimizations

- **Embedding Caching**: Pre-computed CLIP embeddings for fast similarity search
- **Efficient Algorithms**: O(n) greedy optimization for capsule selection
- **Lazy Loading**: Components load as needed
- **Image Optimization**: Placeholder images for fast rendering

## 🎯 Future Enhancements

### Technical Improvements
- **Real Images**: Integration with fashion retailer APIs
- **Advanced ML**: Transformer-based recommendation models
- **Real-time Updates**: Live trend analysis and inventory updates
- **Personalization**: Learning from user interactions

## 📝 Technical Specifications

### Backend Stack
- **Framework**: FastAPI 0.104.1
- **ML Libraries**: scikit-learn, pandas, numpy
- **Data Processing**: CLIP embeddings, k-means clustering
- **API Design**: RESTful with automatic documentation

### Frontend Stack
- **Framework**: React Native with Expo
- **Navigation**: React Navigation 6
- **UI Components**: Custom components with react-native-super-grid
- **State Management**: React hooks and context

### Data Pipeline
1. **Data Collection**: Fashion dataset curation
2. **Preprocessing**: Cleaning and normalization
3. **Feature Extraction**: CLIP embedding generation
4. **Storage**: Pickle files for fast loading


## 📊 Analytics & Insights

### User Metrics
- **Quiz Completion Rate**: Track user engagement
- **Style Diversity**: Measure recommendation variety
- **Capsule Satisfaction**: Outfit combination usage
- **Serendipity Usage**: Adventure vs. safety preferences

### Business Metrics
- **Recommendation Accuracy**: User feedback on suggestions
- **Engagement Time**: Session duration and frequency
- **Feature Usage**: Most popular app sections
- **Conversion Potential**: Items users show interest in

