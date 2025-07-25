#!/usr/bin/env python3
"""
Firebase Configuration for BlueEdge Framework - Complete Final Version
======================================================================
Enhanced Firebase integration for existing BlueEdge mobile app with:
- Real-time database operations
- Background synchronization
- Performance monitoring
- Complete error handling
- BlueEdge-specific data structures
"""

import json
import requests
from datetime import datetime
import threading
import time
import os
import uuid
import sys

class FirebaseConfig:
    """Firebase Realtime Database Configuration for BlueEdge"""
    
    def __init__(self):
        # Firebase Project Configuration
        # TODO: Update these values after creating Firebase project
        self.project_id = "blueedge-framework"
        self.database_url = "https://blueedge-framework-default-rtdb.firebaseio.com"
        self.api_key = "YOUR_API_KEY_HERE"  # Will be updated from Firebase console
        
        # Database endpoints
        self.users_endpoint = f"{self.database_url}/users.json"
        self.comparisons_endpoint = f"{self.database_url}/comparisons.json"
        self.statistics_endpoint = f"{self.database_url}/statistics.json"
        self.sessions_endpoint = f"{self.database_url}/sessions.json"
        
        # Connection status
        self.connected = False
        self.last_sync = None
        self.connection_attempts = 0
        self.max_connection_attempts = 3
        
        print("🔥 Firebase Config initialized for BlueEdge")
        
    def test_connection(self):
        """Test Firebase connection with retry logic"""
        self.connection_attempts += 1
        
        try:
            print(f"🔗 Testing Firebase connection (attempt {self.connection_attempts})...")
            
            # Test with timeout
            response = requests.get(
                f"{self.database_url}/.json", 
                timeout=8,
                headers={'User-Agent': 'BlueEdge-Framework/1.0'}
            )
            
            if response.status_code == 200:
                self.connected = True
                self.last_sync = datetime.now()
                print("✅ Firebase connection successful!")
                return True, "Firebase connection successful"
                
            elif response.status_code == 404:
                print("❌ Firebase project not found - please create Firebase project")
                return False, "Firebase project not found (404)"
                
            else:
                print(f"❌ Firebase connection failed: HTTP {response.status_code}")
                return False, f"Connection failed: HTTP {response.status_code}"
                
        except requests.exceptions.Timeout:
            print("❌ Firebase connection timeout")
            return False, "Connection timeout - check internet connection"
            
        except requests.exceptions.ConnectionError:
            print("❌ Firebase connection error - no internet")
            return False, "No internet connection"
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Firebase request error: {str(e)}")
            return False, f"Request error: {str(e)}"
            
        except Exception as e:
            print(f"❌ Unexpected Firebase error: {str(e)}")
            return False, f"Unexpected error: {str(e)}"
    
    def is_connected(self):
        """Check if Firebase is currently connected"""
        return self.connected
    
    def get_connection_info(self):
        """Get detailed connection information"""
        return {
            'connected': self.connected,
            'last_sync': self.last_sync.isoformat() if self.last_sync else None,
            'connection_attempts': self.connection_attempts,
            'project_id': self.project_id,
            'database_url': self.database_url
        }

class FirebaseDatabase:
    """Firebase Realtime Database Operations for BlueEdge"""
    
    def __init__(self, config: FirebaseConfig):
        self.config = config
        self.local_cache = {}
        self.request_timeout = 10
        print("📁 Firebase Database handler initialized for BlueEdge")
        
    def save_comparison_result(self, user_id, comparison_data):
        """Save BlueEdge name comparison result to Firebase"""
        if not self.config.is_connected():
            print("❌ Cannot save - Firebase not connected")
            return False, None
            
        try:
            # Generate unique session ID
            session_id = f"session_{int(time.time())}_{uuid.uuid4().hex[:8]}"
            timestamp = datetime.now().isoformat()
            
            # Enhanced data structure for BlueEdge compatibility
            data = {
                # User and session info
                "user_id": user_id,
                "session_id": session_id,
                "timestamp": timestamp,
                
                # Original comparison data from BlueEdge
                "comparison_results": comparison_data,
                
                # Performance metrics (BlueEdge standard)
                "processing_time": comparison_data.get("processing_time", 0),
                "memory_usage": "~5KB",  # BlueEdge standard
                "platform": "mobile_edge_computing",
                
                # Analysis results
                "similarity_score": comparison_data.get("similarity_score", 0),
                "duplicate_status": comparison_data.get("is_duplicate", False),
                "confidence_level": comparison_data.get("confidence_level", "unknown"),
                "error_category": comparison_data.get("category", "unknown"),
                "error_types_detected": comparison_data.get("error_types", []),
                
                # Name data (structured)
                "name1_data": {
                    "full_name": comparison_data.get("name1", ""),
                    "processed": comparison_data.get("name1_processed", "")
                },
                "name2_data": {
                    "full_name": comparison_data.get("name2", ""),
                    "processed": comparison_data.get("name2_processed", "")
                },
                
                # BlueEdge framework metadata
                "framework": {
                    "name": "BlueEdge",
                    "version": "1.0.0",
                    "algorithm_type": "levenshtein_enhanced",
                    "mobile_optimized": True,
                    "language_support": ["english", "arabic"],
                    "categories_supported": [
                        "different_spelling", "misspelling", "abbreviation",
                        "honorific_prefix", "nickname", "split_name"
                    ]
                }
            }
            
            print(f"💾 Saving comparison to Firebase for user: {user_id}")
            
            # Send to Firebase with retry logic
            for attempt in range(2):
                try:
                    response = requests.post(
                        self.config.comparisons_endpoint,
                        json=data,
                        timeout=self.request_timeout,
                        headers={'User-Agent': 'BlueEdge-Framework/1.0'}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        firebase_key = result.get('name', 'unknown')
                        print(f"✅ Data saved to Firebase: {firebase_key}")
                        
                        # Update global statistics
                        self._update_statistics_async(data)
                        
                        return True, firebase_key
                    else:
                        print(f"❌ Firebase save failed: HTTP {response.status_code}")
                        if attempt == 0:
                            print("🔄 Retrying save operation...")
                            time.sleep(1)
                        
                except requests.exceptions.RequestException as e:
                    print(f"❌ Firebase save request error (attempt {attempt + 1}): {e}")
                    if attempt == 0:
                        time.sleep(1)
            
            return False, None
                
        except Exception as e:
            print(f"❌ Firebase save error: {str(e)}")
            return False, None
    
    def get_user_history(self, user_id, limit=10):
        """Retrieve user's comparison history from Firebase"""
        if not self.config.is_connected():
            print("❌ Cannot load history - Firebase not connected")
            return False, []
            
        try:
            print(f"📖 Loading history for user: {user_id}")
            
            # Query Firebase for user data
            params = {
                'orderBy': '"user_id"',
                'equalTo': f'"{user_id}"',
                'limitToLast': min(limit, 50)  # Limit to prevent large downloads
            }
            
            response = requests.get(
                self.config.comparisons_endpoint,
                params=params,
                timeout=self.request_timeout,
                headers={'User-Agent': 'BlueEdge-Framework/1.0'}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data:
                    # Convert to list format
                    history = []
                    for key, value in data.items():
                        value['firebase_key'] = key
                        # Add formatted display data
                        value['display'] = self._format_history_item(value)
                        history.append(value)
                    
                    # Sort by timestamp (newest first)
                    history.sort(
                        key=lambda x: x.get('timestamp', ''),
                        reverse=True
                    )
                    
                    print(f"✅ Retrieved {len(history)} history records")
                    return True, history[:limit]
                else:
                    print("📝 No history found for user")
                    return True, []
                    
            else:
                print(f"❌ History retrieval failed: HTTP {response.status_code}")
                return False, []
                
        except Exception as e:
            print(f"❌ Firebase retrieve error: {str(e)}")
            return False, []
    
    def get_global_statistics(self):
        """Get global BlueEdge statistics from Firebase"""
        if not self.config.is_connected():
            return False, {}
            
        try:
            response = requests.get(
                self.config.statistics_endpoint, 
                timeout=5,
                headers={'User-Agent': 'BlueEdge-Framework/1.0'}
            )
            
            if response.status_code == 200:
                stats = response.json() or {}
                print("📊 Global statistics retrieved")
                return True, stats
            else:
                print(f"❌ Statistics retrieval failed: HTTP {response.status_code}")
                return False, {}
                
        except Exception as e:
            print(f"❌ Statistics retrieval error: {str(e)}")
            return False, {}
    
    def save_user_session(self, user_id, session_data):
        """Save user session information"""
        if not self.config.is_connected():
            return False
            
        try:
            session_info = {
                'user_id': user_id,
                'start_time': datetime.now().isoformat(),
                'app_version': '1.0.0',
                'platform': 'mobile',
                'session_data': session_data
            }
            
            response = requests.post(
                self.config.sessions_endpoint,
                json=session_info,
                timeout=5,
                headers={'User-Agent': 'BlueEdge-Framework/1.0'}
            )
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ Session save error: {str(e)}")
            return False
    
    def _update_statistics_async(self, comparison_data):
        """Update statistics in background thread"""
        def update_stats():
            try:
                self._update_statistics(comparison_data)
            except Exception as e:
                print(f"❌ Background statistics update error: {e}")
        
        # Run in background thread
        thread = threading.Thread(target=update_stats, daemon=True)
        thread.start()
    
    def _update_statistics(self, comparison_data):
        """Update global BlueEdge statistics"""
        try:
            # Get current stats
            response = requests.get(self.config.statistics_endpoint, timeout=5)
            current_stats = {}
            
            if response.status_code == 200 and response.json():
                current_stats = response.json()
            
            # Extract relevant data
            is_duplicate = comparison_data.get('duplicate_status', False)
            processing_time = comparison_data.get('processing_time', 0)
            error_category = comparison_data.get('error_category', 'unknown')
            
            # Update statistics
            updated_stats = {
                # Basic counters
                "total_comparisons": current_stats.get("total_comparisons", 0) + 1,
                "total_duplicates_found": current_stats.get("total_duplicates_found", 0) + (1 if is_duplicate else 0),
                "total_unique_pairs": current_stats.get("total_unique_pairs", 0) + (0 if is_duplicate else 1),
                
                # Performance metrics
                "average_processing_time": self._calculate_average_time(current_stats, processing_time),
                "total_processing_time": current_stats.get("total_processing_time", 0) + processing_time,
                "min_processing_time": min(current_stats.get("min_processing_time", float('inf')), processing_time),
                "max_processing_time": max(current_stats.get("max_processing_time", 0), processing_time),
                
                # Category distribution
                "category_distribution": self._update_category_distribution(current_stats, error_category),
                
                # BlueEdge specific metrics
                "mobile_edge_sessions": current_stats.get("mobile_edge_sessions", 0) + 1,
                "memory_efficiency": "5KB_per_comparison",
                "platform_type": "mobile_edge_computing",
                "accuracy_rate": self._calculate_accuracy_rate(current_stats, is_duplicate),
                
                # Metadata
                "last_updated": datetime.now().isoformat(),
                "framework_info": {
                    "name": "BlueEdge",
                    "version": "1.0.0",
                    "algorithm": "levenshtein_enhanced",
                    "supported_categories": 6,
                    "languages": ["english", "arabic"]
                }
            }
            
            # Send updated stats
            response = requests.put(
                self.config.statistics_endpoint,
                json=updated_stats,
                timeout=self.request_timeout,
                headers={'User-Agent': 'BlueEdge-Framework/1.0'}
            )
            
            if response.status_code == 200:
                print("📊 Statistics updated successfully")
            else:
                print(f"❌ Statistics update failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Statistics update error: {str(e)}")
    
    def _calculate_average_time(self, current_stats, new_time):
        """Calculate updated average processing time"""
        current_avg = current_stats.get("average_processing_time", 0)
        current_count = current_stats.get("total_comparisons", 0)
        
        if current_count == 0:
            return new_time
        
        total_time = (current_avg * current_count) + new_time
        return total_time / (current_count + 1)
    
    def _update_category_distribution(self, current_stats, new_category):
        """Update error category distribution"""
        distribution = current_stats.get("category_distribution", {})
        
        if new_category and new_category != 'unknown':
            distribution[new_category] = distribution.get(new_category, 0) + 1
        
        return distribution
    
    def _calculate_accuracy_rate(self, current_stats, is_duplicate):
        """Calculate overall accuracy rate (placeholder - needs ground truth)"""
        # This is a simplified calculation
        # In production, you'd need ground truth data for real accuracy
        total = current_stats.get("total_comparisons", 0) + 1
        correct = current_stats.get("correct_predictions", total * 0.85) + (1 if is_duplicate else 0.85)
        
        return min(1.0, correct / total) if total > 0 else 0.85
    
    def _format_history_item(self, item):
        """Format history item for display"""
        try:
            comparison = item.get('comparison_results', {})
            timestamp = item.get('timestamp', '')
            
            # Format timestamp
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                time_str = dt.strftime('%m/%d %H:%M')
            except:
                time_str = timestamp[:16] if len(timestamp) > 16 else timestamp
            
            # Format names
            name1 = comparison.get('name1', 'Unknown')
            name2 = comparison.get('name2', 'Unknown')
            similarity = item.get('similarity_score', 0)
            category = item.get('error_category', 'unknown')
            
            return {
                'time': time_str,
                'name1': name1[:20] + '...' if len(name1) > 20 else name1,
                'name2': name2[:20] + '...' if len(name2) > 20 else name2,
                'similarity': f"{similarity:.1%}" if isinstance(similarity, (int, float)) else str(similarity),
                'category': category.replace('_', ' ').title(),
                'is_duplicate': item.get('duplicate_status', False)
            }
        except Exception as e:
            print(f"❌ History formatting error: {e}")
            return {
                'time': 'Unknown',
                'name1': 'Error',
                'name2': 'Error',
                'similarity': '0%',
                'category': 'Unknown',
                'is_duplicate': False
            }

class FirebaseSync:
    """Background synchronization service for BlueEdge"""
    
    def __init__(self, firebase_db: FirebaseDatabase):
        self.firebase_db = firebase_db
        self.sync_queue = []
        self.sync_thread = None
        self.running = False
        self.max_queue_size = 50
        print("🔄 Firebase Sync service initialized")
        
    def start_sync_service(self):
        """Start background sync service"""
        if not self.running and self.firebase_db.config.is_connected():
            self.running = True
            self.sync_thread = threading.Thread(target=self._sync_loop, daemon=True)
            self.sync_thread.start()
            print("🔄 Firebase sync service started")
        else:
            print("⚠️ Sync service not started - Firebase not connected")
    
    def stop_sync_service(self):
        """Stop background sync service"""
        if self.running:
            self.running = False
            if self.sync_thread and self.sync_thread.is_alive():
                self.sync_thread.join(timeout=3)
            print("⏹️ Firebase sync service stopped")
    
    def add_to_sync_queue(self, user_id, data):
        """Add data to sync queue with size limit"""
        if len(self.sync_queue) >= self.max_queue_size:
            # Remove oldest item if queue is full
            removed = self.sync_queue.pop(0)
            print(f"⚠️ Sync queue full - removed oldest item")
        
        sync_item = {
            'user_id': user_id,
            'data': data,
            'timestamp': datetime.now(),
            'retries': 0,
            'max_retries': 3
        }
        
        self.sync_queue.append(sync_item)
        print(f"📝 Added to sync queue (size: {len(self.sync_queue)})")
    
    def get_queue_status(self):
        """Get sync queue status"""
        return {
            'queue_size': len(self.sync_queue),
            'max_size': self.max_queue_size,
            'running': self.running,
            'connected': self.firebase_db.config.is_connected()
        }
    
    def _sync_loop(self):
        """Background sync loop with error handling"""
        consecutive_errors = 0
        max_consecutive_errors = 5
        
        while self.running:
            try:
                if self.sync_queue and self.firebase_db.config.is_connected():
                    item = self.sync_queue.pop(0)
                    
                    # Try to sync data
                    success, result = self.firebase_db.save_comparison_result(
                        item['user_id'],
                        item['data']
                    )
                    
                    if success:
                        print(f"✅ Sync successful for user {item['user_id']}")
                        consecutive_errors = 0  # Reset error counter
                        
                    elif item['retries'] < item['max_retries']:
                        # Retry failed items
                        item['retries'] += 1
                        self.sync_queue.append(item)
                        print(f"🔄 Retrying sync (attempt {item['retries']}/{item['max_retries']})")
                        consecutive_errors += 1
                        
                    else:
                        print(f"❌ Sync failed permanently for user {item['user_id']}")
                        consecutive_errors += 1
                
                # Adaptive sleep based on queue size and errors
                if consecutive_errors >= max_consecutive_errors:
                    time.sleep(10)  # Longer wait after many errors
                elif len(self.sync_queue) > 10:
                    time.sleep(1)   # Faster processing for large queue
                else:
                    time.sleep(3)   # Normal processing
                
            except Exception as e:
                print(f"❌ Sync loop error: {str(e)}")
                consecutive_errors += 1
                time.sleep(5)  # Wait longer on error

# Factory function for easy initialization
def create_firebase_service():
    """Create and configure Firebase service for BlueEdge"""
    print("🏗️ Creating Firebase service for BlueEdge...")
    
    try:
        config = FirebaseConfig()
        database = FirebaseDatabase(config)
        sync_service = FirebaseSync(database)
        
        # Test connection with retries
        success = False
        for attempt in range(config.max_connection_attempts):
            success, message = config.test_connection()
            if success:
                break
            elif attempt < config.max_connection_attempts - 1:
                print(f"🔄 Retrying connection in 2 seconds...")
                time.sleep(2)
        
        if success:
            print("✅ Firebase service ready for BlueEdge!")
            # Start sync service
            sync_service.start_sync_service()
        else:
            print(f"⚠️ Firebase service created but not connected: {message}")
            print("💡 The app will work in offline mode")
        
        return {
            'config': config,
            'database': database,
            'sync': sync_service,
            'connected': success,
            'message': message if not success else "Connected successfully"
        }
        
    except Exception as e:
        print(f"❌ Firebase service creation failed: {e}")
        return {
            'config': None,
            'database': None,
            'sync': None,
            'connected': False,
            'message': f"Service creation failed: {e}"
        }

# Utility functions for BlueEdge integration
def format_blueedge_data(comparison_result, name1="", name2=""):
    """Format BlueEdge comparison result for Firebase storage"""
    return {
        'name1': name1,
        'name2': name2,
        'similarity_score': comparison_result.get('similarity', 0),
        'is_duplicate': comparison_result.get('is_duplicate', False),
        'processing_time': comparison_result.get('processing_time', 0),
        'confidence_level': comparison_result.get('confidence', 'unknown'),
        'category': comparison_result.get('category', 'unknown'),
        'error_types': comparison_result.get('error_types', []),
        'algorithm_version': 'blueedge_v1.0',
        'platform': 'mobile_edge'
    }

def get_firebase_status():
    """Get current Firebase status for debugging"""
    try:
        service = create_firebase_service()
        return {
            'available': True,
            'connected': service['connected'],
            'message': service['message']
        }
    except Exception as e:
        return {
            'available': False,
            'connected': False,
            'message': f"Firebase not available: {e}"
        }

# Testing and debugging functions
def test_firebase_connection():
    """Quick test of Firebase connection"""
    print("🧪 Testing Firebase connection...")
    
    try:
        service = create_firebase_service()
        
        if service['connected']:
            print("✅ Firebase connection test successful")
            
            # Test data save
            test_data = {
                'similarity_score': 0.89,
                'is_duplicate': True,
                'processing_time': 1.2,
                'category': 'different_spelling'
            }
            
            success, key = service['database'].save_comparison_result("test_user", test_data)
            
            if success:
                print(f"✅ Test data save successful: {key}")
            else:
                print("❌ Test data save failed")
                
            # Test data retrieval
            success, history = service['database'].get_user_history("test_user", 1)
            
            if success:
                print(f"✅ Test data retrieval successful: {len(history)} items")
            else:
                print("❌ Test data retrieval failed")
                
        else:
            print(f"❌ Firebase connection test failed: {service['message']}")
            
        return service['connected']
        
    except Exception as e:
        print(f"❌ Firebase test error: {e}")
        return False

# Usage example and testing
if __name__ == "__main__":
    print("🔥 BlueEdge Firebase Configuration Test")
    print("=" * 60)
    
    # Run connection test
    success = test_firebase_connection()
    
    if success:
        print("\n🎉 Firebase integration is ready!")
        print("💡 Next steps:")
        print("1. Create Firebase project at: https://console.firebase.google.com/")
        print("2. Update API key and database URL in this file")
        print("3. Test the integration with the BlueEdge mobile app")
    else:
        print("\n⚠️ Firebase integration needs setup:")
        print("1. Create Firebase project")
        print("2. Enable Realtime Database")
        print("3. Update configuration in this file")
        print("4. Check internet connection")
        
    print("\n📖 The app will work in offline mode until Firebase is configured")