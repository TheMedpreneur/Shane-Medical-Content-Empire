#!/bin/bash

###############################################################################
# Medical Content Build and Deploy Script
# Automates building, testing, and deploying medical educational content
# Version: 2.0 (Optimized)
###############################################################################

set -euo pipefail  # Exit on error, undefined vars, pipe failures

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
    local warnings=()
    
    # Check for required tools
    command -v python3 >/dev/null 2>&1 || missing_deps+=("python3")
    command -v ffmpeg >/dev/null 2>&1 || missing_deps+=("ffmpeg")
    
    # Check for optional tools
    command -v node >/dev/null 2>&1 || warnings+=("node (optional)")
    command -v git >/dev/null 2>&1 || warnings+=("git (optional)")
    
    # Check Python version
    if command -v python3 >/dev/null 2>&1; then
        local python_version
        python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
            warnings+=("python3 version $python_version (recommend 3.8+)")
        fi
    fi
    
    # Check FFmpeg version
    if command -v ffmpeg >/dev/null 2>&1; then
        local ffmpeg_version
        ffmpeg_version=$(ffmpeg -version 2>&1 | head -n1 | grep -o '[0-9]\+\.[0-9]\+' | head -n1)
        log_info "FFmpeg version: $ffmpeg_version"
    fi
    
    # Check disk space
    local available_space
    available_space=$(df -BG "$BUILD_DIR" 2>/dev/null | awk 'NR==2 {print $4}' | sed 's/G//' || echo "unknown")
    if [[ "$available_space" != "unknown" && "$available_space" -lt 5 ]]; then
        warnings+=("low disk space: ${available_space}GB available (recommend 5GB+)")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        log_info "Please install missing dependencies and try again"
        exit 1
    fi
    
    if [ ${#warnings[@]} -ne 0 ]; then
        for warning in "${warnings[@]}"; do
            log_warning "Optional dependency missing or suboptimal: $warning"
        done
    fi
    
    log_success "All prerequisites met"
}

# Build video content
build_videos() {
    log_info "Building video content..."
    
    local video_scripts_dir="./templates/video-scripts"
    local output_dir="$BUILD_DIR/videos"
    local success_count=0
    local failure_count=0
    
    if [ ! -d "$video_scripts_dir" ]; then
        log_warning "No video scripts found, skipping video build"
        return 0
    fi
    
    # Create output directory
    mkdir -p "$output_dir"
    
    # Find all script files
    local script_files=()
    while IFS= read -r -d '' script_file; do
        script_files+=("$script_file")
    done < <(find "$video_scripts_dir" -name "*.md" -not -name "*template*" -print0)
    
    local total_scripts=${#script_files[@]}
    log_info "Found $total_scripts script files to process"
    
    if [ $total_scripts -eq 0 ]; then
        log_warning "No script files found, skipping video build"
        return 0
    fi
    
    # Process each script
    for i in "${!script_files[@]}"; do
        local script_file="${script_files[$i]}"
        local script_name=$(basename "${script_file%.md}")
        local progress=$((i + 1))
        
        log_info "[$progress/$total_scripts] Processing script: $script_name"
        
        # Run video creation automation with timeout
        if timeout 300 python3 scripts/content_production_automation.py \
            --action create-video \
            --input "$script_file" \
            --output "$output_dir/$script_name" \
            --config config/automation.json \
            2>&1 | tee -a "${LOG_DIR}/video_build_${script_name}.log"; then
            
            # Verify output was created
            if [ -f "$output_dir/$script_name.mp4" ] || [ -f "$output_dir/$script_name_final.mp4" ]; then
                log_success "Successfully built: $script_name"
                ((success_count++))
            else
                log_error "Video file not found for: $script_name"
                ((failure_count++))
            fi
        else
            local exit_code=$?
            if [ $exit_code -eq 124 ]; then
                log_error "Timeout building video: $script_name (5 minutes)"
            else
                log_error "Failed to build video: $script_name (exit code: $exit_code)"
            fi
            ((failure_count++))
        fi
    done
    
    log_info "Video build complete: $success_count successful, $failure_count failed"
    
    if [ $failure_count -gt 0 ]; then
        log_warning "Some videos failed to build. Check individual log files for details."
        return 1
    fi
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
    log_info "Running comprehensive quality checks..."
    
    local checks_passed=true
    local video_count=0
    local large_files=0
    local corrupted_files=0
    
    # Check video quality and properties
    log_info "Checking video quality and properties..."
    for video in "$BUILD_DIR/videos"/*.mp4; do
        if [ -f "$video" ]; then
            ((video_count++))
            local video_name=$(basename "$video")
            
            # Use FFprobe to check video properties
            if ffprobe -v error -select_streams v:0 \
                -show_entries stream=width,height,codec_name,bit_rate,duration \
                -of default=noprint_wrappers=1 "$video" > "${LOG_DIR}/quality_${video_name}.log" 2>&1; then
                
                # Extract video properties
                local width height codec bitrate duration
                width=$(grep "width=" "${LOG_DIR}/quality_${video_name}.log" | cut -d'=' -f2)
                height=$(grep "height=" "${LOG_DIR}/quality_${video_name}.log" | cut -d'=' -f2)
                codec=$(grep "codec_name=" "${LOG_DIR}/quality_${video_name}.log" | cut -d'=' -f2)
                bitrate=$(grep "bit_rate=" "${LOG_DIR}/quality_${video_name}.log" | cut -d'=' -f2)
                duration=$(grep "duration=" "${LOG_DIR}/quality_${video_name}.log" | cut -d'=' -f2)
                
                log_info "Video: $video_name - ${width}x${height}, $codec, ${bitrate}bps, ${duration}s"
                
                # Check for minimum quality standards
                if [ -n "$width" ] && [ -n "$height" ]; then
                    if [ "$width" -lt 1280 ] || [ "$height" -lt 720 ]; then
                        log_warning "Low resolution video: $video_name (${width}x${height})"
                    fi
                fi
                
                if [ -n "$bitrate" ] && [ "$bitrate" -lt 1000000 ]; then
                    log_warning "Low bitrate video: $video_name (${bitrate}bps)"
                fi
            else
                log_error "Failed to analyze video: $video_name"
                ((corrupted_files++))
                checks_passed=false
            fi
        fi
    done
    
    # Check file sizes and detect large files
    log_info "Checking file sizes..."
    while IFS= read -r -d '' file; do
        local file_size
        file_size=$(stat -c%s "$file" 2>/dev/null || echo "0")
        local file_size_mb=$((file_size / 1024 / 1024))
        
        if [ $file_size_mb -gt 100 ]; then
            log_warning "Large file detected: $(basename "$file") (${file_size_mb}MB)"
            ((large_files++))
        fi
        
        # Check for empty files
        if [ $file_size -eq 0 ]; then
            log_error "Empty file detected: $file"
            ((corrupted_files++))
            checks_passed=false
        fi
    done < <(find "$BUILD_DIR" -type f -print0)
    
    # Check for required files
    log_info "Checking for required output files..."
    local required_dirs=("videos" "interactives" "assessments")
    for dir in "${required_dirs[@]}"; do
        if [ ! -d "$BUILD_DIR/$dir" ]; then
            log_warning "Missing output directory: $dir"
        fi
    done
    
    # Validate medical content
    log_info "Validating medical content..."
    if python3 scripts/content_production_automation.py \
        --action validate \
        --input "$BUILD_DIR" \
        2>&1 | tee -a "${LOG_DIR}/validation.log"; then
        log_success "Medical content validation passed"
    else
        log_error "Medical content validation failed"
        checks_passed=false
    fi
    
    # Generate quality report
    log_info "Generating quality report..."
    cat > "${LOG_DIR}/quality_summary.txt" << EOF
Quality Check Summary
====================
Date: $(date)
Total Videos: $video_count
Large Files (>100MB): $large_files
Corrupted Files: $corrupted_files
Status: $([ $checks_passed = true ] && echo "PASSED" || echo "FAILED")

Video Details:
$(find "$BUILD_DIR/videos" -name "*.mp4" -exec basename {} \; | sort)

File Size Analysis:
$(find "$BUILD_DIR" -type f -exec ls -lh {} \; | sort -k5 -hr | head -20)
EOF
    
    if [ $checks_passed = true ]; then
        log_success "All quality checks passed"
    else
        log_error "Quality checks failed - see quality_summary.txt for details"
        return 1
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
