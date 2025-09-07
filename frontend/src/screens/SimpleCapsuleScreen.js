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
  Image,
} from 'react-native';
import { apiService } from '../services/api';

const { width } = Dimensions.get('window');

const SimpleCapsuleScreen = ({ route, navigation }) => {
  const { likedIds } = route.params;
  const [capsuleData, setCapsuleData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCapsule();
  }, []);

  const loadCapsule = async () => {
    try {
      setLoading(true);
      console.log('Loading capsule for liked IDs:', likedIds);
      
      // Show a timeout warning after 15 seconds
      const timeoutWarning = setTimeout(() => {
        console.log('⏰ Capsule optimization is taking longer than expected...');
      }, 15000);
      
      const data = await apiService.getCapsule(likedIds, 8);
      clearTimeout(timeoutWarning);
      console.log('Capsule data received:', data);
      setCapsuleData(data);
    } catch (error) {
      console.error('Error loading capsule:', error);
      
      let errorMessage = 'Failed to load capsule wardrobe.';
      if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
        errorMessage = 'Capsule optimization timed out. The algorithm is processing your preferences - please try again.';
      } else if (error.message.includes('Network Error')) {
        errorMessage = 'Network connection lost. Please check your connection and try again.';
      }
      
      Alert.alert(
        'Error', 
        `${errorMessage}\n\nError: ${error.message}`,
        [
          { text: 'Retry', onPress: loadCapsule },
          { text: 'Go Back', onPress: () => navigation.goBack() }
        ]
      );
    } finally {
      setLoading(false);
    }
  };

  const renderCapsuleItem = (item, index) => (
    <View key={index} style={styles.itemCard}>
      <View style={styles.itemPlaceholder}>
        {item.imageUrl ? (
          <Image 
            source={{ uri: item.imageUrl }} 
            style={styles.itemImage}
            resizeMode="cover"
          />
        ) : (
          <>
            <Text style={styles.itemType}>{item.articleType}</Text>
            <Text style={styles.itemBrand}>{item.productDisplayName}</Text>
          </>
        )}
      </View>
      <View style={styles.itemDetails}>
        <Text style={styles.itemName}>{item.subCategory}</Text>
        <Text style={styles.itemColor}>{item.baseColour}</Text>
        <Text style={styles.itemUsage}>{item.usage}</Text>
        {item.explanation && (
          <Text style={styles.explanation}>{item.explanation}</Text>
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

  if (!capsuleData) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.errorText}>Failed to load capsule data</Text>
        <TouchableOpacity style={styles.retryButton} onPress={loadCapsule}>
          <Text style={styles.retryButtonText}>Retry</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        {/* Header Stats */}
        <View style={styles.statsContainer}>
          <View style={styles.statCard}>
            <Text style={styles.statNumber}>{capsuleData.capsule_items?.length || 0}</Text>
            <Text style={styles.statLabel}>Items</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statNumber}>{capsuleData.outfits_possible || 0}</Text>
            <Text style={styles.statLabel}>Outfits</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statNumber}>{capsuleData.optimization_stats?.categories_covered || 0}</Text>
            <Text style={styles.statLabel}>Categories</Text>
          </View>
        </View>

        {/* Capsule Items */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Your Capsule Wardrobe</Text>
          {capsuleData.capsule_items?.map((item, index) => renderCapsuleItem(item, index))}
        </View>

        {/* Action Buttons */}
        <View style={styles.buttonContainer}>
          <TouchableOpacity 
            style={styles.primaryButton}
            onPress={() => navigation.navigate('Quiz')}
          >
            <Text style={styles.primaryButtonText}>Take Quiz Again</Text>
          </TouchableOpacity>
          
          <TouchableOpacity 
            style={styles.secondaryButton}
            onPress={() => navigation.navigate('Welcome')}
          >
            <Text style={styles.secondaryButtonText}>Start Over</Text>
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
    textAlign: 'center',
  },
  errorText: {
    fontSize: 16,
    color: '#e74c3c',
    textAlign: 'center',
    marginBottom: 20,
  },
  retryButton: {
    backgroundColor: '#667eea',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
  },
  retryButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  content: {
    padding: 20,
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 30,
  },
  statCard: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 12,
    alignItems: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    minWidth: 80,
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#667eea',
    marginBottom: 4,
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    textAlign: 'center',
  },
  section: {
    marginBottom: 30,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 16,
  },
  itemCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
  },
  itemImage: {
    width: '100%',
    height: 120,
    borderRadius: 8,
    backgroundColor: '#f8f9fa',
  },
  itemPlaceholder: {
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
    padding: 20,
    alignItems: 'center',
    marginBottom: 12,
    borderWidth: 2,
    borderColor: '#e9ecef',
    borderStyle: 'dashed',
  },
  itemType: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#667eea',
    marginBottom: 4,
  },
  itemBrand: {
    fontSize: 12,
    color: '#666',
    textAlign: 'center',
  },
  itemDetails: {
    alignItems: 'center',
  },
  itemName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 4,
  },
  itemColor: {
    fontSize: 14,
    color: '#667eea',
    marginBottom: 2,
  },
  itemUsage: {
    fontSize: 12,
    color: '#666',
    fontStyle: 'italic',
    marginBottom: 8,
  },
  explanation: {
    fontSize: 12,
    color: '#27ae60',
    textAlign: 'center',
    fontStyle: 'italic',
  },
  buttonContainer: {
    gap: 12,
    marginTop: 20,
  },
  primaryButton: {
    backgroundColor: '#667eea',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  primaryButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  secondaryButton: {
    backgroundColor: '#fff',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#667eea',
  },
  secondaryButtonText: {
    color: '#667eea',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default SimpleCapsuleScreen;
