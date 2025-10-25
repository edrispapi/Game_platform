#!/usr/bin/env python3
"""
Manual Service Starter for Steam Clone
Starts services locally without Docker
"""

import subprocess
import time
import os
import sys
import signal
import threading
from pathlib import Path

class ServiceStarter:
    def __init__(self):
        self.processes = []
        self.base_dir = Path(__file__).parent.parent
        
    def start_service(self, service_name, port, working_dir):
        """Start a single service"""
        print(f"🚀 Starting {service_name} on port {port}...")
        
        try:
            # Change to service directory
            service_dir = self.base_dir / "services" / service_name
            
            if not service_dir.exists():
                print(f"❌ Service directory not found: {service_dir}")
                return None
            
            # Check if main.py exists
            main_file = service_dir / "app" / "main.py"
            if not main_file.exists():
                print(f"❌ Main file not found: {main_file}")
                return None
            
            # Start the service
            cmd = [
                sys.executable, "-m", "uvicorn", 
                "app.main:app", 
                "--host", "0.0.0.0", 
                "--port", str(port),
                "--reload"
            ]
            
            process = subprocess.Popen(
                cmd,
                cwd=service_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes.append({
                'name': service_name,
                'port': port,
                'process': process,
                'working_dir': service_dir
            })
            
            print(f"✅ {service_name} started with PID {process.pid}")
            return process
            
        except Exception as e:
            print(f"❌ Failed to start {service_name}: {e}")
            return None
    
    def start_all_services(self):
        """Start all services"""
        print("🚀 Starting all Steam Clone services...")
        
        services = [
            ("user-service", 8001),
            ("game-catalog-service", 8002),
            ("review-service", 8003),
            ("shopping-service", 8004),
            ("purchase-service", 8005),
            ("payment-service", 8006),
            ("online-service", 8007),
            ("social-service", 8008),
            ("notification-service", 8009),
            ("recommendation-service", 8010),
            ("achievement-service", 8011),
            ("monitoring-service", 8012),
            ("api-gateway", 8000)
        ]
        
        started_services = []
        
        for service_name, port in services:
            process = self.start_service(service_name, port, f"services/{service_name}")
            if process:
                started_services.append((service_name, port))
                time.sleep(2)  # Give each service time to start
        
        print(f"\n✅ Started {len(started_services)} services:")
        for service_name, port in started_services:
            print(f"  - {service_name}: http://localhost:{port}")
        
        return started_services
    
    def monitor_services(self):
        """Monitor running services"""
        print("\n📊 Monitoring services...")
        
        while True:
            try:
                running_services = []
                for service_info in self.processes:
                    if service_info['process'].poll() is None:
                        running_services.append(service_info['name'])
                    else:
                        print(f"⚠️  {service_info['name']} has stopped")
                
                if running_services:
                    print(f"🟢 Running services: {', '.join(running_services)}")
                else:
                    print("🔴 No services running")
                
                time.sleep(10)
                
            except KeyboardInterrupt:
                print("\n🛑 Stopping all services...")
                self.stop_all_services()
                break
    
    def stop_all_services(self):
        """Stop all running services"""
        print("🛑 Stopping all services...")
        
        for service_info in self.processes:
            try:
                service_info['process'].terminate()
                service_info['process'].wait(timeout=5)
                print(f"✅ {service_info['name']} stopped")
            except subprocess.TimeoutExpired:
                service_info['process'].kill()
                print(f"🔴 {service_info['name']} force killed")
            except Exception as e:
                print(f"❌ Error stopping {service_info['name']}: {e}")
        
        self.processes.clear()
        print("✅ All services stopped")
    
    def run(self):
        """Run the service starter"""
        try:
            # Start all services
            started_services = self.start_all_services()
            
            if not started_services:
                print("❌ No services started successfully")
                return False
            
            print(f"\n🎉 Successfully started {len(started_services)} services!")
            print("📚 API Documentation available at:")
            for service_name, port in started_services:
                print(f"  - {service_name}: http://localhost:{port}/docs")
            
            print("\n⏹️  Press Ctrl+C to stop all services")
            
            # Monitor services
            self.monitor_services()
            
            return True
            
        except KeyboardInterrupt:
            print("\n🛑 Received interrupt signal")
            self.stop_all_services()
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            self.stop_all_services()
            return False

def main():
    """Main function"""
    starter = ServiceStarter()
    success = starter.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()