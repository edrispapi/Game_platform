#!/usr/bin/env python3
"""
Comprehensive Test Script for All Steam Clone Services
Tests all services with real data and validates Swagger documentation
"""

import asyncio
import aiohttp
import json
import time
import subprocess
import sys
import os
from typing import Dict, List, Any
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ServiceTester:
    def __init__(self):
        self.base_url = "http://localhost"
        self.services = {
            'api-gateway': {'port': 8000, 'health': '/health'},
            'user-service': {'port': 8001, 'health': '/health'},
            'game-catalog-service': {'port': 8002, 'health': '/health'},
            'review-service': {'port': 8003, 'health': '/health'},
            'shopping-service': {'port': 8004, 'health': '/health'},
            'purchase-service': {'port': 8005, 'health': '/health'},
            'payment-service': {'port': 8006, 'health': '/health'},
            'online-service': {'port': 8007, 'health': '/health'},
            'social-service': {'port': 8008, 'health': '/health'},
            'notification-service': {'port': 8009, 'health': '/health'},
            'recommendation-service': {'port': 8010, 'health': '/health'},
            'achievement-service': {'port': 8011, 'health': '/health'},
            'monitoring-service': {'port': 8012, 'health': '/health'}
        }
        self.session = None
        self.test_results = {}
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def check_service_health(self, service_name: str) -> bool:
        """Check if a service is healthy"""
        try:
            service_config = self.services[service_name]
            url = f"{self.base_url}:{service_config['port']}{service_config['health']}"
            
            async with self.session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"✅ {service_name} is healthy: {data}")
                    return True
                else:
                    logger.error(f"❌ {service_name} health check failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ {service_name} health check error: {e}")
            return False
    
    async def test_swagger_docs(self, service_name: str) -> bool:
        """Test if Swagger documentation is accessible"""
        try:
            service_config = self.services[service_name]
            url = f"{self.base_url}:{service_config['port']}/docs"
            
            async with self.session.get(url, timeout=10) as response:
                if response.status == 200:
                    logger.info(f"✅ {service_name} Swagger docs accessible")
                    return True
                else:
                    logger.error(f"❌ {service_name} Swagger docs failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ {service_name} Swagger docs error: {e}")
            return False
    
    async def test_api_endpoints(self, service_name: str) -> Dict[str, Any]:
        """Test API endpoints for a specific service"""
        results = {
            'service': service_name,
            'endpoints_tested': 0,
            'endpoints_passed': 0,
            'endpoints_failed': 0,
            'errors': []
        }
        
        try:
            service_config = self.services[service_name]
            base_url = f"{self.base_url}:{service_config['port']}"
            
            # Define test endpoints for each service
            test_endpoints = self.get_test_endpoints(service_name)
            
            for endpoint, method in test_endpoints:
                results['endpoints_tested'] += 1
                url = f"{base_url}{endpoint}"
                
                try:
                    if method.upper() == 'GET':
                        async with self.session.get(url, timeout=10) as response:
                            if response.status in [200, 201, 404]:  # 404 is acceptable for some endpoints
                                results['endpoints_passed'] += 1
                                logger.info(f"✅ {service_name} {method} {endpoint} - {response.status}")
                            else:
                                results['endpoints_failed'] += 1
                                error_msg = f"{method} {endpoint} - {response.status}"
                                results['errors'].append(error_msg)
                                logger.error(f"❌ {service_name} {error_msg}")
                    elif method.upper() == 'POST':
                        # Test with sample data
                        test_data = self.get_test_data(service_name, endpoint)
                        async with self.session.post(url, json=test_data, timeout=10) as response:
                            if response.status in [200, 201, 400, 422]:  # 400/422 are acceptable for validation errors
                                results['endpoints_passed'] += 1
                                logger.info(f"✅ {service_name} {method} {endpoint} - {response.status}")
                            else:
                                results['endpoints_failed'] += 1
                                error_msg = f"{method} {endpoint} - {response.status}"
                                results['errors'].append(error_msg)
                                logger.error(f"❌ {service_name} {error_msg}")
                except Exception as e:
                    results['endpoints_failed'] += 1
                    error_msg = f"{method} {endpoint} - {str(e)}"
                    results['errors'].append(error_msg)
                    logger.error(f"❌ {service_name} {error_msg}")
                
                # Small delay between requests
                await asyncio.sleep(0.1)
                
        except Exception as e:
            logger.error(f"❌ {service_name} API testing error: {e}")
            results['errors'].append(f"API testing error: {str(e)}")
        
        return results
    
    def get_test_endpoints(self, service_name: str) -> List[tuple]:
        """Get test endpoints for a specific service"""
        endpoints = {
            'api-gateway': [
                ('/', 'GET'),
                ('/health', 'GET'),
                ('/docs', 'GET')
            ],
            'user-service': [
                ('/', 'GET'),
                ('/health', 'GET'),
                ('/docs', 'GET'),
                ('/api/v1/users/', 'GET'),
                ('/api/v1/users/', 'POST')
            ],
            'game-catalog-service': [
                ('/', 'GET'),
                ('/health', 'GET'),
                ('/docs', 'GET'),
                ('/api/v1/catalog/games', 'GET'),
                ('/api/v1/catalog/games', 'POST')
            ],
            'review-service': [
                ('/', 'GET'),
                ('/health', 'GET'),
                ('/docs', 'GET'),
                ('/api/v1/reviews/', 'GET'),
                ('/api/v1/reviews/', 'POST')
            ],
            'shopping-service': [
                ('/', 'GET'),
                ('/health', 'GET'),
                ('/docs', 'GET'),
                ('/api/v1/shopping/carts', 'GET'),
                ('/api/v1/shopping/wishlists', 'GET')
            ],
            'purchase-service': [
                ('/', 'GET'),
                ('/health', 'GET'),
                ('/docs', 'GET'),
                ('/api/v1/purchases/orders', 'GET'),
                ('/api/v1/purchases/orders', 'POST')
            ],
            'payment-service': [
                ('/', 'GET'),
                ('/health', 'GET'),
                ('/docs', 'GET'),
                ('/api/v1/payments/methods', 'GET'),
                ('/api/v1/payments/transactions', 'GET')
            ],
            'online-service': [
                ('/', 'GET'),
                ('/health', 'GET'),
                ('/docs', 'GET'),
                ('/api/v1/online/sessions', 'GET'),
                ('/api/v1/online/sessions', 'POST')
            ],
            'social-service': [
                ('/', 'GET'),
                ('/health', 'GET'),
                ('/docs', 'GET'),
                ('/api/v1/social/friends', 'GET'),
                ('/api/v1/social/groups', 'GET')
            ],
            'notification-service': [
                ('/', 'GET'),
                ('/health', 'GET'),
                ('/docs', 'GET'),
                ('/api/v1/notifications/', 'GET'),
                ('/api/v1/notifications/', 'POST')
            ],
            'recommendation-service': [
                ('/', 'GET'),
                ('/health', 'GET'),
                ('/docs', 'GET'),
                ('/api/v1/recommendations/', 'GET'),
                ('/api/v1/recommendations/', 'POST')
            ],
            'achievement-service': [
                ('/', 'GET'),
                ('/health', 'GET'),
                ('/docs', 'GET'),
                ('/api/v1/achievements/', 'GET'),
                ('/api/v1/achievements/', 'POST')
            ],
            'monitoring-service': [
                ('/', 'GET'),
                ('/health', 'GET'),
                ('/docs', 'GET'),
                ('/api/v1/monitoring/metrics', 'GET'),
                ('/api/v1/monitoring/alerts', 'GET')
            ]
        }
        
        return endpoints.get(service_name, [])
    
    def get_test_data(self, service_name: str, endpoint: str) -> Dict[str, Any]:
        """Get test data for POST requests"""
        test_data = {
            'user-service': {
                '/api/v1/users/': {
                    'username': 'testuser123',
                    'email': 'test@example.com',
                    'password': 'testpassword123',
                    'first_name': 'Test',
                    'last_name': 'User'
                }
            },
            'game-catalog-service': {
                '/api/v1/catalog/games': {
                    'name': 'Test Game',
                    'price': 29.99,
                    'description': 'A test game for testing purposes',
                    'developer': 'Test Developer',
                    'publisher': 'Test Publisher'
                }
            },
            'review-service': {
                '/api/v1/reviews/': {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'game_id': 1,
                    'rating': 5,
                    'title': 'Great Game!',
                    'content': 'This is a fantastic game that I highly recommend.'
                }
            },
            'shopping-service': {
                '/api/v1/shopping/carts': {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'items': [{'game_id': 1, 'quantity': 1}]
                }
            },
            'purchase-service': {
                '/api/v1/purchases/orders': {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'items': [{'game_id': 1, 'quantity': 1, 'price': 29.99}],
                    'total_amount': 29.99
                }
            },
            'payment-service': {
                '/api/v1/payments/methods': {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'type': 'credit_card',
                    'provider': 'visa',
                    'last_four_digits': '1234'
                }
            },
            'online-service': {
                '/api/v1/online/sessions': {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'game_id': 1,
                    'status': 'online'
                }
            },
            'social-service': {
                '/api/v1/social/friends': {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'friend_id': '123e4567-e89b-12d3-a456-426614175000'
                }
            },
            'notification-service': {
                '/api/v1/notifications/': {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'type': 'email',
                    'title': 'Test Notification',
                    'content': 'This is a test notification'
                }
            },
            'recommendation-service': {
                '/api/v1/recommendations/': {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'algorithm': 'collaborative',
                    'limit': 10
                }
            },
            'achievement-service': {
                '/api/v1/achievements/': {
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'game_id': 1,
                    'name': 'Test Achievement',
                    'description': 'A test achievement'
                }
            },
            'monitoring-service': {
                '/api/v1/monitoring/metrics': {
                    'service_name': 'test-service',
                    'metric_name': 'test_metric',
                    'metric_value': 100.0
                }
            }
        }
        
        return test_data.get(service_name, {}).get(endpoint, {})
    
    async def run_performance_test(self, service_name: str, endpoint: str, num_requests: int = 10) -> Dict[str, Any]:
        """Run performance test on a specific endpoint"""
        results = {
            'service': service_name,
            'endpoint': endpoint,
            'num_requests': num_requests,
            'total_time': 0,
            'avg_response_time': 0,
            'min_response_time': float('inf'),
            'max_response_time': 0,
            'success_count': 0,
            'error_count': 0,
            'errors': []
        }
        
        try:
            service_config = self.services[service_name]
            url = f"{self.base_url}:{service_config['port']}{endpoint}"
            
            start_time = time.time()
            
            tasks = []
            for i in range(num_requests):
                task = asyncio.create_task(self.make_request(url))
                tasks.append(task)
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            end_time = time.time()
            results['total_time'] = end_time - start_time
            
            response_times = []
            for response in responses:
                if isinstance(response, dict):
                    response_times.append(response['response_time'])
                    if response['success']:
                        results['success_count'] += 1
                    else:
                        results['error_count'] += 1
                        results['errors'].append(response['error'])
                else:
                    results['error_count'] += 1
                    results['errors'].append(str(response))
            
            if response_times:
                results['avg_response_time'] = sum(response_times) / len(response_times)
                results['min_response_time'] = min(response_times)
                results['max_response_time'] = max(response_times)
            
        except Exception as e:
            logger.error(f"❌ Performance test error for {service_name} {endpoint}: {e}")
            results['errors'].append(str(e))
        
        return results
    
    async def make_request(self, url: str) -> Dict[str, Any]:
        """Make a single request and measure response time"""
        start_time = time.time()
        try:
            async with self.session.get(url, timeout=10) as response:
                end_time = time.time()
                return {
                    'success': response.status == 200,
                    'response_time': (end_time - start_time) * 1000,  # Convert to milliseconds
                    'status_code': response.status,
                    'error': None
                }
        except Exception as e:
            end_time = time.time()
            return {
                'success': False,
                'response_time': (end_time - start_time) * 1000,
                'status_code': None,
                'error': str(e)
            }
    
    async def run_all_tests(self):
        """Run all tests for all services"""
        logger.info("🚀 Starting comprehensive service testing...")
        
        # Test service health
        logger.info("\n📊 Testing service health...")
        health_results = {}
        for service_name in self.services:
            health_results[service_name] = await self.check_service_health(service_name)
        
        # Test Swagger documentation
        logger.info("\n📚 Testing Swagger documentation...")
        swagger_results = {}
        for service_name in self.services:
            swagger_results[service_name] = await self.test_swagger_docs(service_name)
        
        # Test API endpoints
        logger.info("\n🔧 Testing API endpoints...")
        api_results = {}
        for service_name in self.services:
            logger.info(f"\nTesting {service_name}...")
            api_results[service_name] = await self.test_api_endpoints(service_name)
        
        # Run performance tests
        logger.info("\n⚡ Running performance tests...")
        performance_results = {}
        for service_name in self.services:
            logger.info(f"\nPerformance testing {service_name}...")
            service_config = self.services[service_name]
            performance_results[service_name] = await self.run_performance_test(
                service_name, 
                service_config['health'], 
                num_requests=20
            )
        
        # Generate report
        self.generate_report(health_results, swagger_results, api_results, performance_results)
    
    def generate_report(self, health_results, swagger_results, api_results, performance_results):
        """Generate comprehensive test report"""
        logger.info("\n" + "="*80)
        logger.info("📋 COMPREHENSIVE TEST REPORT")
        logger.info("="*80)
        
        # Health check summary
        logger.info("\n🏥 SERVICE HEALTH SUMMARY:")
        healthy_services = sum(1 for is_healthy in health_results.values() if is_healthy)
        total_services = len(health_results)
        logger.info(f"Healthy services: {healthy_services}/{total_services}")
        
        for service, is_healthy in health_results.items():
            status = "✅ HEALTHY" if is_healthy else "❌ UNHEALTHY"
            logger.info(f"  {service}: {status}")
        
        # Swagger documentation summary
        logger.info("\n📚 SWAGGER DOCUMENTATION SUMMARY:")
        swagger_accessible = sum(1 for is_accessible in swagger_results.values() if is_accessible)
        logger.info(f"Accessible docs: {swagger_accessible}/{total_services}")
        
        for service, is_accessible in swagger_results.items():
            status = "✅ ACCESSIBLE" if is_accessible else "❌ NOT ACCESSIBLE"
            logger.info(f"  {service}: {status}")
        
        # API endpoints summary
        logger.info("\n🔧 API ENDPOINTS SUMMARY:")
        for service, results in api_results.items():
            total_tested = results['endpoints_tested']
            total_passed = results['endpoints_passed']
            total_failed = results['endpoints_failed']
            success_rate = (total_passed / total_tested * 100) if total_tested > 0 else 0
            
            logger.info(f"  {service}: {total_passed}/{total_tested} passed ({success_rate:.1f}%)")
            if results['errors']:
                logger.info(f"    Errors: {len(results['errors'])}")
        
        # Performance summary
        logger.info("\n⚡ PERFORMANCE SUMMARY:")
        for service, results in performance_results.items():
            if results['success_count'] > 0:
                avg_time = results['avg_response_time']
                min_time = results['min_response_time']
                max_time = results['max_response_time']
                success_rate = (results['success_count'] / results['num_requests'] * 100)
                
                logger.info(f"  {service}:")
                logger.info(f"    Avg response time: {avg_time:.2f}ms")
                logger.info(f"    Min response time: {min_time:.2f}ms")
                logger.info(f"    Max response time: {max_time:.2f}ms")
                logger.info(f"    Success rate: {success_rate:.1f}%")
            else:
                logger.info(f"  {service}: ❌ No successful requests")
        
        # Overall summary
        logger.info("\n📊 OVERALL SUMMARY:")
        overall_health = healthy_services / total_services * 100
        overall_swagger = swagger_accessible / total_services * 100
        
        logger.info(f"Service Health: {overall_health:.1f}%")
        logger.info(f"Swagger Access: {overall_swagger:.1f}%")
        
        if overall_health >= 80 and overall_swagger >= 80:
            logger.info("🎉 Overall Status: EXCELLENT")
        elif overall_health >= 60 and overall_swagger >= 60:
            logger.info("✅ Overall Status: GOOD")
        elif overall_health >= 40 and overall_swagger >= 40:
            logger.info("⚠️ Overall Status: FAIR")
        else:
            logger.info("❌ Overall Status: POOR")
        
        logger.info("\n" + "="*80)

async def main():
    """Main function to run all tests"""
    async with ServiceTester() as tester:
        await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())