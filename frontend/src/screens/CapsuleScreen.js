import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  ActivityIndicator,
  Alert,
  Dimensions,
  FlatList,
  Image,
} from 'react-native';
import { apiService } from '../services/api';

const { width } = Dimensions.get('window');

const CapsuleScreen = ({ route }) => {
  const { likedIds } = route.params;
  const [capsuleData, setCapsuleData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [budget, setBudget] = useState(12);

  useEffect(() => {
    loadCapsule();
  }, []);

  const loadCapsule = async () => {
    try {
      setLoading(true);
      const data = await apiService.getCapsule(likedIds, budget);
      setCapsuleData(data);
    } catch (error) {
      Alert.alert('Error', 'Failed to load capsule wardrobe. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const loadRecommendations = async () => {
    try {
      const data = await apiService.getRecommendations(likedIds, serendipity, 12);
      setRecommendations(data.recommendations);
    } catch (error) {
      Alert.alert('Error', 'Failed to load recommendations. Please try again.');
    }
  };

  const getSerendipityLabel = (value) => {
    if (value < 0.3) return 'Safe & Familiar';
    if (value < 0.7) return 'Balanced Mix';
    return 'Adventurous & Bold';
  };

  const renderCapsuleItem = ({ item }) => (
    <View style={styles.itemCard}>
      <View style={styles.itemImagePlaceholder}>
        {item.imageUrl ? (
          <Image 
            source={{ uri: item.imageUrl }} 
            style={styles.itemImage}
            resizeMode="cover"
          />
        ) : (
          <Text style={styles.itemImageText}>{item.articleType}</Text>
        )}
      </View>
      <View style={styles.itemInfo}>
        <Text style={styles.itemName} numberOfLines={2}>
          {item.productDisplayName}
        </Text>
        <Text style={styles.itemCategory}>
          {item.subCategory} • {item.baseColour}
        </Text>
        <Text style={styles.itemUsage}>{item.usage}</Text>
        {item.explanation && (
          <Text style={styles.itemExplanation} numberOfLines={3}>
            {item.explanation}
          </Text>
        )}
      </View>
    </View>
  );

  const renderRecommendationItem = ({ item }) => (
    <View style={styles.recommendationCard}>
      <View style={styles.itemImagePlaceholder}>
        {item.item.imageUrl ? (
          <Image 
            source={{ uri: item.item.imageUrl }} 
            style={styles.itemImage}
            resizeMode="cover"
          />
        ) : (
          <Text style={styles.itemImageText}>{item.item.articleType}</Text>
        )}
      </View>
      <View style={styles.itemInfo}>
        <Text style={styles.itemName} numberOfLines={2}>
          {item.item.productDisplayName}
        </Text>
        <Text style={styles.itemCategory}>
          {item.item.subCategory} • {item.item.baseColour}
        </Text>
        <View style={styles.scoreContainer}>
          <View style={styles.scoreItem}>
            <Text style={styles.scoreLabel}>Match</Text>
            <Text style={styles.scoreValue}>{Math.round(item.similarity * 100)}%</Text>
          </View>
          <View style={styles.scoreItem}>
            <Text style={styles.scoreLabel}>Novelty</Text>
            <Text style={styles.scoreValue}>{Math.round(item.novelty * 100)}%</Text>
          </View>
        </View>
        {item.explanation && (
          <Text style={styles.itemExplanation} numberOfLines={2}>
            {item.explanation}
          </Text>
        )}
      </View>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#667eea" />
        <Text style={styles.loadingText}>Creating your capsule wardrobe...</Text>
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        {/* Capsule Summary */}
        <View style={styles.summaryCard}>
          <Text style={styles.summaryTitle}>Your Capsule Wardrobe</Text>
          <View style={styles.summaryStats}>
            <View style={styles.statItem}>
              <Text style={styles.statNumber}>{capsuleData?.capsule_items?.length || 0}</Text>
              <Text style={styles.statLabel}>Items</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statNumber}>{capsuleData?.outfits_possible || 0}</Text>
              <Text style={styles.statLabel}>Possible Outfits</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statNumber}>
                {capsuleData?.optimization_stats?.categories_covered || 0}
              </Text>
              <Text style={styles.statLabel}>Categories</Text>
            </View>
          </View>
        </View>

        {/* Budget Slider */}
        <View style={styles.controlCard}>
          <Text style={styles.controlTitle}>Capsule Size: {budget} items</Text>
          <Slider
            style={styles.slider}
            minimumValue={8}
            maximumValue={20}
            value={budget}
            onValueChange={setBudget}
            onSlidingComplete={setBudget}
            step={1}
            minimumTrackTintColor="#667eea"
            maximumTrackTintColor="#e9ecef"
            thumbStyle={styles.sliderThumb}
          />
        </View>

        {/* Outfit Visualizer */}
        {capsuleData?.capsule_items && (
          <OutfitVisualizer capsuleItems={capsuleData.capsule_items} />
        )}

        {/* Capsule Items Grid */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Capsule Items</Text>
          <FlatGrid
            itemDimension={width * 0.4}
            data={capsuleData?.capsule_items || []}
            style={styles.grid}
            spacing={12}
            renderItem={renderCapsuleItem}
            scrollEnabled={false}
          />
        </View>

        {/* Serendipity Section */}
        <View style={styles.controlCard}>
          <Text style={styles.controlTitle}>
            Discover More: {getSerendipityLabel(serendipity)}
          </Text>
          <Text style={styles.controlDescription}>
            Adjust to find safe recommendations or explore new styles
          </Text>
          <Slider
            style={styles.slider}
            minimumValue={0}
            maximumValue={1}
            value={serendipity}
            onValueChange={setSerendipity}
            minimumTrackTintColor="#667eea"
            maximumTrackTintColor="#e9ecef"
            thumbStyle={styles.sliderThumb}
          />
          <View style={styles.sliderLabels}>
            <Text style={styles.sliderLabel}>Safe</Text>
            <Text style={styles.sliderLabel}>Adventurous</Text>
          </View>
          
          <TouchableOpacity
            style={styles.recommendButton}
            onPress={() => {
              setShowRecommendations(!showRecommendations);
              if (!showRecommendations) {
                loadRecommendations();
              }
            }}
          >
            <Text style={styles.recommendButtonText}>
              {showRecommendations ? 'Hide Recommendations' : 'Show Recommendations'}
            </Text>
          </TouchableOpacity>
        </View>

        {/* Recommendations */}
        {showRecommendations && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Recommended for You</Text>
            <FlatGrid
              itemDimension={width * 0.4}
              data={recommendations}
              style={styles.grid}
              spacing={12}
              renderItem={renderRecommendationItem}
              scrollEnabled={false}
            />
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f8f9fa',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666',
  },
  content: {
    flexGrow: 1,
    padding: 16,
  },
  summaryCard: {
    backgroundColor: '#667eea',
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
  },
  summaryTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
    marginBottom: 20,
  },
  summaryStats: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  statItem: {
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
  },
  statLabel: {
    fontSize: 14,
    color: '#fff',
    opacity: 0.8,
  },
  controlCard: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
  },
  controlTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 8,
  },
  controlDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 16,
  },
  slider: {
    width: '100%',
    height: 40,
  },
  sliderThumb: {
    backgroundColor: '#667eea',
    width: 20,
    height: 20,
  },
  sliderLabels: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 8,
  },
  sliderLabel: {
    fontSize: 12,
    color: '#666',
  },
  recommendButton: {
    backgroundColor: '#667eea',
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 16,
  },
  recommendButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  section: {
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 16,
  },
  grid: {
    flex: 1,
  },
  itemCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 12,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  recommendationCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 12,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    borderLeftWidth: 3,
    borderLeftColor: '#667eea',
  },
  itemImage: {
    height: 120,
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
    width: '100%',
  },
  itemImagePlaceholder: {
    height: 120,
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
    borderWidth: 1,
    borderColor: '#e9ecef',
    borderStyle: 'dashed',
  },
  itemImageText: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#667eea',
    textAlign: 'center',
  },
  itemInfo: {
    flex: 1,
  },
  itemName: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 4,
  },
  itemCategory: {
    fontSize: 12,
    color: '#667eea',
    marginBottom: 2,
  },
  itemUsage: {
    fontSize: 11,
    color: '#666',
    marginBottom: 4,
  },
  itemExplanation: {
    fontSize: 10,
    color: '#666',
    fontStyle: 'italic',
    lineHeight: 14,
  },
  scoreContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginVertical: 4,
  },
  scoreItem: {
    alignItems: 'center',
  },
  scoreLabel: {
    fontSize: 10,
    color: '#666',
  },
  scoreValue: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#667eea',
  },
});

export default CapsuleScreen;
