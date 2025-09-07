import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Dimensions,
} from 'react-native';

const { width } = Dimensions.get('window');

const OutfitVisualizer = ({ capsuleItems }) => {
  const [currentOutfit, setCurrentOutfit] = useState({});
  const [outfitCount, setOutfitCount] = useState(0);

  useEffect(() => {
    generateRandomOutfit();
    calculateTotalOutfits();
  }, [capsuleItems]);

  const categorizeItems = () => {
    const categories = {
      tops: capsuleItems.filter(item => item.subCategory === 'Topwear'),
      bottoms: capsuleItems.filter(item => item.subCategory === 'Bottomwear'),
      shoes: capsuleItems.filter(item => item.masterCategory === 'Footwear'),
      accessories: capsuleItems.filter(item => item.masterCategory === 'Accessories'),
    };
    return categories;
  };

  const generateRandomOutfit = () => {
    const categories = categorizeItems();
    const outfit = {};

    if (categories.tops.length > 0) {
      outfit.top = categories.tops[Math.floor(Math.random() * categories.tops.length)];
    }
    if (categories.bottoms.length > 0) {
      outfit.bottom = categories.bottoms[Math.floor(Math.random() * categories.bottoms.length)];
    }
    if (categories.shoes.length > 0) {
      outfit.shoes = categories.shoes[Math.floor(Math.random() * categories.shoes.length)];
    }
    if (categories.accessories.length > 0) {
      outfit.accessory = categories.accessories[Math.floor(Math.random() * categories.accessories.length)];
    }

    setCurrentOutfit(outfit);
  };

  const calculateTotalOutfits = () => {
    const categories = categorizeItems();
    const total = Math.max(1, categories.tops.length) * 
                 Math.max(1, categories.bottoms.length) * 
                 Math.max(1, categories.shoes.length);
    setOutfitCount(total);
  };

  const renderOutfitItem = (item, position) => {
    if (!item) return null;

    return (
      <View style={[styles.outfitItem, styles[position]]}>
        <View style={styles.itemPlaceholder}>
          <Text style={styles.itemText}>{item.articleType}</Text>
        </View>
        <Text style={styles.itemLabel} numberOfLines={1}>
          {item.baseColour} {item.articleType}
        </Text>
      </View>
    );
  };

  const getOutfitCompatibility = () => {
    const { top, bottom, shoes } = currentOutfit;
    let score = 0;
    let reasons = [];

    // Color compatibility
    if (top && bottom) {
      const neutralColors = ['Black', 'White', 'Grey', 'Navy'];
      if (neutralColors.includes(top.baseColour) || neutralColors.includes(bottom.baseColour)) {
        score += 30;
        reasons.push('Great color coordination');
      } else if (top.baseColour === bottom.baseColour) {
        score += 20;
        reasons.push('Monochromatic style');
      }
    }

    // Usage compatibility
    if (top && bottom && top.usage === bottom.usage) {
      score += 25;
      reasons.push(`Perfect for ${top.usage.toLowerCase()} occasions`);
    }

    // Season compatibility
    if (top && bottom && top.season === bottom.season) {
      score += 20;
      reasons.push(`Great for ${top.season.toLowerCase()}`);
    }

    // Style versatility
    if (Object.keys(currentOutfit).length >= 3) {
      score += 25;
      reasons.push('Complete outfit with accessories');
    }

    return { score: Math.min(100, score), reasons };
  };

  const compatibility = getOutfitCompatibility();

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Outfit Visualizer</Text>
        <Text style={styles.subtitle}>
          {outfitCount} possible combinations
        </Text>
      </View>

      <View style={styles.outfitContainer}>
        <View style={styles.mannequin}>
          {renderOutfitItem(currentOutfit.top, 'top')}
          {renderOutfitItem(currentOutfit.bottom, 'bottom')}
          {renderOutfitItem(currentOutfit.shoes, 'shoes')}
          {renderOutfitItem(currentOutfit.accessory, 'accessory')}
        </View>
      </View>

      <View style={styles.compatibilityCard}>
        <View style={styles.scoreContainer}>
          <Text style={styles.scoreLabel}>Compatibility Score</Text>
          <Text style={[styles.score, { color: compatibility.score > 70 ? '#27ae60' : compatibility.score > 40 ? '#f39c12' : '#e74c3c' }]}>
            {compatibility.score}%
          </Text>
        </View>
        <ScrollView style={styles.reasonsContainer} showsVerticalScrollIndicator={false}>
          {compatibility.reasons.map((reason, index) => (
            <Text key={index} style={styles.reason}>• {reason}</Text>
          ))}
        </ScrollView>
      </View>

      <TouchableOpacity style={styles.shuffleButton} onPress={generateRandomOutfit}>
        <Text style={styles.shuffleButtonText}>🎲 Shuffle Outfit</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 20,
    margin: 16,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
  },
  header: {
    alignItems: 'center',
    marginBottom: 20,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  subtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  outfitContainer: {
    alignItems: 'center',
    marginBottom: 20,
  },
  mannequin: {
    width: width * 0.6,
    height: 300,
    position: 'relative',
    backgroundColor: '#f8f9fa',
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#e9ecef',
    borderStyle: 'dashed',
  },
  outfitItem: {
    position: 'absolute',
    alignItems: 'center',
  },
  top: {
    top: 20,
    left: '50%',
    marginLeft: -40,
    width: 80,
  },
  bottom: {
    top: 120,
    left: '50%',
    marginLeft: -40,
    width: 80,
  },
  shoes: {
    bottom: 20,
    left: '50%',
    marginLeft: -30,
    width: 60,
  },
  accessory: {
    top: 10,
    right: 10,
    width: 40,
  },
  itemPlaceholder: {
    backgroundColor: '#667eea',
    borderRadius: 8,
    padding: 8,
    minHeight: 40,
    justifyContent: 'center',
    alignItems: 'center',
  },
  itemText: {
    fontSize: 10,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
  },
  itemLabel: {
    fontSize: 8,
    color: '#666',
    textAlign: 'center',
    marginTop: 4,
  },
  compatibilityCard: {
    backgroundColor: '#f8f9fa',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  scoreContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  scoreLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2c3e50',
  },
  score: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  reasonsContainer: {
    maxHeight: 60,
  },
  reason: {
    fontSize: 12,
    color: '#666',
    marginBottom: 4,
  },
  shuffleButton: {
    backgroundColor: '#667eea',
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  shuffleButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default OutfitVisualizer;
