#!/usr/bin/env python3
"""
Test script for the Message in a Bottle API
"""

import requests
import json

def test_collect_bottles():
    """Test the /collect-bottles endpoint with sample data"""
    
    # Sample bottle data
    bottles = [
        {"character": "H", "coordinates": {"x": 0, "y": 0}},
        {"character": "e", "coordinates": {"x": 1, "y": 0}},
        {"character": "l", "coordinates": {"x": 2, "y": 0}},
        {"character": "l", "coordinates": {"x": 3, "y": 0}},
        {"character": "o", "coordinates": {"x": 4, "y": 0}},
        {"character": "W", "coordinates": {"x": 0, "y": 1}},
        {"character": "o", "coordinates": {"x": 1, "y": 1}},
        {"character": "r", "coordinates": {"x": 2, "y": 1}},
        {"character": "l", "coordinates": {"x": 3, "y": 1}},
        {"character": "d", "coordinates": {"x": 4, "y": 1}}
    ]
    
    try:
        # Make the request
        response = requests.post(
            "http://localhost:8080/collect-bottles",
            json=bottles,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Test passed!")
            print(f"Message: {result['message']}")
        else:
            print(f"❌ Test failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

def test_health_endpoints():
    """Test the health check endpoints"""
    
    try:
        # Test root endpoint
        response = requests.get("http://localhost:8080/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            
        # Test health endpoint
        response = requests.get("http://localhost:8080/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the application is running on localhost:8080")
    except Exception as e:
        print(f"❌ Health test failed with error: {str(e)}")

if __name__ == "__main__":
    print("Testing Message in a Bottle API...")
    print("=" * 40)
    
    test_health_endpoints()
    print()
    test_collect_bottles() 