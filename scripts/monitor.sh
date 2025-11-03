#!/bin/bash

# True North Audio - Comprehensive Service Monitor
# Tracks: install, lint, test, build, serve, and clean processes
# Shows real-time status for Backend, Frontend, FastAPI, and Ollama

# Colors and formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GRAY='\033[0;90m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m' # No Color

# Log files
BACKEND_LOG="/tmp/backend.log"
FRONTEND_LOG="/tmp/frontend.log"
FASTAPI_LOG="/tmp/fastapi.log"
OLLAMA_LOG="/tmp/ollama.log"

# Status tracking
declare -A SERVICE_STATUS
declare -A SERVICE_PID
declare -A SERVICE_PORT
declare -A SERVICE_ACTIVITY

# Initialize services
SERVICES=("Backend" "Frontend" "FastAPI" "Ollama")
SERVICE_STATUS["Backend"]="⚫ Stopped"
SERVICE_STATUS["Frontend"]="⚫ Stopped"
SERVICE_STATUS["FastAPI"]="⚫ Stopped"
SERVICE_STATUS["Ollama"]="⚫ Stopped"

SERVICE_PORT["Backend"]="3000"
SERVICE_PORT["Frontend"]="4200"
SERVICE_PORT["FastAPI"]="8000"
SERVICE_PORT["Ollama"]="11434"

# Clear screen and setup
clear_screen() {
    clear
    tput cup 0 0
}

# Header
print_header() {
    echo -e "${BOLD}${CYAN}"
    echo "╔════════════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                                ║"
    echo "║              🎵 TRUE NORTH AUDIO - COMPREHENSIVE SERVICE MONITOR              ║"
    echo "║                                                                                ║"
    echo "╚════════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Check if service is running
check_service() {
    local service=$1
    local port=${SERVICE_PORT[$service]}
    local log_file=""
    
    case $service in
        "Backend")    log_file=$BACKEND_LOG ;;
        "Frontend")   log_file=$FRONTEND_LOG ;;
        "FastAPI")    log_file=$FASTAPI_LOG ;;
        "Ollama")     log_file=$OLLAMA_LOG ;;
    esac
    
    # Check if port is in use
    if lsof -i :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        PID=$(lsof -i :$port -sTCP:LISTEN -t | head -1)
        SERVICE_PID[$service]=$PID
        
        # Check activity in log
        if [ -f "$log_file" ]; then
            RECENT=$(tail -1 "$log_file" 2>/dev/null)
            
            # Check for specific activity indicators
            if echo "$RECENT" | grep -qiE "error|failed|exception"; then
                SERVICE_STATUS[$service]="🔴 Error"
            elif echo "$RECENT" | grep -qiE "compiling|building|installing"; then
                SERVICE_STATUS[$service]="🔨 Building"
            elif echo "$RECENT" | grep -qiE "testing|test"; then
                SERVICE_STATUS[$service]="🧪 Testing"
            elif echo "$RECENT" | grep -qiE "lint|linting"; then
                SERVICE_STATUS[$service]="🔍 Linting"
            elif echo "$RECENT" | grep -qiE "download|installing"; then
                SERVICE_STATUS[$service]="📦 Installing"
            elif echo "$RECENT" | grep -qiE "running|listening|ready|started"; then
                SERVICE_STATUS[$service]="🟢 Running"
            else
                SERVICE_STATUS[$service]="🟡 Active"
            fi
            
            SERVICE_ACTIVITY[$service]="$RECENT"
        else
            SERVICE_STATUS[$service]="🟢 Running"
            SERVICE_ACTIVITY[$service]="No log data"
        fi
    else
        SERVICE_STATUS[$service]="⚫ Stopped"
        SERVICE_PID[$service]="-"
        SERVICE_ACTIVITY[$service]="Not running"
    fi
}

# Print service status table
print_status_table() {
    echo -e "\n${BOLD}${WHITE}SERVICE STATUS:${NC}"
    echo -e "${GRAY}─────────────────────────────────────────────────────────────────────────────────${NC}"
    printf "${BOLD}%-15s %-12s %-10s %-8s %-40s${NC}\n" "SERVICE" "STATUS" "PORT" "PID" "LAST ACTIVITY"
    echo -e "${GRAY}─────────────────────────────────────────────────────────────────────────────────${NC}"
    
    for service in "${SERVICES[@]}"; do
        local status="${SERVICE_STATUS[$service]}"
        local port="${SERVICE_PORT[$service]}"
        local pid="${SERVICE_PID[$service]:-"-"}"
        local activity="${SERVICE_ACTIVITY[$service]:-"No activity"}"
        
        # Truncate activity to fit
        if [ ${#activity} -gt 40 ]; then
            activity="${activity:0:37}..."
        fi
        
        # Color code based on status
        if [[ $status == *"Running"* ]]; then
            printf "${GREEN}%-15s %-12s %-10s %-8s${NC} ${DIM}%-40s${NC}\n" "$service" "$status" "$port" "$pid" "$activity"
        elif [[ $status == *"Error"* ]]; then
            printf "${RED}%-15s %-12s %-10s %-8s${NC} ${DIM}%-40s${NC}\n" "$service" "$status" "$port" "$pid" "$activity"
        elif [[ $status == *"Building"* ]] || [[ $status == *"Testing"* ]] || [[ $status == *"Installing"* ]]; then
            printf "${YELLOW}%-15s %-12s %-10s %-8s${NC} ${DIM}%-40s${NC}\n" "$service" "$status" "$port" "$pid" "$activity"
        elif [[ $status == *"Active"* ]]; then
            printf "${CYAN}%-15s %-12s %-10s %-8s${NC} ${DIM}%-40s${NC}\n" "$service" "$status" "$port" "$pid" "$activity"
        else
            printf "${GRAY}%-15s %-12s %-10s %-8s %-40s${NC}\n" "$service" "$status" "$port" "$pid" "$activity"
        fi
    done
    
    echo -e "${GRAY}─────────────────────────────────────────────────────────────────────────────────${NC}"
}

# Print recent log activity with highlighting
print_recent_activity() {
    echo -e "\n${BOLD}${WHITE}RECENT ACTIVITY:${NC}"
    echo -e "${GRAY}═════════════════════════════════════════════════════════════════════════════════${NC}\n"
    
    for service in "${SERVICES[@]}"; do
        local log_file=""
        case $service in
            "Backend")    log_file=$BACKEND_LOG ;;
            "Frontend")   log_file=$FRONTEND_LOG ;;
            "FastAPI")    log_file=$FASTAPI_LOG ;;
            "Ollama")     log_file=$OLLAMA_LOG ;;
        esac
        
        if [ -f "$log_file" ]; then
            echo -e "${BOLD}${BLUE}[$service]${NC}"
            
            # Get last 5 lines and highlight important keywords
            tail -5 "$log_file" 2>/dev/null | while IFS= read -r line; do
                # Highlight errors
                line=$(echo "$line" | sed -E "s/(error|ERROR|failed|FAILED|exception|Exception)/${RED}\1${NC}/gi")
                # Highlight success
                line=$(echo "$line" | sed -E "s/(success|SUCCESS|complete|COMPLETE|ready|READY|started|STARTED)/${GREEN}\1${NC}/gi")
                # Highlight warnings
                line=$(echo "$line" | sed -E "s/(warning|WARNING|warn|WARN)/${YELLOW}\1${NC}/gi")
                # Highlight building/compiling
                line=$(echo "$line" | sed -E "s/(compiling|building|installing|downloading)/${CYAN}\1${NC}/gi")
                
                echo -e "  ${DIM}${line}${NC}"
            done
            echo ""
        fi
    done
}

# Print process summary
print_process_summary() {
    echo -e "${BOLD}${WHITE}PROCESS TRACKING:${NC}"
    echo -e "${GRAY}─────────────────────────────────────────────────────────────────────────────────${NC}"
    
    # Count active processes
    local node_count=$(pgrep -f "node" | wc -l)
    local python_count=$(pgrep -f "python" | wc -l)
    local npm_count=$(pgrep -f "npm|pnpm" | wc -l)
    
    echo -e "  Node.js processes:    ${GREEN}$node_count${NC}"
    echo -e "  Python processes:     ${GREEN}$python_count${NC}"
    echo -e "  Package managers:     ${GREEN}$npm_count${NC}"
    
    echo -e "${GRAY}─────────────────────────────────────────────────────────────────────────────────${NC}"
}

# Print help footer
print_footer() {
    echo -e "\n${BOLD}${WHITE}COMMANDS:${NC}"
    echo -e "  ${GREEN}r${NC} - Refresh now    ${GREEN}q${NC} - Quit    ${GREEN}l${NC} - View logs    ${GREEN}s${NC} - Start services"
    echo -e "\n${DIM}Auto-refreshing every 2 seconds... Press any key to force refresh${NC}"
}

# View detailed logs
view_logs() {
    clear_screen
    print_header
    echo -e "\n${BOLD}${WHITE}DETAILED LOGS:${NC}\n"
    
    echo -e "${BOLD}${BLUE}Select service:${NC}"
    echo "  1) Backend"
    echo "  2) Frontend"
    echo "  3) FastAPI"
    echo "  4) Ollama"
    echo "  5) Back to monitor"
    
    read -p "Choice: " -n 1 -r choice
    echo ""
    
    case $choice in
        1) less +F $BACKEND_LOG ;;
        2) less +F $FRONTEND_LOG ;;
        3) less +F $FASTAPI_LOG ;;
        4) less +F $OLLAMA_LOG ;;
        *) return ;;
    esac
}

# Start services
start_services() {
    echo -e "\n${YELLOW}Starting all services...${NC}"
    npm run serve:all &
    sleep 2
}

# Main monitoring loop
monitor_loop() {
    while true; do
        clear_screen
        print_header
        
        # Update service status
        for service in "${SERVICES[@]}"; do
            check_service "$service"
        done
        
        print_status_table
        print_recent_activity
        print_process_summary
        print_footer
        
        # Wait for input or timeout
        read -t 2 -n 1 key
        
        case $key in
            q|Q) 
                clear
                echo "Exiting monitor..."
                exit 0
                ;;
            r|R)
                continue
                ;;
            l|L)
                view_logs
                ;;
            s|S)
                start_services
                ;;
        esac
    done
}

# Cleanup on exit
cleanup() {
    clear
    echo "Monitor stopped."
    exit 0
}

trap cleanup INT TERM

# Start monitoring
echo "Starting True North Audio Monitor..."
sleep 1
monitor_loop

# True North Audio - Service Monitor
# Real-time monitoring of all services with colored output and activity tracking

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Clear screen and hide cursor
clear
tput civis

# Trap to restore cursor on exit
trap 'tput cnorm; exit' INT TERM EXIT

# Header
print_header() {
    clear
    echo -e "${CYAN}╔════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${WHITE}              🎵 TRUE NORTH AUDIO - SERVICE MONITOR                       ${CYAN}║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Check if service is running
check_service() {
    local port=$1
    local name=$2
    local pid_var=$3
    
    # Check if PID exists and is running
    if [ ! -z "${!pid_var}" ] && ps -p ${!pid_var} > /dev/null 2>&1; then
        # Check if port is responding
        if curl -s -o /dev/null -m 1 http://localhost:${port} 2>/dev/null; then
            echo -e "${GREEN}●${NC} ${BOLD}${name}${NC} ${GRAY}(PID: ${!pid_var})${NC} - ${GREEN}Running & Responding${NC}"
        else
            echo -e "${YELLOW}●${NC} ${BOLD}${name}${NC} ${GRAY}(PID: ${!pid_var})${NC} - ${YELLOW}Starting...${NC}"
        fi
    else
        echo -e "${RED}●${NC} ${BOLD}${name}${NC} - ${RED}Not Running${NC}"
    fi
}

# Get last N lines from log with color coding
get_log_activity() {
    local logfile=$1
    local lines=${2:-3}
    
    if [ -f "$logfile" ]; then
        tail -n $lines "$logfile" 2>/dev/null | while IFS= read -r line; do
            # Color code based on content
            if echo "$line" | grep -qi "error\|fail\|exception"; then
                echo -e "    ${RED}│${NC} ${GRAY}${line}${NC}"
            elif echo "$line" | grep -qi "warn\|warning"; then
                echo -e "    ${YELLOW}│${NC} ${GRAY}${line}${NC}"
            elif echo "$line" | grep -qi "success\|complete\|ready\|listening"; then
                echo -e "    ${GREEN}│${NC} ${GRAY}${line}${NC}"
            elif echo "$line" | grep -qi "log\|info"; then
                echo -e "    ${BLUE}│${NC} ${GRAY}${line}${NC}"
            else
                echo -e "    ${GRAY}│ ${line}${NC}"
            fi
        done
    else
        echo -e "    ${GRAY}│ No log file${NC}"
    fi
}

# Get CPU and Memory usage for PID
get_process_stats() {
    local pid=$1
    if [ ! -z "$pid" ] && ps -p $pid > /dev/null 2>&1; then
        local stats=$(ps -p $pid -o %cpu,%mem,rss | tail -n 1)
        local cpu=$(echo $stats | awk '{print $1}')
        local mem=$(echo $stats | awk '{print $2}')
        local rss=$(echo $stats | awk '{print $3}')
        local rss_mb=$((rss / 1024))
        echo -e "${GRAY}CPU: ${cpu}% | MEM: ${mem}% (${rss_mb}MB)${NC}"
    else
        echo -e "${GRAY}N/A${NC}"
    fi
}

# Count requests in log
count_requests() {
    local logfile=$1
    local time_window=${2:-60} # default 60 seconds
    
    if [ -f "$logfile" ]; then
        local count=$(grep -c "GET\|POST\|PUT\|DELETE" "$logfile" 2>/dev/null || echo "0")
        echo -e "${CYAN}${count} requests${NC}"
    else
        echo -e "${GRAY}0 requests${NC}"
    fi
}

# Monitor function
monitor_services() {
    # Read PIDs from temp file if exists
    if [ -f /tmp/tn-pids.txt ]; then
        source /tmp/tn-pids.txt
    fi
    
    while true; do
        print_header
        
        # Current time
        echo -e "${GRAY}Last updated: $(date '+%Y-%m-%d %H:%M:%S')${NC}"
        echo ""
        
        # Service Status Section
        echo -e "${CYAN}┌─ SERVICE STATUS ──────────────────────────────────────────────────────────┐${NC}"
        echo ""
        check_service 3000 "Backend (NestJS)" "BACKEND_PID"
        echo "  $(get_process_stats "$BACKEND_PID")"
        echo "  $(count_requests "/tmp/backend.log")"
        get_log_activity "/tmp/backend.log" 2
        echo ""
        
        check_service 4200 "Frontend (Angular)" "FRONTEND_PID"
        echo "  $(get_process_stats "$FRONTEND_PID")"
        echo "  $(count_requests "/tmp/frontend.log")"
        get_log_activity "/tmp/frontend.log" 2
        echo ""
        
        check_service 8000 "FastAPI (Python)" "FASTAPI_PID"
        echo "  $(get_process_stats "$FASTAPI_PID")"
        echo "  $(count_requests "/tmp/fastapi.log")"
        get_log_activity "/tmp/fastapi.log" 2
        echo ""
        
        check_service 11434 "Ollama Proxy" "OLLAMA_PID"
        echo "  $(get_process_stats "$OLLAMA_PID")"
        echo "  $(count_requests "/tmp/ollama.log")"
        get_log_activity "/tmp/ollama.log" 2
        echo ""
        
        echo -e "${CYAN}└───────────────────────────────────────────────────────────────────────────┘${NC}"
        echo ""
        
        # Port Status
        echo -e "${CYAN}┌─ PORT STATUS ─────────────────────────────────────────────────────────────┐${NC}"
        echo ""
        for port in 3000 4200 8000 11434; do
            if curl -s -o /dev/null -m 1 http://localhost:${port} 2>/dev/null; then
                echo -e "  ${GREEN}✓${NC} Port ${port} - ${GREEN}Active${NC}"
            else
                echo -e "  ${RED}✗${NC} Port ${port} - ${RED}Inactive${NC}"
            fi
        done
        echo ""
        echo -e "${CYAN}└───────────────────────────────────────────────────────────────────────────┘${NC}"
        echo ""
        
        # System Stats
        echo -e "${CYAN}┌─ SYSTEM STATS ────────────────────────────────────────────────────────────┐${NC}"
        echo ""
        
        # Total Node processes
        local node_count=$(ps aux | grep -c "[n]ode" || echo "0")
        echo -e "  ${BLUE}●${NC} Node Processes: ${node_count}"
        
        # Total Python processes  
        local python_count=$(ps aux | grep -c "[p]ython" || echo "0")
        echo -e "  ${BLUE}●${NC} Python Processes: ${python_count}"
        
        # Disk space for logs
        local log_size=$(du -sh /tmp/*.log 2>/dev/null | awk '{total+=$1} END {print total}' || echo "0")
        echo -e "  ${BLUE}●${NC} Log Files Size: ${log_size}"
        
        echo ""
        echo -e "${CYAN}└───────────────────────────────────────────────────────────────────────────┘${NC}"
        echo ""
        
        # Controls
        echo -e "${GRAY}Controls: ${WHITE}[Q]${GRAY}uit | ${WHITE}[R]${GRAY}efresh | ${WHITE}[L]${GRAY}ogs | ${WHITE}[K]${GRAY}ill Services${NC}"
        
        # Wait for input with timeout
        read -t 3 -n 1 key
        case $key in
            q|Q) 
                tput cnorm
                exit 0
                ;;
            r|R)
                continue
                ;;
            l|L)
                show_logs
                ;;
            k|K)
                kill_services
                ;;
        esac
    done
}

# Show full logs
show_logs() {
    clear
    echo -e "${CYAN}╔════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${WHITE}                         SERVICE LOGS                                      ${CYAN}║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}Select service:${NC}"
    echo "  1) Backend"
    echo "  2) Frontend"
    echo "  3) FastAPI"
    echo "  4) Ollama"
    echo "  5) All"
    echo "  0) Back"
    echo ""
    read -p "Choice: " choice
    
    case $choice in
        1) less +F /tmp/backend.log 2>/dev/null || echo "No backend logs" ;;
        2) less +F /tmp/frontend.log 2>/dev/null || echo "No frontend logs" ;;
        3) less +F /tmp/fastapi.log 2>/dev/null || echo "No fastapi logs" ;;
        4) less +F /tmp/ollama.log 2>/dev/null || echo "No ollama logs" ;;
        5) tail -f /tmp/*.log 2>/dev/null ;;
        0) return ;;
    esac
}

# Kill services
kill_services() {
    echo ""
    echo -e "${RED}⚠️  Kill all services? (y/N)${NC}"
    read -n 1 confirm
    if [[ $confirm =~ ^[Yy]$ ]]; then
        echo ""
        echo "Stopping services..."
        [ ! -z "$BACKEND_PID" ] && kill $BACKEND_PID 2>/dev/null
        [ ! -z "$FRONTEND_PID" ] && kill $FRONTEND_PID 2>/dev/null
        [ ! -z "$FASTAPI_PID" ] && kill $FASTAPI_PID 2>/dev/null
        [ ! -z "$OLLAMA_PID" ] && kill $OLLAMA_PID 2>/dev/null
        sleep 2
        rm -f /tmp/tn-pids.txt
        echo "Services stopped"
        sleep 2
    fi
}

# Main
echo "Starting True North Audio Monitor..."
sleep 1
monitor_services
