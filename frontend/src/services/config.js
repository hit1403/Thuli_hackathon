import { Platform } from 'react-native';

// Network configuration for React Native - Robust multi-scenario support
export const BACKEND_PORT = 8001;

// Comprehensive IP addresses for different network scenarios
export const API_CONFIG = {
  // Emulator/Simulator URLs
  ANDROID_EMULATOR: 'http://10.0.2.2:8001',
  IOS_SIMULATOR: 'http://localhost:8001',
  
  // Common hotspot IP ranges
  MOBILE_HOTSPOT_RANGES: [
    'http://192.168.43.1:8001',    // Android hotspot default
    'http://172.20.10.1:8001',     // iPhone hotspot default
    'http://192.168.137.1:8001',   // Windows hotspot default
    'http://10.241.153.6:8001',    // Current mobile hotspot IP
  ],
  
  // Common WiFi IP ranges
  WIFI_RANGES: [
    'http://10.1.232.94:8001',     // Current WiFi IP
    'http://192.168.1.100:8001',   // Common router range
    'http://192.168.0.100:8001',   // Common router range
    'http://10.0.0.100:8001',      // Common router range
  ],
  
  // Localhost variants
  LOCALHOST_VARIANTS: [
    'http://localhost:8001',
    'http://127.0.0.1:8001',
  ],
  
  // Production URL
  PRODUCTION: 'http://your-production-url.com',
};

// Get the appropriate base URL with intelligent fallback
export const getBaseURL = () => {
  if (__DEV__) {
    // For development, we'll use the connection testing to find the working URL
    return API_CONFIG.WORKING_URL || 'http://10.241.153.6:8001';
  }
  return API_CONFIG.PRODUCTION;
};

// Comprehensive connection testing for all scenarios
export const testConnection = async () => {
  // Build comprehensive list of URLs to try
  const urlsToTry = [
    // Current known IPs first (most likely to work)
    'http://10.241.153.6:8001',    // Current mobile hotspot
    'http://10.1.232.94:8001',
    'http://10.173.129.6:8001',     // Current WiFi
    
    // Common hotspot IPs
    ...API_CONFIG.MOBILE_HOTSPOT_RANGES,
    
    // Localhost variants
    ...API_CONFIG.LOCALHOST_VARIANTS,
    
    // Common WiFi ranges
    ...API_CONFIG.WIFI_RANGES,
    
    // Emulator/Simulator
    API_CONFIG.ANDROID_EMULATOR,
    API_CONFIG.IOS_SIMULATOR,
  ];

  // Remove duplicates
  const uniqueUrls = [...new Set(urlsToTry)];
  
  console.log(`🔍 Testing ${uniqueUrls.length} possible backend URLs...`);
  
  for (const baseURL of uniqueUrls) {
    console.log(`Testing connection to: ${baseURL}`);
    
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 3000);
      
      const response = await fetch(`${baseURL}/quiz/items?count=1`, {
        method: 'GET',
        signal: controller.signal,
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
      });
      
      clearTimeout(timeoutId);
      
      if (response.ok) {
        const data = await response.json();
        console.log(`✅ Backend connection successful at: ${baseURL}`);
        console.log(`📊 Received ${data.items?.length || 0} quiz items`);
        
        // Store the working URL for future use
        API_CONFIG.WORKING_URL = baseURL;
        return { success: true, url: baseURL, data };
      } else {
        console.log(`❌ ${baseURL} responded with status: ${response.status}`);
      }
    } catch (error) {
      if (error.name === 'AbortError') {
        console.log(`⏰ ${baseURL} timed out (3s)`);
      } else {
        console.log(`❌ ${baseURL} failed: ${error.message}`);
      }
    }
  }
  
  console.log('🚨 All backend connection attempts failed');
  return { 
    success: false, 
    error: 'Cannot connect to backend server. Please ensure:\n1. Backend is running on port 8001\n2. Both devices are on same network\n3. Firewall allows connections',
    url: null 
  };
};
