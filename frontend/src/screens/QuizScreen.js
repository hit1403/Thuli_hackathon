import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
  ActivityIndicator,
  Alert,
  ScrollView,
  Dimensions,
  Image,
} from 'react-native';
import { apiService, updateApiBaseURL } from '../services/api';
import { testConnection } from '../services/config';

const { width } = Dimensions.get('window');

const QuizScreen = ({ navigation }) => {
  const [quizItems, setQuizItems] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [feedback, setFeedback] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadQuizItems();
  }, []);

  const loadQuizItems = async () => {
    try {
      setLoading(true);
      
      const checkBackendConnection = async () => {
        console.log('🔍 Testing backend connection...');
        const result = await testConnection();
        
        if (!result.success) {
          Alert.alert(
            'Connection Error',
            result.error,
            [
              { text: 'Retry', onPress: () => loadQuizItems() },
              { text: 'Cancel', onPress: () => navigation.goBack() }
            ]
          );
          return false;
        } else {
          // Update API service to use the working URL
          updateApiBaseURL(result.url);
          console.log(`✅ Using working backend URL: ${result.url}`);
          return true;
        }
      };

      if (await checkBackendConnection()) {
        console.log('Backend connection successful, loading quiz items...');
        const data = await apiService.getQuizItems(20);
        setQuizItems(data.items);
        console.log(`Loaded ${data.items.length} quiz items`);
      }
    } catch (error) {
      console.error('Error fetching quiz items:', error);
      Alert.alert(
        'Error', 
        `Failed to load quiz items.\n\nError: ${error.message}\n\nPlease check your network connection and try again.`,
        [
          { text: 'Retry', onPress: loadQuizItems },
          { text: 'Cancel', style: 'cancel' }
        ]
      );
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = (liked) => {
    const currentItem = quizItems[currentIndex];
    const newFeedback = [...feedback, { item_id: currentItem.id, liked }];
    setFeedback(newFeedback);

    if (currentIndex < quizItems.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      submitQuiz(newFeedback);
    }
  };

  const submitQuiz = async (finalFeedback) => {
    try {
      setSubmitting(true);
      const result = await apiService.submitQuizFeedback(finalFeedback);
      
      // Navigate to profile screen with results
      navigation.navigate('Profile', { 
        profile: result.profile, 
        likedIds: result.liked_ids 
      });
    } catch (error) {
      Alert.alert('Error', 'Failed to submit quiz. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const currentItem = quizItems[currentIndex];
  const progress = ((currentIndex + 1) / quizItems.length) * 100;

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#667eea" />
        <Text style={styles.loadingText}>Loading style quiz...</Text>
      </View>
    );
  }

  if (submitting) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#667eea" />
        <Text style={styles.loadingText}>Analyzing your style...</Text>
      </View>
    );
  }

  if (!currentItem) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.errorText}>No quiz items available</Text>
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <View style={styles.progressContainer}>
          <View style={styles.progressBar}>
            <View style={[styles.progressFill, { width: `${progress}%` }]} />
          </View>
          <Text style={styles.progressText}>
            {currentIndex + 1} of {quizItems.length}
          </Text>
        </View>
      </View>

      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.itemContainer}>
          <View style={styles.imageContainer}>
            {currentItem.imageUrl ? (
              <Image 
                source={{ uri: currentItem.imageUrl }} 
                style={styles.itemImage}
                resizeMode="cover"
              />
            ) : (
              <View style={styles.imagePlaceholder}>
                <Text style={styles.imagePlaceholderText}>
                  {currentItem.articleType}
                </Text>
                <Text style={styles.brandText}>
                  {currentItem.productDisplayName}
                </Text>
              </View>
            )}
          </View>
          
          <View style={styles.itemInfo}>
            <Text style={styles.itemTitle}>{currentItem.productDisplayName}</Text>
            <Text style={styles.itemDetails}>
              {currentItem.articleType} • {currentItem.baseColour} • {currentItem.usage}
            </Text>
            <Text style={styles.itemCategory}>{currentItem.subCategory}</Text>
          </View>

          <View style={styles.buttonContainer}>
            <TouchableOpacity
              style={[styles.button, styles.dislikeButton]}
              onPress={() => handleFeedback(false)}
            >
              <Text style={styles.buttonText}>👎 Pass</Text>
            </TouchableOpacity>
            
            <TouchableOpacity
              style={[styles.button, styles.likeButton]}
              onPress={() => handleFeedback(true)}
            >
              <Text style={styles.buttonText}>👍 Like</Text>
            </TouchableOpacity>
          </View>
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
  },
  errorText: {
    fontSize: 16,
    color: '#e74c3c',
  },
  header: {
    padding: 20,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e9ecef',
  },
  progressContainer: {
    alignItems: 'center',
  },
  progressBar: {
    width: '100%',
    height: 8,
    backgroundColor: '#e9ecef',
    borderRadius: 4,
    marginBottom: 8,
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#667eea',
    borderRadius: 4,
  },
  progressText: {
    fontSize: 14,
    color: '#666',
    fontWeight: '500',
  },
  content: {
    flexGrow: 1,
    padding: 20,
  },
  itemContainer: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 20,
    marginBottom: 20,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
  },
  imageContainer: {
    alignItems: 'center',
    marginBottom: 20,
  },
  itemImage: {
    width: width * 0.6,
    height: width * 0.6,
    borderRadius: 12,
    backgroundColor: '#f8f9fa',
  },
  imagePlaceholder: {
    width: width * 0.6,
    height: width * 0.6,
    backgroundColor: '#f8f9fa',
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#e9ecef',
    borderStyle: 'dashed',
  },
  imagePlaceholderText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#667eea',
    textAlign: 'center',
    marginBottom: 8,
  },
  brandText: {
    fontSize: 12,
    color: '#666',
    textAlign: 'center',
    paddingHorizontal: 10,
  },
  itemDetails: {
    alignItems: 'center',
  },
  itemName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 8,
  },
  itemCategory: {
    fontSize: 16,
    color: '#667eea',
    marginBottom: 4,
  },
  itemUsage: {
    fontSize: 14,
    color: '#666',
    fontStyle: 'italic',
  },
  questionContainer: {
    alignItems: 'center',
    marginVertical: 20,
  },
  questionText: {
    fontSize: 20,
    fontWeight: '600',
    color: '#2c3e50',
    textAlign: 'center',
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 20,
    gap: 15,
  },
  button: {
    flex: 1,
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
  },
  likeButton: {
    backgroundColor: '#27ae60',
  },
  dislikeButton: {
    backgroundColor: '#e74c3c',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default QuizScreen;
