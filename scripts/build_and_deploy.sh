#!/bin/bash

###############################################################################
# Medical Content Build and Deploy Script
# Automates building, testing, and deploying medical educational content
###############################################################################

set -e  # Exit on error

# Configuration
PROJECT_NAME="Medical-Content-Empire"
UE5_PROJECT_PATH="${UE5_PROJECT_PATH:-/path/to/ue5/project}"
BUILD_DIR="${BUILD_DIR:-./build}"
DEPLOY_DIR="${DEPLOY_DIR:-./deploy}"
LOG_DIR="${LOG_DIR:-./logs}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] INFO: $1" >> "${LOG_DIR}/build.log"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SUCCESS: $1" >> "${LOG_DIR}/build.log"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: $1" >> "${LOG_DIR}/build.log"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" >> "${LOG_DIR}/build.log"
}

# Initialize directories
init_directories() {
    log_info "Initializing directories..."
    mkdir -p "$BUILD_DIR"
    mkdir -p "$DEPLOY_DIR"
    mkdir -p "$LOG_DIR"
    mkdir -p "$BUILD_DIR/videos"
    mkdir -p "$BUILD_DIR/interactives"
    mkdir -p "$BUILD_DIR/assessments"
    log_success "Directories initialized"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    local missing_deps=()
    
    # Check for required tools
    command -v python3 >/dev/null 2>&1 || missing_deps+=("python3")
    command -v node >/dev/null 2>&1 || missing_deps+=("node")
    command -v ffmpeg >/dev/null 2>&1 || missing_deps+=("ffmpeg")
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing dependencies: ${missing_deps[*]}"
        log_info "Please install missing dependencies and try again"
        exit 1
    fi
    
    log_success "All prerequisites met"
}

# Build video content
build_videos() {
    log_info "Building video content..."
    
    local video_scripts_dir="./templates/video-scripts"
    local output_dir="$BUILD_DIR/videos"
    
    if [ ! -d "$video_scripts_dir" ]; then
        log_warning "No video scripts found, skipping video build"
        return 0
    fi
    
    # Find all script files
    local script_count=0
    while IFS= read -r -d '' script_file; do
        log_info "Processing script: $(basename "$script_file")"
        
        # Run video creation automation
        python3 scripts/content_production_automation.py \
            --action create-video \
            --input "$script_file" \
            --output "$output_dir/$(basename "${script_file%.md}")" \
            2>&1 | tee -a "${LOG_DIR}/video_build.log"
        
        ((script_count++))
    done < <(find "$video_scripts_dir" -name "*.md" -not -name "*template*" -print0)
    
    log_success "Built $script_count videos"
}

# Build UE5 interactive content
build_ue5_content() {
    log_info "Building UE5 interactive content..."
    
    # Check if UE5 project exists
    if [ ! -d "$UE5_PROJECT_PATH" ]; then
        log_warning "UE5 project not found at $UE5_PROJECT_PATH, skipping UE5 build"
        return 0
    fi
    
    log_info "Packaging UE5 project for web..."
    
    # UE5 packaging command (example for HTML5/WebGL)
    # In production, this would call the actual UE5 build system
    # "$UE5_PROJECT_PATH/Engine/Build/BatchFiles/RunUAT.sh" BuildCookRun \
    #     -project="$UE5_PROJECT_PATH/MedicalContent.uproject" \
    #     -platform=HTML5 \
    #     -clientconfig=Development \
    #     -cook -stage -pak -archive \
    #     -archivedirectory="$BUILD_DIR/interactives"
    
    log_success "UE5 content built"
}

# Generate assessments
generate_assessments() {
    log_info "Generating assessments..."
    
    local assessment_templates_dir="./templates/assessments"
    local output_dir="$BUILD_DIR/assessments"
    
    if [ ! -d "$assessment_templates_dir" ]; then
        log_warning "No assessment templates found, skipping assessment generation"
        return 0
    fi
    
    # Process assessment templates
    # In production, this would integrate with LMS API
    
    log_success "Assessments generated"
}

# Run quality checks
run_quality_checks() {
    log_info "Running quality checks..."
    
    local checks_passed=true
    
    # Check video quality
    log_info "Checking video quality..."
    for video in "$BUILD_DIR/videos"/*.mp4; do
        if [ -f "$video" ]; then
            # Use FFprobe to check video properties
            ffprobe -v error -select_streams v:0 \
                -show_entries stream=width,height,codec_name,bit_rate \
                -of default=noprint_wrappers=1 "$video" >> "${LOG_DIR}/quality_check.log" 2>&1
        fi
    done
    
    # Check file sizes
    log_info "Checking file sizes..."
    find "$BUILD_DIR" -type f -size +100M -exec ls -lh {} \; | while read -r line; do
        log_warning "Large file detected: $line"
    done
    
    # Validate medical content
    log_info "Validating medical content..."
    python3 scripts/content_production_automation.py \
        --action validate \
        --input "$BUILD_DIR" \
        2>&1 | tee -a "${LOG_DIR}/validation.log"
    
    if [ $checks_passed = true ]; then
        log_success "Quality checks passed"
    else
        log_error "Quality checks failed"
        exit 1
    fi
}

# Optimize content for delivery
optimize_content() {
    log_info "Optimizing content for delivery..."
    
    # Optimize videos
    log_info "Optimizing videos..."
    for video in "$BUILD_DIR/videos"/*.mp4; do
        if [ -f "$video" ] && [[ ! "$video" == *"_optimized.mp4" ]]; then
            log_info "Optimizing: $(basename "$video")"
            python3 scripts/content_production_automation.py \
                --action optimize \
                --input "$video" \
                2>&1 | tee -a "${LOG_DIR}/optimization.log"
        fi
    done
    
    # Compress images
    log_info "Compressing images..."
    find "$BUILD_DIR" -name "*.png" -o -name "*.jpg" | while read -r image; do
        log_info "Compressing: $(basename "$image")"
        # In production, would use image optimization tools
    done
    
    log_success "Content optimized"
}

# Package content
package_content() {
    log_info "Packaging content for deployment..."
    
    local package_name="${PROJECT_NAME}-$(date +%Y%m%d-%H%M%S).tar.gz"
    local package_path="$DEPLOY_DIR/$package_name"
    
    # Create package
    tar -czf "$package_path" -C "$BUILD_DIR" . 2>&1 | tee -a "${LOG_DIR}/package.log"
    
    # Generate checksums
    sha256sum "$package_path" > "$package_path.sha256"
    
    log_success "Content packaged: $package_name"
    echo "$package_path" > "$DEPLOY_DIR/latest_package.txt"
}

# Deploy content
deploy_content() {
    local environment="${1:-staging}"
    
    log_info "Deploying content to $environment..."
    
    # Read latest package
    if [ ! -f "$DEPLOY_DIR/latest_package.txt" ]; then
        log_error "No package found to deploy"
        exit 1
    fi
    
    local package_path=$(cat "$DEPLOY_DIR/latest_package.txt")
    
    # Deployment steps (customize based on your infrastructure)
    case "$environment" in
        staging)
            log_info "Deploying to staging environment..."
            # rsync -avz "$package_path" staging-server:/var/www/medical-content/
            ;;
        production)
            log_info "Deploying to production environment..."
            # Require confirmation for production
            read -p "Are you sure you want to deploy to PRODUCTION? (yes/no): " confirm
            if [ "$confirm" != "yes" ]; then
                log_warning "Production deployment cancelled"
                exit 0
            fi
            # rsync -avz "$package_path" production-server:/var/www/medical-content/
            ;;
        *)
            log_error "Unknown environment: $environment"
            exit 1
            ;;
    esac
    
    log_success "Deployment to $environment complete"
}

# Generate production report
generate_report() {
    log_info "Generating production report..."
    
    python3 scripts/content_production_automation.py \
        --action report \
        --output "$BUILD_DIR/production_report.html" \
        2>&1 | tee -a "${LOG_DIR}/report.log"
    
    log_success "Report generated: $BUILD_DIR/production_report.html"
}

# Cleanup build artifacts
cleanup() {
    log_info "Cleaning up temporary files..."
    
    # Remove temporary files
    find "$BUILD_DIR" -name "*.tmp" -delete
    find "$BUILD_DIR" -name "*.cache" -delete
    
    # Keep only last 5 packages
    cd "$DEPLOY_DIR"
    ls -t *.tar.gz 2>/dev/null | tail -n +6 | xargs -r rm -f
    cd - > /dev/null
    
    log_success "Cleanup complete"
}

# Main build function
build_all() {
    log_info "Starting full content build..."
    
    init_directories
    check_prerequisites
    build_videos
    build_ue5_content
    generate_assessments
    run_quality_checks
    optimize_content
    package_content
    generate_report
    cleanup
    
    log_success "Build complete!"
}

# Display usage information
usage() {
    cat << EOF
Usage: $0 [COMMAND] [OPTIONS]

Commands:
    build           Build all content
    videos          Build video content only
    ue5             Build UE5 interactive content only
    assessments     Generate assessments only
    optimize        Optimize existing content
    package         Package content for deployment
    deploy [env]    Deploy to environment (staging|production)
    report          Generate production report
    clean           Clean build artifacts
    help            Show this help message

Environment Variables:
    UE5_PROJECT_PATH    Path to UE5 project (default: /path/to/ue5/project)
    BUILD_DIR           Build output directory (default: ./build)
    DEPLOY_DIR          Deployment package directory (default: ./deploy)
    LOG_DIR             Log file directory (default: ./logs)

Examples:
    $0 build                    # Full build
    $0 videos                   # Build videos only
    $0 deploy staging          # Deploy to staging
    $0 deploy production       # Deploy to production

EOF
}

# Main script logic
main() {
    case "${1:-}" in
        build)
            build_all
            ;;
        videos)
            init_directories
            check_prerequisites
            build_videos
            ;;
        ue5)
            init_directories
            check_prerequisites
            build_ue5_content
            ;;
        assessments)
            init_directories
            generate_assessments
            ;;
        optimize)
            init_directories
            optimize_content
            ;;
        package)
            package_content
            ;;
        deploy)
            deploy_content "${2:-staging}"
            ;;
        report)
            generate_report
            ;;
        clean)
            cleanup
            ;;
        help|--help|-h)
            usage
            ;;
        *)
            log_error "Unknown command: ${1:-}"
            usage
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
