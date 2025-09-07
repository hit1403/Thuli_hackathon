import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  Dimensions,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

const { width, height } = Dimensions.get('window');

const WelcomeScreen = ({ navigation }) => {
  return (
    <SafeAreaView style={styles.container}>
      <LinearGradient
        colors={['#667eea', '#764ba2']}
        style={styles.gradient}
      >
        <View style={styles.content}>
          <View style={styles.header}>
            <Text style={styles.title}>StyleGenius</Text>
            <Text style={styles.subtitle}>AI-Powered Fashion Recommendations</Text>
          </View>

          <View style={styles.features}>
            <View style={styles.featureItem}>
              <Text style={styles.featureIcon}>🎯</Text>
              <Text style={styles.featureText}>Personalized Style Quiz</Text>
            </View>
            <View style={styles.featureItem}>
              <Text style={styles.featureIcon}>👗</Text>
              <Text style={styles.featureText}>Smart Capsule Wardrobe</Text>
            </View>
            <View style={styles.featureItem}>
              <Text style={styles.featureIcon}>✨</Text>
              <Text style={styles.featureText}>Serendipity Slider</Text>
            </View>
          </View>

          <View style={styles.buttonContainer}>
            <TouchableOpacity
              style={styles.startButton}
              onPress={() => navigation.navigate('Quiz')}
            >
              <Text style={styles.buttonText}>Start Style Quiz</Text>
            </TouchableOpacity>
            
            <Text style={styles.description}>
              Discover your unique style personality and get personalized fashion recommendations
            </Text>
          </View>
        </View>
      </LinearGradient>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  gradient: {
    flex: 1,
  },
  content: {
    flex: 1,
    justifyContent: 'space-between',
    paddingHorizontal: 30,
    paddingVertical: 50,
  },
  header: {
    alignItems: 'center',
    marginTop: 60,
  },
  title: {
    fontSize: 42,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 18,
    color: '#f8f9fa',
    textAlign: 'center',
    opacity: 0.9,
  },
  features: {
    marginVertical: 40,
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginVertical: 15,
    paddingHorizontal: 20,
  },
  featureIcon: {
    fontSize: 24,
    marginRight: 15,
  },
  featureText: {
    fontSize: 18,
    color: '#fff',
    fontWeight: '500',
  },
  buttonContainer: {
    alignItems: 'center',
  },
  startButton: {
    backgroundColor: '#fff',
    paddingVertical: 18,
    paddingHorizontal: 50,
    borderRadius: 30,
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    marginBottom: 20,
  },
  buttonText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#667eea',
  },
  description: {
    fontSize: 16,
    color: '#f8f9fa',
    textAlign: 'center',
    opacity: 0.8,
    lineHeight: 24,
  },
});

export default WelcomeScreen;
