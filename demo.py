#!/usr/bin/env python3
"""
Energetic Backend Demo Script
Demonstrates the API functionality and usage examples
"""

import asyncio
import json
import websockets
import requests
import time
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000"

class EnergeticBackendDemo:
    """Demo class for testing the Energetic Backend"""
    
    def __init__(self):
        self.session_id = None
        self.ws_connection = None
    
    def test_health_endpoint(self):
        """Test the health check endpoint"""
        print("🏥 Testing health endpoint...")
        try:
            response = requests.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print("✅ Health check passed:", response.json())
                return True
            else:
                print("❌ Health check failed:", response.status_code)
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def test_api_health(self):
        """Test the API health endpoint"""
        print("🔌 Testing API health...")
        try:
            response = requests.get(f"{BASE_URL}/api/v1/health")
            if response.status_code == 200:
                print("✅ API health check passed:", response.json())
                return True
            else:
                print("❌ API health check failed:", response.status_code)
                return False
        except Exception as e:
            print(f"❌ API health check error: {e}")
            return False
    
    def create_session(self, title: str) -> bool:
        """Create a new session"""
        print(f"📝 Creating session: {title}")
        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/sessions/",
                json={
                    "title": title,
                    "system_prompt": None,
                    "model_name": None,
                    "tool_version": None
                }
            )
            
            if response.status_code == 200:
                session_data = response.json()
                self.session_id = session_data["session_id"]
                print(f"✅ Session created: {self.session_id}")
                return True
            else:
                print(f"❌ Session creation failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Session creation error: {e}")
            return False
    
    def list_sessions(self):
        """List all sessions"""
        print("📋 Listing sessions...")
        try:
            response = requests.get(f"{BASE_URL}/api/v1/sessions/")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Found {data['total']} sessions:")
                for session in data['sessions']:
                    print(f"   • {session['title']} ({session['status']}) - {session['session_id']}")
                return True
            else:
                print(f"❌ List sessions failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ List sessions error: {e}")
            return False
    
    async def connect_websocket(self):
        """Connect to WebSocket for real-time communication"""
        if not self.session_id:
            print("❌ No session ID available")
            return False
        
        print(f"🔌 Connecting to WebSocket: {self.session_id}")
        try:
            self.ws_connection = await websockets.connect(
                f"{WS_URL}/ws/chat/{self.session_id}"
            )
            print("✅ WebSocket connected")
            return True
        except Exception as e:
            print(f"❌ WebSocket connection error: {e}")
            return False
    
    async def send_message(self, message: str):
        """Send a message via WebSocket"""
        if not self.ws_connection:
            print("❌ WebSocket not connected")
            return
        
        print(f"💬 Sending message: {message}")
        try:
            await self.ws_connection.send(json.dumps({
                "type": "chat",
                "data": {"message": message}
            }))
            print("✅ Message sent")
        except Exception as e:
            print(f"❌ Message send error: {e}")
    
    async def listen_for_responses(self, timeout: int = 30):
        """Listen for responses from the agent"""
        if not self.ws_connection:
            print("❌ WebSocket not connected")
            return
        
        print(f"👂 Listening for responses (timeout: {timeout}s)...")
        start_time = time.time()
        
        try:
            while time.time() - start_time < timeout:
                try:
                    message = await asyncio.wait_for(
                        self.ws_connection.recv(), 
                        timeout=1.0
                    )
                    data = json.loads(message)
                    print(f"📨 Received: {data['type']} - {data.get('data', {})}")
                    
                    # Check if task is complete
                    if data['type'] == 'complete':
                        print("🎉 Task completed!")
                        break
                    elif data['type'] == 'error':
                        print(f"❌ Error received: {data['data']}")
                        break
                        
                except asyncio.TimeoutError:
                    continue
                    
        except Exception as e:
            print(f"❌ Response listening error: {e}")
    
    async def demo_weather_search(self, city: str):
        """Demonstrate weather search functionality"""
        print(f"\n🌤️  Demo: Searching weather in {city}")
        print("=" * 50)
        
        # Create session
        if not self.create_session(f"Search weather in {city}"):
            return False
        
        # Connect WebSocket
        if not await self.connect_websocket():
            return False
        
        # Send message
        await self.send_message(f"Search the weather in {city}")
        
        # Listen for responses
        await self.listen_for_responses(timeout=60)
        
        # Close WebSocket
        if self.ws_connection:
            await self.ws_connection.close()
            self.ws_connection = None
        
        print(f"✅ Weather search demo for {city} completed")
        return True
    
    def get_session_status(self):
        """Get current session status"""
        if not self.session_id:
            print("❌ No session ID available")
            return
        
        print(f"📊 Getting session status: {self.session_id}")
        try:
            response = requests.get(f"{BASE_URL}/api/v1/sessions/{self.session_id}/status")
            if response.status_code == 200:
                status = response.json()
                print(f"✅ Session status: {status}")
                return status
            else:
                print(f"❌ Status check failed: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Status check error: {e}")
            return None
    
    def close_session(self):
        """Close the current session"""
        if not self.session_id:
            print("❌ No session ID available")
            return
        
        print(f"🔒 Closing session: {self.session_id}")
        try:
            response = requests.delete(f"{BASE_URL}/api/v1/sessions/{self.session_id}")
            if response.status_code == 200:
                print("✅ Session closed")
                self.session_id = None
            else:
                print(f"❌ Session close failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Session close error: {e}")


async def main():
    """Main demo function"""
    print("🚀 Energetic Backend Demo")
    print("=" * 50)
    
    demo = EnergeticBackendDemo()
    
    # Test basic endpoints
    if not demo.test_health_endpoint():
        print("❌ Health check failed. Is the backend running?")
        return
    
    if not demo.test_api_health():
        print("❌ API health check failed.")
        return
    
    # List existing sessions
    demo.list_sessions()
    
    # Demo 1: Search weather in Dubai
    await demo.demo_weather_search("Dubai")
    
    # Wait a bit between demos
    print("\n⏳ Waiting 5 seconds before next demo...")
    await asyncio.sleep(5)
    
    # Demo 2: Search weather in San Francisco
    await demo.demo_weather_search("San Francisco")
    
    # List sessions again to show history
    print("\n📋 Final session list:")
    demo.list_sessions()
    
    # Get status of last session
    demo.get_session_status()
    
    # Close the session
    demo.close_session()
    
    print("\n🎉 Demo completed successfully!")
    print("\n💡 Tips:")
    print("   • Check the frontend at http://localhost:8000")
    print("   • View API docs at http://localhost:8000/api/docs")
    print("   • Monitor logs with: docker-compose logs -f backend")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("Make sure the backend is running with: ./start.sh")
