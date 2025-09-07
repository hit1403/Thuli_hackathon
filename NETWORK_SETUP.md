# React Native Network Setup Guide

## The Problem
React Native apps cannot connect to `localhost` because they run in a different network context than your computer.

## Solutions by Platform

### 🤖 Android Emulator
- **Use**: `http://10.0.2.2:8000`
- **Why**: Android emulator maps `10.0.2.2` to the host machine's `localhost`

### 📱 iOS Simulator
- **Use**: `http://localhost:8000`
- **Why**: iOS simulator shares the same network as the host machine

### 📲 Physical Device (Android/iOS)
- **Use**: `http://YOUR_COMPUTER_IP:8000`
- **Find your IP**:
  - Windows: Run `ipconfig` in Command Prompt
  - Mac/Linux: Run `ifconfig` in Terminal
  - Look for your WiFi adapter's IPv4 address (e.g., 192.168.1.100)

## Current Configuration
The app is currently configured to automatically detect your platform and use the appropriate URL:

- ✅ Android Emulator: `http://10.0.2.2:8000`
- ✅ iOS Simulator: `http://localhost:8000`
- ❌ Physical Device: Needs your computer's IP address

## Quick Fix for Physical Device

1. **Find your computer's IP address**:
   ```bash
   # Windows
   ipconfig
   
   # Mac/Linux
   ifconfig
   ```

2. **Update the configuration**:
   Edit `frontend/src/services/config.js` and replace:
   ```javascript
   PHYSICAL_DEVICE: 'http://192.168.1.100:8000', // Replace with your actual IP
   ```

3. **Make sure both devices are on the same WiFi network**

## Troubleshooting Steps

### 1. Check Backend Server
- Ensure backend is running: `python run_simple.py`
- Test in browser: Visit `http://localhost:8000`
- Should see: `{"message": "Style Quiz Backend is running 🚀"}`

### 2. Check Network Connectivity
- Both computer and device must be on same WiFi
- Firewall might be blocking port 8000
- Try disabling firewall temporarily

### 3. Test Connection
The app will automatically test the connection and show detailed error messages.

### 4. Alternative Ports
If port 8000 is blocked, modify `backend/run_simple.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8080)  # Try port 8080
```

## Common Errors and Solutions

| Error | Solution |
|-------|----------|
| "Network Error" | Check IP address configuration |
| "Connection refused" | Backend server not running |
| "Timeout" | Firewall blocking connection |
| "ECONNRESET" | Network connectivity issue |

## Testing Your Setup

1. Start the backend server
2. Open the React Native app
3. Check the console logs for connection details
4. The app will show specific error messages if connection fails
