import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  Dimensions,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

const { width } = Dimensions.get('window');

const ProfileScreen = ({ navigation, route }) => {
  const { profile, likedIds } = route.params;

  const renderColorPalette = (colors) => {
    const colorMap = {
      Black: '#000000',
      White: '#FFFFFF',
      Blue: '#3498db',
      Red: '#e74c3c',
      Green: '#27ae60',
      Grey: '#95a5a6',
      Brown: '#8b4513',
      Pink: '#e91e63',
      Yellow: '#f1c40f',
      Orange: '#f39c12',
      Purple: '#9b59b6',
    };

    return Object.entries(colors).map(([color, count]) => (
      <View key={color} style={styles.colorItem}>
        <View 
          style={[
            styles.colorSwatch, 
            { backgroundColor: colorMap[color] || '#ccc' },
            color === 'White' && { borderWidth: 1, borderColor: '#ddd' }
          ]} 
        />
        <Text style={styles.colorText}>{color} ({count})</Text>
      </View>
    ));
  };

  const renderCategoryChart = (categories) => {
    const total = Object.values(categories).reduce((sum, count) => sum + count, 0);
    
    return Object.entries(categories).map(([category, count]) => {
      const percentage = (count / total) * 100;
      return (
        <View key={category} style={styles.categoryItem}>
          <Text style={styles.categoryLabel}>{category}</Text>
          <View style={styles.categoryBarContainer}>
            <View 
              style={[styles.categoryBar, { width: `${percentage}%` }]} 
            />
          </View>
          <Text style={styles.categoryCount}>{count}</Text>
        </View>
      );
    });
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <LinearGradient
          colors={['#667eea', '#764ba2']}
          style={styles.headerGradient}
        >
          <View style={styles.headerContent}>
            <Text style={styles.personalityTitle}>Your Style Personality</Text>
            <Text style={styles.personalityType}>{profile.style_personality}</Text>
            <View style={styles.statsContainer}>
              <View style={styles.statItem}>
                <Text style={styles.statNumber}>{profile.liked_count}</Text>
                <Text style={styles.statLabel}>Liked Items</Text>
              </View>
              <View style={styles.statItem}>
                <Text style={styles.statNumber}>{profile.disliked_count}</Text>
                <Text style={styles.statLabel}>Passed Items</Text>
              </View>
            </View>
          </View>
        </LinearGradient>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Favorite Categories</Text>
          <View style={styles.sectionContent}>
            {renderCategoryChart(profile.top_categories)}
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Color Preferences</Text>
          <View style={styles.colorPalette}>
            {renderColorPalette(profile.favorite_colors)}
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Style Usage</Text>
          <View style={styles.usageContainer}>
            {Object.entries(profile.style_usage).map(([usage, count]) => (
              <View key={usage} style={styles.usageItem}>
                <Text style={styles.usageLabel}>{usage}</Text>
                <Text style={styles.usageCount}>{count} items</Text>
              </View>
            ))}
          </View>
        </View>

        <View style={styles.buttonContainer}>
          <TouchableOpacity
            style={styles.capsuleButton}
            onPress={() => navigation.navigate('Capsule', { likedIds })}
          >
            <Text style={styles.buttonText}>Create My Capsule Wardrobe</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  content: {
    flexGrow: 1,
  },
  headerGradient: {
    paddingVertical: 40,
    paddingHorizontal: 20,
  },
  headerContent: {
    alignItems: 'center',
  },
  personalityTitle: {
    fontSize: 18,
    color: '#fff',
    opacity: 0.9,
    marginBottom: 8,
  },
  personalityType: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
    marginBottom: 30,
  },
  statsContainer: {
    flexDirection: 'row',
    gap: 40,
  },
  statItem: {
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
  },
  statLabel: {
    fontSize: 14,
    color: '#fff',
    opacity: 0.8,
  },
  section: {
    margin: 20,
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 20,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 16,
  },
  sectionContent: {
    gap: 12,
  },
  categoryItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  categoryLabel: {
    fontSize: 16,
    color: '#2c3e50',
    width: 80,
  },
  categoryBarContainer: {
    flex: 1,
    height: 8,
    backgroundColor: '#e9ecef',
    borderRadius: 4,
  },
  categoryBar: {
    height: '100%',
    backgroundColor: '#667eea',
    borderRadius: 4,
  },
  categoryCount: {
    fontSize: 14,
    color: '#666',
    width: 30,
    textAlign: 'right',
  },
  colorPalette: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  colorItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 8,
  },
  colorSwatch: {
    width: 24,
    height: 24,
    borderRadius: 12,
  },
  colorText: {
    fontSize: 14,
    color: '#2c3e50',
  },
  usageContainer: {
    gap: 12,
  },
  usageItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
    paddingHorizontal: 12,
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
  },
  usageLabel: {
    fontSize: 16,
    color: '#2c3e50',
    fontWeight: '500',
  },
  usageCount: {
    fontSize: 14,
    color: '#667eea',
    fontWeight: 'bold',
  },
  buttonContainer: {
    padding: 20,
  },
  capsuleButton: {
    backgroundColor: '#667eea',
    paddingVertical: 18,
    borderRadius: 12,
    alignItems: 'center',
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});

export default ProfileScreen;
