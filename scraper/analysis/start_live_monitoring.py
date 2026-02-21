#!/usr/bin/env python3
"""
Live Monitoring - Run App and Dashboard Together
Watch businesses being added to the database in real-time on the dashboard
"""

import subprocess
import time
import os
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def main():
    console.print(Panel.fit(
        "[bold cyan]🤖 BUSINESS FINDER - LIVE MONITORING[/bold cyan]\n"
        "[yellow]Running App & Dashboard Simultaneously[/yellow]",
        border_style="cyan"
    ))
    
    console.print("\n[bold]📋 Setup Instructions:[/bold]\n")
    console.print("[cyan]Terminal 1 (This window):[/cyan]")
    console.print("  • Scrape for businesses using the CLI interface")
    console.print("  • See real-time results in Terminal 2\n")
    
    console.print("[cyan]Terminal 2 (Open in new terminal):[/cyan]")
    console.print("  • Open browser to http://localhost:5000")
    console.print("  • See live dashboard updates")
    console.print("  • Dashboard auto-refreshes every 2 seconds\n")
    
    console.print("[bold]Quick Start:[/bold]\n")
    console.print("1. [green]✓[/green] Dashboard starting on port 5000...")
    console.print("2. [yellow]↻[/yellow] Open new terminal and run:")
    console.print("   [cyan]python3 dashboard.py[/cyan]\n")
    console.print("3. [yellow]↻[/yellow] Open browser and go to:")
    console.print("   [cyan]http://localhost:5000[/cyan]\n")
    console.print("4. [yellow]↻[/yellow] Return to this terminal to search:")
    console.print("   [cyan]python3 app.py[/cyan]\n")
    
    console.print("[bold yellow]OR run everything with one command:[/bold yellow]\n")
    console.print("   [cyan]./run_with_dashboard.sh[/cyan]\n")
    
    # Create helper script
    create_helper_script()
    
    console.print("[bold]📊 What You'll See:[/bold]\n")
    console.print("  ✓ Real-time business count updates")
    console.print("  ✓ Website analysis scores")
    console.print("  ✓ Category distribution")
    console.print("  ✓ Lead priority ranking")
    console.print("  ✓ Mobile-friendly status")
    console.print("  ✓ SSL/TLS certificate info\n")
    
    console.print("[bold cyan]Ready to start?[/bold cyan] Follow the instructions above!")
    console.print("[dim]Press Ctrl+C to exit[/dim]\n")

def create_helper_script():
    """Create a bash script to run both in parallel"""
    script_content = '''#!/bin/bash

# Check if dashboard is already running
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠ Dashboard already running on port 5000"
else
    echo "Starting dashboard on port 5000..."
    python3 dashboard.py > /tmp/dashboard.log 2>&1 &
    DASHBOARD_PID=$!
    sleep 2
    echo "✓ Dashboard started (PID: $DASHBOARD_PID)"
fi

echo ""
echo "Opening browser to http://localhost:5000..."
# Try to open browser (works on Linux, macOS, and Windows)
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5000 &
elif command -v open &> /dev/null; then
    open http://localhost:5000 &
fi

echo ""
echo "Starting app for searching businesses..."
sleep 1
python3 app.py

# Cleanup
if [ ! -z "$DASHBOARD_PID" ]; then
    kill $DASHBOARD_PID 2>/dev/null
fi
'''
    
    script_path = "/home/shalekami/Desktop/Jimmy/Sajim/Scraper /run_with_dashboard.sh"
    try:
        with open(script_path, 'w') as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        print(f"✓ Helper script created: run_with_dashboard.sh")
    except:
        pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Exited[/yellow]")
        sys.exit(0)
