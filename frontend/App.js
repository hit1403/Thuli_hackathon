import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet } from 'react-native';

// Import screens
import WelcomeScreen from './src/screens/WelcomeScreen';
import QuizScreen from './src/screens/QuizScreen';
import SimpleCapsuleScreen from './src/screens/SimpleCapsuleScreen';
import ProfileScreen from './src/screens/ProfileScreen';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <StatusBar style="auto" />
      <Stack.Navigator 
        initialRouteName="Welcome"
        screenOptions={{
          headerStyle: {
            backgroundColor: '#2c3e50',
          },
          headerTintColor: '#fff',
          headerTitleStyle: {
            fontWeight: 'bold',
          },
        }}
      >
        <Stack.Screen 
          name="Welcome" 
          component={WelcomeScreen} 
          options={{ headerShown: false }}
        />
        <Stack.Screen 
          name="Quiz" 
          component={QuizScreen} 
          options={{ title: 'Style Quiz' }}
        />
        <Stack.Screen 
          name="Profile" 
          component={ProfileScreen} 
          options={{ title: 'Your Style Profile' }}
        />
        <Stack.Screen 
          name="Capsule" 
          component={SimpleCapsuleScreen} 
          options={{ title: 'Your Capsule Wardrobe' }} 
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
});
