#!/bin/bash

# Comprehensive Setup and Test Script for Steam Clone
# This script sets up the entire environment, imports data, and tests all services

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a port is in use
port_in_use() {
    lsof -i :$1 >/dev/null 2>&1
}

# Function to wait for a service to be ready
wait_for_service() {
    local service_name=$1
    local port=$2
    local max_attempts=30
    local attempt=1
    
    log_info "Waiting for $service_name to be ready on port $port..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:$port/health >/dev/null 2>&1; then
            log_success "$service_name is ready!"
            return 0
        fi
        
        log_info "Attempt $attempt/$max_attempts - $service_name not ready yet, waiting 5 seconds..."
        sleep 5
        ((attempt++))
    done
    
    log_error "$service_name failed to start within expected time"
    return 1
}

# Function to check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if Docker is installed
    if ! command_exists docker; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check if Docker Compose is installed
    if ! command_exists docker-compose; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if Python is installed
    if ! command_exists python3; then
        log_error "Python 3 is not installed. Please install Python 3 first."
        exit 1
    fi
    
    # Check if pip is installed
    if ! command_exists pip3; then
        log_error "pip3 is not installed. Please install pip3 first."
        exit 1
    fi
    
    log_success "All prerequisites are installed"
}

# Function to install Python dependencies
install_dependencies() {
    log_info "Installing Python dependencies..."
    
    # Install global requirements
    if [ -f "requirements-global.txt" ]; then
        log_info "Installing global requirements..."
        pip3 install -r requirements-global.txt
    fi
    
    # Install service-specific requirements
    for service_dir in services/*/; do
        if [ -f "$service_dir/requirements.txt" ]; then
            log_info "Installing requirements for $(basename $service_dir)..."
            pip3 install -r "$service_dir/requirements.txt"
        fi
    done
    
    log_success "Python dependencies installed"
}

# Function to stop existing services
stop_existing_services() {
    log_info "Stopping existing services..."
    
    # Stop Docker Compose services
    if [ -f "docker-compose.yml" ]; then
        docker-compose down --remove-orphans || true
    fi
    
    # Kill any processes using our ports
    for port in 8000 8001 8002 8003 8004 8005 8006 8007 8008 8009 8010 8011 8012; do
        if port_in_use $port; then
            log_warning "Port $port is in use, attempting to free it..."
            lsof -ti:$port | xargs kill -9 2>/dev/null || true
        fi
    done
    
    log_success "Existing services stopped"
}

# Function to start infrastructure services
start_infrastructure() {
    log_info "Starting infrastructure services (databases, Redis, etc.)..."
    
    # Start only infrastructure services first
    docker-compose up -d user-db game-catalog-db review-db shopping-db purchase-db payment-db online-db social-db notification-db recommendation-db achievement-db monitoring-db redis elasticsearch zookeeper kafka
    
    # Wait for databases to be ready
    log_info "Waiting for databases to be ready..."
    sleep 30
    
    # Check if databases are ready
    for db_port in 5432 5433 5434 5435 5436 5437 5438 5439 5440 5441 5442 5443; do
        if ! port_in_use $db_port; then
            log_warning "Database on port $db_port may not be ready yet"
        fi
    done
    
    log_success "Infrastructure services started"
}

# Function to start microservices
start_microservices() {
    log_info "Starting microservices..."
    
    # Start all services
    docker-compose up -d
    
    # Wait for services to be ready
    log_info "Waiting for microservices to be ready..."
    
    # Wait for each service
    wait_for_service "API Gateway" 8000
    wait_for_service "User Service" 8001
    wait_for_service "Game Catalog Service" 8002
    wait_for_service "Review Service" 8003
    wait_for_service "Shopping Service" 8004
    wait_for_service "Purchase Service" 8005
    wait_for_service "Payment Service" 8006
    wait_for_service "Online Service" 8007
    wait_for_service "Social Service" 8008
    wait_for_service "Notification Service" 8009
    wait_for_service "Recommendation Service" 8010
    wait_for_service "Achievement Service" 8011
    wait_for_service "Monitoring Service" 8012
    
    log_success "All microservices started"
}

# Function to import data
import_data() {
    log_info "Importing SteamDB data..."
    
    # Make the data importer executable
    chmod +x scripts/steamdb_data_importer.py
    
    # Run the data importer
    python3 scripts/steamdb_data_importer.py
    
    if [ $? -eq 0 ]; then
        log_success "Data import completed successfully"
    else
        log_error "Data import failed"
        return 1
    fi
}

# Function to run tests
run_tests() {
    log_info "Running comprehensive tests..."
    
    # Make the test script executable
    chmod +x scripts/test_all_services.py
    
    # Run the test script
    python3 scripts/test_all_services.py
    
    if [ $? -eq 0 ]; then
        log_success "All tests completed successfully"
    else
        log_warning "Some tests failed, but continuing..."
    fi
}

# Function to show service URLs
show_service_urls() {
    log_info "Service URLs:"
    echo ""
    echo "🌐 API Gateway: http://localhost:8000"
    echo "📚 API Documentation: http://localhost:8000/docs"
    echo ""
    echo "🔧 Individual Services:"
    echo "  👤 User Service: http://localhost:8001"
    echo "  🎮 Game Catalog Service: http://localhost:8002"
    echo "  ⭐ Review Service: http://localhost:8003"
    echo "  🛒 Shopping Service: http://localhost:8004"
    echo "  💳 Purchase Service: http://localhost:8005"
    echo "  💰 Payment Service: http://localhost:8006"
    echo "  🌐 Online Service: http://localhost:8007"
    echo "  👥 Social Service: http://localhost:8008"
    echo "  🔔 Notification Service: http://localhost:8009"
    echo "  🎯 Recommendation Service: http://localhost:8010"
    echo "  🏆 Achievement Service: http://localhost:8011"
    echo "  📊 Monitoring Service: http://localhost:8012"
    echo ""
    echo "📚 Individual Swagger Docs:"
    echo "  👤 User Service: http://localhost:8001/docs"
    echo "  🎮 Game Catalog Service: http://localhost:8002/docs"
    echo "  ⭐ Review Service: http://localhost:8003/docs"
    echo "  🛒 Shopping Service: http://localhost:8004/docs"
    echo "  💳 Purchase Service: http://localhost:8005/docs"
    echo "  💰 Payment Service: http://localhost:8006/docs"
    echo "  🌐 Online Service: http://localhost:8007/docs"
    echo "  👥 Social Service: http://localhost:8008/docs"
    echo "  🔔 Notification Service: http://localhost:8009/docs"
    echo "  🎯 Recommendation Service: http://localhost:8010/docs"
    echo "  🏆 Achievement Service: http://localhost:8011/docs"
    echo "  📊 Monitoring Service: http://localhost:8012/docs"
    echo ""
}

# Function to show logs
show_logs() {
    log_info "Showing service logs (press Ctrl+C to exit)..."
    docker-compose logs -f
}

# Function to cleanup
cleanup() {
    log_info "Cleaning up..."
    docker-compose down --remove-orphans
    log_success "Cleanup completed"
}

# Main function
main() {
    echo "🚀 Steam Clone - Comprehensive Setup and Test Script"
    echo "=================================================="
    echo ""
    
    # Parse command line arguments
    case "${1:-setup}" in
        "setup")
            check_prerequisites
            install_dependencies
            stop_existing_services
            start_infrastructure
            start_microservices
            import_data
            run_tests
            show_service_urls
            ;;
        "test")
            run_tests
            ;;
        "import")
            import_data
            ;;
        "start")
            start_infrastructure
            start_microservices
            ;;
        "stop")
            stop_existing_services
            ;;
        "restart")
            stop_existing_services
            start_infrastructure
            start_microservices
            ;;
        "logs")
            show_logs
            ;;
        "cleanup")
            cleanup
            ;;
        "urls")
            show_service_urls
            ;;
        *)
            echo "Usage: $0 {setup|test|import|start|stop|restart|logs|cleanup|urls}"
            echo ""
            echo "Commands:"
            echo "  setup    - Complete setup (default)"
            echo "  test     - Run tests only"
            echo "  import   - Import data only"
            echo "  start    - Start services only"
            echo "  stop     - Stop services only"
            echo "  restart  - Restart services"
            echo "  logs     - Show service logs"
            echo "  cleanup  - Clean up everything"
            echo "  urls     - Show service URLs"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"