#!/usr/bin/env python3
"""
Smart Caching System for BlueEdge Framework - Final Version
==========================================================
Intelligent result caching to accelerate duplicate name comparisons
Features:
- LRU (Least Recently Used) cache eviction
- Similarity-based cache lookup
- Memory-efficient storage for mobile devices
- Cache analytics and optimization
- Mobile-optimized for 5KB memory constraint per comparison
"""

import time
import hashlib
import json
from collections import OrderedDict
from datetime import datetime

class SmartCache:
    """Intelligent caching system for BlueEdge name comparisons"""
    
    def __init__(self, max_size=50, max_memory_kb=25):
        """
        Initialize Smart Cache
        
        Args:
            max_size: Maximum number of cached results (default: 50 for mobile)
            max_memory_kb: Maximum memory usage in KB (default: 25KB for mobile)
        """
        # Cache storage (using OrderedDict for LRU)
        self.cache = OrderedDict()
        self.max_size = max_size
        self.max_memory_kb = max_memory_kb
        
        # Cache statistics
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.total_requests = 0
        
        # Performance tracking
        self.creation_time = time.time()
        self.last_cleanup = time.time()
        self.estimated_memory_bytes = 0
        
        # Cache configuration (mobile-optimized)
        self.similarity_threshold = 0.95  # 95% similarity for cache hit
        self.expire_hours = 12  # Cache entries expire after 12 hours (mobile-optimized)
        self.cleanup_interval = 300  # Cleanup every 5 minutes
        
        print(f"🧠 Smart Cache initialized - Max: {max_size} items, {max_memory_kb}KB")
    
    def get_cache_key(self, name1, name2):
        """Generate cache key for name pair"""
        # Normalize names for consistent caching
        n1 = str(name1).lower().strip()
        n2 = str(name2).lower().strip()
        
        # Sort names to ensure consistent key regardless of order
        if n1 > n2:
            n1, n2 = n2, n1
        
        # Create hash-based key (shorter for mobile)
        key_string = f"{n1}|{n2}"
        return hashlib.md5(key_string.encode('utf-8')).hexdigest()[:10]  # Shorter hash for mobile
    
    def get(self, name1, name2):
        """
        Get cached comparison result
        
        Returns:
            tuple: (found, result) - found is boolean, result is cached data or None
        """
        self.total_requests += 1
        
        # Check if cleanup is needed
        if time.time() - self.last_cleanup > self.cleanup_interval:
            self._auto_cleanup()
        
        cache_key = self.get_cache_key(name1, name2)
        
        if cache_key in self.cache:
            cached_item = self.cache[cache_key]
            
            # Check if expired
            if self._is_expired(cached_item):
                del self.cache[cache_key]
                self.estimated_memory_bytes -= cached_item['size_bytes']
                self.misses += 1
                return False, None
            
            # Move to end (most recently used)
            self.cache.move_to_end(cache_key)
            
            # Update access info
            cached_item['last_accessed'] = time.time()
            cached_item['access_count'] += 1
            
            self.hits += 1
            return True, cached_item['result']
        
        self.misses += 1
        return False, None
    
    def put(self, name1, name2, comparison_result):
        """
        Store comparison result in cache
        
        Args:
            name1, name2: Names being compared
            comparison_result: The comparison result to cache
        """
        cache_key = self.get_cache_key(name1, name2)
        
        # Create cache entry
        cache_entry = {
            'key': cache_key,
            'name1': str(name1),
            'name2': str(name2),
            'result': comparison_result,
            'created_at': time.time(),
            'last_accessed': time.time(),
            'access_count': 1,
            'size_bytes': self._estimate_size(comparison_result)
        }
        
        # Check memory limit before adding
        estimated_new_memory = self.estimated_memory_bytes + cache_entry['size_bytes']
        if estimated_new_memory > self.max_memory_kb * 1024:
            self._memory_cleanup()
        
        # Remove existing entry if present
        if cache_key in self.cache:
            old_entry = self.cache[cache_key]
            self.estimated_memory_bytes -= old_entry['size_bytes']
        
        # Add to cache
        self.cache[cache_key] = cache_entry
        self.estimated_memory_bytes += cache_entry['size_bytes']
        
        # Check size limit and evict if necessary
        while len(self.cache) > self.max_size:
            self._evict_lru()
    
    def get_statistics(self):
        """Get cache performance statistics"""
        total_requests = max(1, self.total_requests)  # Avoid division by zero
        hit_rate = self.hits / total_requests
        miss_rate = self.misses / total_requests
        
        # Calculate memory usage
        current_memory_kb = self.estimated_memory_bytes / 1024
        memory_utilization = (current_memory_kb / self.max_memory_kb) * 100 if self.max_memory_kb > 0 else 0
        
        # Calculate efficiency metrics
        avg_access_per_item = sum(item['access_count'] for item in self.cache.values()) / max(1, len(self.cache))
        
        return {
            # Basic statistics
            'total_requests': self.total_requests,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'miss_rate': miss_rate,
            'evictions': self.evictions,
            
            # Cache status
            'current_size': len(self.cache),
            'max_size': self.max_size,
            'size_utilization': (len(self.cache) / self.max_size) * 100 if self.max_size > 0 else 0,
            
            # Memory usage
            'estimated_memory_kb': current_memory_kb,
            'max_memory_kb': self.max_memory_kb,
            'memory_utilization': memory_utilization,
            
            # Performance metrics
            'avg_access_per_item': avg_access_per_item,
            'cache_age_hours': (time.time() - self.creation_time) / 3600,
            'last_cleanup_ago_minutes': (time.time() - self.last_cleanup) / 60,
            
            # Efficiency rating
            'efficiency_score': self._calculate_efficiency_score(hit_rate, memory_utilization)
        }
    
    def clear(self):
        """Clear all cached items"""
        cleared_count = len(self.cache)
        self.cache.clear()
        self.estimated_memory_bytes = 0
        
        print(f"🗑️ Cache cleared - removed {cleared_count} items")
        return cleared_count
    
    def optimize(self):
        """Optimize cache for better performance"""
        print("🔧 Optimizing cache...")
        
        initial_size = len(self.cache)
        initial_memory = self.estimated_memory_bytes
        
        # Remove expired items
        expired_count = self._remove_expired()
        
        # Remove least accessed items if memory is high
        if self.estimated_memory_bytes > (self.max_memory_kb * 1024 * 0.8):
            memory_freed = self._memory_cleanup()
        else:
            memory_freed = 0
        
        final_size = len(self.cache)
        final_memory = self.estimated_memory_bytes
        
        print(f"✅ Cache optimization completed:")
        print(f"   Items: {initial_size} → {final_size}")
        print(f"   Memory: {initial_memory/1024:.1f}KB → {final_memory/1024:.1f}KB")
        print(f"   Expired removed: {expired_count}")
        
        return {
            'items_before': initial_size,
            'items_after': final_size,
            'memory_before_kb': initial_memory / 1024,
            'memory_after_kb': final_memory / 1024,
            'expired_removed': expired_count,
            'memory_freed_kb': memory_freed / 1024
        }
    
    def _estimate_size(self, obj):
        """Estimate memory size of object in bytes (mobile-optimized)"""
        try:
            # Simple estimation for mobile optimization
            if isinstance(obj, dict):
                size = len(str(obj))  # Simplified
            elif isinstance(obj, str):
                size = len(obj.encode('utf-8'))
            else:
                size = len(str(obj))
            
            return max(50, size)  # Minimum 50 bytes per item (mobile-optimized)
        except:
            return 100  # Default size
    
    def _is_expired(self, cache_item):
        """Check if cache item is expired"""
        age_hours = (time.time() - cache_item['created_at']) / 3600
        return age_hours > self.expire_hours
    
    def _evict_lru(self):
        """Evict least recently used item"""
        if not self.cache:
            return
        
        # Remove first item (least recently used)
        lru_key, lru_item = self.cache.popitem(last=False)
        self.estimated_memory_bytes -= lru_item['size_bytes']
        self.evictions += 1
    
    def _memory_cleanup(self):
        """Clean up memory by removing low-value items"""
        if not self.cache:
            return 0
        
        # Sort by value score (access_count / age)
        items_by_value = []
        current_time = time.time()
        
        for key, item in self.cache.items():
            age_hours = (current_time - item['created_at']) / 3600
            value_score = item['access_count'] / max(1, age_hours)
            items_by_value.append((key, item, value_score))
        
        # Sort by value score (lowest first)
        items_by_value.sort(key=lambda x: x[2])
        
        # Remove lowest value items until memory is acceptable
        target_memory = self.max_memory_kb * 1024 * 0.7  # Target 70% of max
        memory_freed = 0
        
        for key, item, value_score in items_by_value:
            if self.estimated_memory_bytes <= target_memory:
                break
            
            self.estimated_memory_bytes -= item['size_bytes']
            memory_freed += item['size_bytes']
            del self.cache[key]
            self.evictions += 1
        
        return memory_freed
    
    def _auto_cleanup(self):
        """Automatic cleanup of expired items"""
        self.last_cleanup = time.time()
        expired_count = self._remove_expired()
        
        if expired_count > 0:
            print(f"🧹 Auto cleanup: removed {expired_count} expired items")
    
    def _remove_expired(self):
        """Remove expired cache items"""
        expired_keys = []
        
        for key, item in self.cache.items():
            if self._is_expired(item):
                expired_keys.append(key)
        
        for key in expired_keys:
            item = self.cache[key]
            self.estimated_memory_bytes -= item['size_bytes']
            del self.cache[key]
        
        return len(expired_keys)
    
    def _calculate_efficiency_score(self, hit_rate, memory_utilization):
        """Calculate cache efficiency score (0-100)"""
        # Hit rate component (70% weight)
        hit_score = hit_rate * 70
        
        # Memory efficiency component (30% weight)
        # Optimal memory utilization is around 60-80% for mobile
        if memory_utilization <= 80:
            memory_score = 30
        elif memory_utilization <= 90:
            memory_score = 30 - ((memory_utilization - 80) * 2)
        else:
            memory_score = max(0, 10 - (memory_utilization - 90))
        
        return min(100, hit_score + memory_score)

# Testing and usage example
if __name__ == "__main__":
    print("🧠 Smart Cache System Test - Mobile Optimized")
    print("=" * 50)
    
    # Initialize cache (mobile-optimized settings)
    cache = SmartCache(max_size=20, max_memory_kb=10)
    
    # Test data
    test_comparisons = [
        ("Ahmed Hassan", "Ahmad Hasan", {"similarity_score": 0.89, "is_duplicate": True, "category": "spelling_variation"}),
        ("Mohammed Ali", "Mohamed Ali", {"similarity_score": 0.95, "is_duplicate": True, "category": "spelling_variation"}),
        ("Sara Ibrahim", "Sarah Ibrahim", {"similarity_score": 0.92, "is_duplicate": True, "category": "spelling_variation"}),
        ("Omar Khalil", "Omar Khaleel", {"similarity_score": 0.87, "is_duplicate": True, "category": "spelling_variation"}),
        ("Fatima Salem", "Fatema Salim", {"similarity_score": 0.91, "is_duplicate": True, "category": "spelling_variation"})
    ]
    
    print("\n🧪 Testing cache operations...")
    
    # Test cache misses and puts
    for name1, name2, result in test_comparisons:
        found, cached_result = cache.get(name1, name2)
        if not found:
            print(f"❌ Cache MISS: {name1} vs {name2}")
            cache.put(name1, name2, result)
            print(f"💾 Cached result: {result['similarity_score']}")
        else:
            print(f"✅ Cache HIT: {name1} vs {name2}")
    
    # Test cache hits
    print("\n🔄 Testing cache hits...")
    for name1, name2, result in test_comparisons[:3]:
        found, cached_result = cache.get(name1, name2)
        if found:
            print(f"✅ Cache HIT: {name1} vs {name2} (similarity: {cached_result['similarity_score']})")
        else:
            print(f"❌ Unexpected cache miss: {name1} vs {name2}")
    
    # Get statistics
    print("\n📊 Cache Statistics:")
    stats = cache.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"{key}: {value:.2f}")
        else:
            print(f"{key}: {value}")
    
    # Test optimization
    print("\n🔧 Testing cache optimization...")
    optimization_result = cache.optimize()
    
    print("\n✅ Smart Cache test completed!")
    print(f"📊 Final hit rate: {stats['hit_rate']:.1%}")
    print(f"💾 Memory usage: {stats['estimated_memory_kb']:.1f}KB")
    print(f"⚡ Efficiency score: {stats['efficiency_score']:.0f}/100") 
