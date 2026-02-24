#!/bin/bash
# update-widgets.sh - Refresh all live data widgets
# Run every hour via cron

cd "$(dirname "$0")/.."
SCRIPT_DIR="$(dirname "$0")"

echo "[$(date)] Updating farming data widgets..."

# Generate weather widget
python3 "$SCRIPT_DIR/weather-widget.py" 2>&1 | tee -a logs/widgets.log

# Generate commodity prices
python3 "$SCRIPT_DIR/commodity-widget.py" 2>&1 | tee -a logs/widgets.log

# Generate livestock markets
python3 "$SCRIPT_DIR/livestock-markets.py" 2>&1 | tee -a logs/widgets.log

# Rebuild site with new widgets
python3 "$SCRIPT_DIR/build-site.py" 2>&1 | tee -a logs/widgets.log

echo "[$(date)] Widgets updated successfully"
