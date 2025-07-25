#!/usr/bin/env python3
"""
Fixed Simple Performance Monitor for BlueEdge Framework
======================================================
Lightweight performance monitoring without recursion issues
"""

import time
import threading
import gc
import sys
import json
from datetime import datetime
from collections import deque

class SimplePerformanceMonitor:
    """Fixed lightweight performance monitoring for BlueEdge"""
    
    def __init__(self, max_history=50):
        # Performance metrics storage
        self.max_history = max_history
        self.metrics_history = deque(maxlen=max_history)
        
        # Session metrics
        self.session_start = time.time()
        self.total_comparisons = 0
        self.total_processing_time = 0
        self.fastest_comparison = float('inf')
        self.slowest_comparison = 0
        
        # Cache metrics
        self.cache_hits = 0
        self.cache_misses = 0
        
        # Memory estimates
        self.estimated_memory_usage = 0
        self.peak_estimated_memory = 0
        
        # BlueEdge thresholds
        self.thresholds = {
            'target_processing_ms': 1000,  # 1 second target
            'max_processing_ms': 1500,     # 1.5 seconds max
            'estimated_memory_kb': 5000,   # 5KB per comparison
            'min_cache_hit_rate': 0.75     # 75% cache hit rate
        }
        
        print("📊 Simple Performance Monitor initialized (Fixed)")
        print(f"🎯 BlueEdge targets: {self.thresholds['target_processing_ms']}ms processing, ~5KB memory")
        
    def record_comparison(self, processing_time, data_size_estimate=None, cache_hit=None):
        """Record a name comparison operation"""
        timestamp = time.time()
        processing_ms = processing_time * 1000
        
        # Update session totals
        self.total_comparisons += 1
        self.total_processing_time += processing_time
        
        # Update performance ranges
        if processing_time < self.fastest_comparison:
            self.fastest_comparison = processing_time
        if processing_time > self.slowest_comparison:
            self.slowest_comparison = processing_time
        
        # Estimate memory usage
        if data_size_estimate:
            self.estimated_memory_usage += data_size_estimate
        else:
            self.estimated_memory_usage += 5 * 1024  # 5KB default
        
        if self.estimated_memory_usage > self.peak_estimated_memory:
            self.peak_estimated_memory = self.estimated_memory_usage
        
        # Update cache metrics
        if cache_hit is True:
            self.cache_hits += 1
        elif cache_hit is False:
            self.cache_misses += 1
        
        # Create performance record
        record = {
            'timestamp': timestamp,
            'comparison_id': self.total_comparisons,
            'processing_time_ms': processing_ms,
            'estimated_memory_kb': self.estimated_memory_usage / 1024,
            'cache_hit': cache_hit,
            'session_duration_s': timestamp - self.session_start,
            'performance_score': self._calculate_single_score(processing_ms)
        }
        
        # Add to history
        self.metrics_history.append(record)
        
        # Check for performance alerts
        self._check_performance_alerts(record)
        
        # Auto cleanup every 10 comparisons
        if self.total_comparisons % 10 == 0:
            self._auto_cleanup()
        
        return record
    
    def get_current_metrics(self):
        """Get current performance metrics (fixed - no recursion)"""
        current_time = time.time()
        session_duration = current_time - self.session_start
        
        # Calculate averages
        avg_processing_time = (self.total_processing_time / self.total_comparisons) if self.total_comparisons > 0 else 0
        cache_total = self.cache_hits + self.cache_misses
        cache_hit_rate = self.cache_hits / cache_total if cache_total > 0 else 0
        
        # Get recent performance (last 5 records)
        recent_records = list(self.metrics_history)[-5:] if self.metrics_history else []
        recent_avg_time = sum(r['processing_time_ms'] for r in recent_records) / len(recent_records) if recent_records else 0
        
        # Calculate efficiency WITHOUT calling self methods
        efficiency_score = self._calculate_efficiency_direct(avg_processing_time * 1000, cache_hit_rate)
        
        return {
            # Session summary
            'session_duration_s': session_duration,
            'session_duration_min': session_duration / 60,
            'total_comparisons': self.total_comparisons,
            'comparisons_per_minute': (self.total_comparisons / session_duration * 60) if session_duration > 0 else 0,
            
            # Processing performance
            'avg_processing_time_ms': avg_processing_time * 1000,
            'recent_avg_processing_time_ms': recent_avg_time,
            'fastest_comparison_ms': self.fastest_comparison * 1000 if self.fastest_comparison != float('inf') else 0,
            'slowest_comparison_ms': self.slowest_comparison * 1000,
            
            # Memory estimates
            'estimated_current_memory_kb': self.estimated_memory_usage / 1024,
            'peak_estimated_memory_kb': self.peak_estimated_memory / 1024,
            'estimated_memory_per_comparison_kb': (self.estimated_memory_usage / self.total_comparisons / 1024) if self.total_comparisons > 0 else 0,
            
            # Cache performance
            'cache_hit_rate': cache_hit_rate,
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'cache_total_requests': cache_total,
            
            # Performance status (calculated directly)
            'efficiency_score': efficiency_score,
            'performance_status': self._get_status_direct(efficiency_score),
            'blueedge_compliance': self._check_compliance_direct(avg_processing_time * 1000, cache_hit_rate),
            'optimization_tips': self._get_tips_direct(avg_processing_time * 1000, cache_hit_rate)
        }
    
    def get_performance_summary(self):
        """Get concise performance summary for UI display"""
        metrics = self.get_current_metrics()
        
        return {
            'total_comparisons': metrics['total_comparisons'],
            'avg_time_ms': round(metrics['avg_processing_time_ms']),
            'recent_time_ms': round(metrics['recent_avg_processing_time_ms']),
            'memory_kb': round(metrics['estimated_current_memory_kb']),
            'cache_rate': round(metrics['cache_hit_rate'] * 100),
            'efficiency': round(metrics['efficiency_score']),
            'status': metrics['performance_status'],
            'blueedge_compliant': metrics['blueedge_compliance']['overall_compliant']
        }
    
    def generate_report(self):
        """Generate detailed performance report"""
        metrics = self.get_current_metrics()
        
        report = {
            'report_timestamp': datetime.now().isoformat(),
            'blueedge_framework_version': '1.0.0',
            
            # Executive summary
            'summary': {
                'session_duration_minutes': round(metrics['session_duration_min'], 1),
                'total_comparisons_processed': metrics['total_comparisons'],
                'average_processing_speed_ms': round(metrics['avg_processing_time_ms']),
                'efficiency_rating': f"{metrics['efficiency_score']:.0f}/100",
                'overall_status': metrics['performance_status']
            },
            
            # Performance details
            'performance_metrics': {
                'processing_speed': {
                    'average_ms': round(metrics['avg_processing_time_ms']),
                    'fastest_ms': round(metrics['fastest_comparison_ms']),
                    'slowest_ms': round(metrics['slowest_comparison_ms']),
                    'recent_average_ms': round(metrics['recent_avg_processing_time_ms']),
                    'target_ms': self.thresholds['target_processing_ms'],
                    'meets_target': metrics['avg_processing_time_ms'] <= self.thresholds['target_processing_ms']
                },
                'memory_usage': {
                    'estimated_current_kb': round(metrics['estimated_current_memory_kb']),
                    'estimated_peak_kb': round(metrics['peak_estimated_memory_kb']),
                    'per_comparison_kb': round(metrics['estimated_memory_per_comparison_kb'], 1),
                    'blueedge_target_kb': self.thresholds['estimated_memory_kb'],
                    'within_target': metrics['estimated_current_memory_kb'] <= self.thresholds['estimated_memory_kb']
                },
                'cache_efficiency': {
                    'hit_rate_percent': round(metrics['cache_hit_rate'] * 100, 1),
                    'total_hits': metrics['cache_hits'],
                    'total_misses': metrics['cache_misses'],
                    'target_rate_percent': self.thresholds['min_cache_hit_rate'] * 100,
                    'meets_target': metrics['cache_hit_rate'] >= self.thresholds['min_cache_hit_rate']
                }
            },
            
            # BlueEdge compliance
            'blueedge_compliance': metrics['blueedge_compliance'],
            
            # Optimization recommendations
            'recommendations': metrics['optimization_tips']
        }
        
        return report
    
    def export_report(self, filename=None):
        """Export performance report to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"blueedge_performance_report_{timestamp}.json"
        
        try:
            report = self.generate_report()
            report['raw_metrics_history'] = list(self.metrics_history)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, default=str, ensure_ascii=False)
            
            print(f"📄 Performance report exported to: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return None
    
    def _calculate_single_score(self, processing_ms):
        """Calculate performance score for a single comparison"""
        if processing_ms <= self.thresholds['target_processing_ms']:
            return 100
        elif processing_ms <= self.thresholds['max_processing_ms']:
            excess = processing_ms - self.thresholds['target_processing_ms']
            max_excess = self.thresholds['max_processing_ms'] - self.thresholds['target_processing_ms']
            return 100 - (excess / max_excess * 30)
        else:
            return max(0, 70 - (processing_ms - self.thresholds['max_processing_ms']) / 100)
    
    def _calculate_efficiency_direct(self, avg_processing_ms, cache_hit_rate):
        """Calculate efficiency without recursion"""
        if self.total_comparisons == 0:
            return 100
        
        score = 100
        
        # Processing time impact (40% weight)
        if avg_processing_ms > self.thresholds['target_processing_ms']:
            time_penalty = min(40, (avg_processing_ms - self.thresholds['target_processing_ms']) / 10)
            score -= time_penalty
        
        # Memory impact (30% weight)
        memory_kb = self.estimated_memory_usage / 1024
        if memory_kb > self.thresholds['estimated_memory_kb']:
            memory_penalty = min(30, (memory_kb - self.thresholds['estimated_memory_kb']) / 1000)
            score -= memory_penalty
        
        # Cache impact (30% weight)
        if cache_hit_rate < self.thresholds['min_cache_hit_rate']:
            cache_penalty = (self.thresholds['min_cache_hit_rate'] - cache_hit_rate) * 30
            score -= cache_penalty
        
        return max(0, min(100, score))
    
    def _get_status_direct(self, efficiency):
        """Get status based on efficiency score"""
        if efficiency >= 90:
            return 'excellent'
        elif efficiency >= 75:
            return 'good'
        elif efficiency >= 60:
            return 'acceptable'
        else:
            return 'needs_optimization'
    
    def _check_compliance_direct(self, avg_processing_ms, cache_hit_rate):
        """Check BlueEdge compliance directly"""
        memory_kb = self.estimated_memory_usage / 1024
        
        compliance = {
            'processing_time_compliant': avg_processing_ms <= self.thresholds['target_processing_ms'],
            'memory_compliant': memory_kb <= self.thresholds['estimated_memory_kb'],
            'cache_compliant': cache_hit_rate >= self.thresholds['min_cache_hit_rate']
        }
        
        compliance['overall_compliant'] = all(compliance.values())
        compliance['compliance_score'] = sum(compliance.values()) / 3 * 100
        
        return compliance
    
    def _get_tips_direct(self, avg_processing_ms, cache_hit_rate):
        """Get optimization tips directly"""
        tips = []
        memory_kb = self.estimated_memory_usage / 1024
        
        if avg_processing_ms > self.thresholds['target_processing_ms']:
            tips.append({
                'category': 'speed',
                'tip': f"Average processing time ({avg_processing_ms:.0f}ms) exceeds target ({self.thresholds['target_processing_ms']}ms)",
                'priority': 'high' if avg_processing_ms > self.thresholds['max_processing_ms'] else 'medium'
            })
        
        if memory_kb > self.thresholds['estimated_memory_kb']:
            tips.append({
                'category': 'memory',
                'tip': f"Memory usage ({memory_kb:.0f}KB) exceeds target ({self.thresholds['estimated_memory_kb']}KB)",
                'priority': 'medium'
            })
        
        if cache_hit_rate < self.thresholds['min_cache_hit_rate']:
            tips.append({
                'category': 'cache',
                'tip': f"Cache hit rate ({cache_hit_rate:.1%}) below target ({self.thresholds['min_cache_hit_rate']:.1%})",
                'priority': 'medium'
            })
        
        return tips
    
    def _check_performance_alerts(self, record):
        """Check for real-time performance alerts"""
        if record['processing_time_ms'] > self.thresholds['max_processing_ms']:
            print(f"🐌 Slow comparison detected: {record['processing_time_ms']:.0f}ms (comparison #{record['comparison_id']})")
        
        if record['estimated_memory_kb'] > self.thresholds['estimated_memory_kb'] * 1.5:
            print(f"💾 High memory usage estimated: {record['estimated_memory_kb']:.0f}KB")
    
    def _auto_cleanup(self):
        """Automatic memory cleanup"""
        try:
            gc.collect()
            self.estimated_memory_usage = max(0, self.estimated_memory_usage * 0.8)
            print(f"🧹 Auto cleanup executed (comparison #{self.total_comparisons})")
        except Exception as e:
            print(f"❌ Cleanup failed: {e}")
    
    def manual_cleanup(self):
        """Manual performance optimization"""
        print("🧹 Running manual cleanup...")
        gc.collect()
        
        if len(self.metrics_history) > 20:
            recent_metrics = list(self.metrics_history)[-20:]
            self.metrics_history.clear()
            self.metrics_history.extend(recent_metrics)
        
        self.estimated_memory_usage = max(0, self.estimated_memory_usage * 0.6)
        print("✅ Manual cleanup completed")
        return True

# Testing
if __name__ == "__main__":
    print("📊 BlueEdge Performance Monitor - Fixed Version")
    print("=" * 55)
    
    monitor = SimplePerformanceMonitor()
    
    # Test cases
    test_cases = [
        {"time": 0.8, "cache": True, "desc": "Fast comparison (cached)"},
        {"time": 1.2, "cache": False, "desc": "Normal comparison"},
        {"time": 0.5, "cache": True, "desc": "Very fast (cached)"},
        {"time": 1.8, "cache": False, "desc": "Slow comparison"},
        {"time": 0.9, "cache": True, "desc": "Good performance"}
    ]
    
    print("\n🧪 Running performance tests...")
    
    for i, test in enumerate(test_cases):
        record = monitor.record_comparison(test["time"], cache_hit=test["cache"])
        print(f"✅ {test['desc']}: {record['processing_time_ms']:.0f}ms (Score: {record['performance_score']:.0f})")
        time.sleep(0.1)
    
    print("\n📊 Performance Summary:")
    summary = monitor.get_performance_summary()
    
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    print("\n📄 Generating report...")
    report = monitor.generate_report()
    print(f"Session: {report['summary']['session_duration_minutes']} min")
    print(f"Efficiency: {report['summary']['efficiency_rating']}")
    print(f"Status: {report['summary']['overall_status']}")
    
    filename = monitor.export_report()
    print(f"\n✅ Test completed! Report: {filename}")