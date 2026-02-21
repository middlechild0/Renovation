#!/usr/bin/env python3
"""
📊 LIVE MONITORING SETUP GUIDE
================================

Watch businesses being added to the database in real-time as you scrape!

THREE WAYS TO RUN WITH LIVE MONITORING:
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import os

console = Console()

def show_guide():
    console.print(Panel.fit(
        "[bold cyan]📊 LIVE MONITORING - SETUP GUIDE[/bold cyan]",
        border_style="cyan"
    ))
    
    # Method 1
    console.print("\n[bold]METHOD 1: Run Dashboard First (Easiest)[/bold]")
    console.print("=" * 60)
    console.print("\n[cyan]Step 1:[/cyan] Start dashboard in one terminal")
    console.print("[dim]  Terminal 1:$ python3 dashboard.py[/dim]")
    console.print("  Output: [yellow]Running on http://127.0.0.1:5000[/yellow]\n")
    
    console.print("[cyan]Step 2:[/cyan] Open browser in another window")
    console.print("[dim]  Browser: http://localhost:5000[/dim]")
    console.print("  You'll see [green]Live Monitoring[/green] indicator at the top\n")
    
    console.print("[cyan]Step 3:[/cyan] Run app in second terminal")
    console.print("[dim]  Terminal 2:$ python3 app.py[/dim]")
    console.print("  Start searching for businesses...\n")
    
    console.print("[yellow]✓[/yellow] Watch the dashboard update in real-time (every 2 seconds)!\n")
    
    # Method 2
    console.print("\n[bold]METHOD 2: Use Helper Script (Automated)[/bold]")
    console.print("=" * 60)
    console.print("\n[cyan]One command starts both:[/cyan]")
    console.print("[dim]  $ chmod +x run_with_dashboard.sh[/dim]")
    console.print("[dim]  $ ./run_with_dashboard.sh[/dim]\n")
    
    console.print("This will:")
    console.print("  ✓ Start dashboard on port 5000")
    console.print("  ✓ Open browser automatically")
    console.print("  ✓ Launch the app\n")
    
    # Method 3
    console.print("\n[bold]METHOD 3: Start Live Monitoring Guide[/bold]")
    console.print("=" * 60)
    console.print("\n[cyan]Run the interactive setup:[/cyan]")
    console.print("[dim]  $ python3 start_live_monitoring.py[/dim]\n")
    
    console.print("You'll get:")
    console.print("  ✓ Clear instructions")
    console.print("  ✓ Automatic helper script creation")
    console.print("  ✓ Port setup information\n")
    
    # What you'll see
    console.print("\n[bold]WHAT YOU'LL SEE ON DASHBOARD:[/bold]")
    console.print("=" * 60)
    
    stats_table = Table(title="Live Metrics", show_header=True, header_style="bold cyan")
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Updates Every", style="yellow")
    stats_table.add_column("What It Shows", style="green")
    
    stats_table.add_row("Total Businesses", "2 seconds", "Count of businesses in database")
    stats_table.add_row("Analyzed Websites", "2 seconds", "Number of analyzed/scored websites")
    stats_table.add_row("High Priority Leads", "2 seconds", "Businesses needing redesign")
    stats_table.add_row("Average Website Score", "2 seconds", "Overall quality metric")
    stats_table.add_row("Category Distribution", "2 seconds", "Breakdown by business type")
    stats_table.add_row("Priority Chart", "2 seconds", "High/Medium/Low priority pie")
    stats_table.add_row("Leads Table", "2 seconds", "Top 10 actionable leads")
    
    console.print(stats_table)
    
    # Timeline example
    console.print("\n\n[bold]EXAMPLE TIMELINE:[/bold]")
    console.print("=" * 60)
    
    timeline = Table(show_header=True, header_style="bold yellow")
    timeline.add_column("Time", style="dim")
    timeline.add_column("Action", style="cyan")
    timeline.add_column("Dashboard Shows", style="green")
    
    timeline.add_row("0:00", "Start app, search Nairobi", "[gray]Initializing...[/gray]")
    timeline.add_row("0:02", "First API call", "Total: 0, Searching... [yellow]⟳[/yellow]")
    timeline.add_row("0:05", "API returns 50 results", "[bold]Total: 50[/bold] businesses")
    timeline.add_row("0:07", "Database saves", "Analytics updating...")
    timeline.add_row("0:10", "Analysis starts", "Analyzed: 5/50")
    timeline.add_row("0:15", "More scores added", "Analyzed: 15/50, Avg Score: 45")
    timeline.add_row("0:30", "Analysis complete", "Analyzed: 50/50, High Priority: 12")
    
    console.print(timeline)
    
    # Features
    console.print("\n\n[bold cyan]✨ FEATURES:[/bold cyan]")
    features = [
        "Real-time data updates (2 second refresh)",
        "Live business count",
        "Category breakdown updates instantly",
        "Website quality score tracking",
        "Priority lead identification",
        "Mobile-friendly detection indicator",
        "SSL/TLS certificate status",
        "Design needs assessment",
        "Export data anytime",
        "Mobile responsive design"
    ]
    
    for feature in features:
        console.print(f"  ✓ {feature}")
    
    # Troubleshooting
    console.print("\n\n[bold red]🔧 TROUBLESHOOTING:[/bold red]")
    console.print("=" * 60)
    
    console.print("\n[yellow]Q: Port 5000 already in use?[/yellow]")
    console.print("[cyan]A:[/cyan] Kill existing process or use different port:")
    console.print("[dim]   $ lsof -i :5000  # Find what's using it[/dim]")
    console.print("[dim]   $ kill -9 <PID>   # Kill the process[/dim]\n")
    
    console.print("[yellow]Q: Dashboard not updating?[/yellow]")
    console.print("[cyan]A:[/cyan] Check browser console (F12) for errors and ensure:")
    console.print("[dim]   • App is running (python3 app.py)[/dim]")
    console.print("[dim]   • Database is accessible[/dim]")
    console.print("[dim]   • No firewall blocking localhost:5000[/dim]\n")
    
    console.print("[yellow]Q: Want faster/slower updates?[/yellow]")
    console.print("[cyan]A:[/cyan] Edit templates/dashboard.html line with setInterval:")
    console.print("[dim]   setInterval(loadStats, 2000);  // 2000ms = 2 seconds[/dim]")
    console.print("[dim]   // Change 2000 to 1000 for 1 second, or 5000 for 5 seconds[/dim]\n")
    
    # Final tips
    console.print("\n[bold green]💡 PRO TIPS:[/bold green]")
    console.print("=" * 60)
    console.print("1. Use separate monitors: App on left, Dashboard on right")
    console.print("2. Use split screens: tmux or VS Code terminal splits")
    console.print("3. Analyze while scraping: Enable auto-analysis for instant scores")
    console.print("4. Export regularly: Download leads while searching")
    console.print("5. Monitor scores: Watch quality metrics in real-time\n")

if __name__ == "__main__":
    show_guide()
    
    console.print("\n[bold cyan]Ready to start?[/bold cyan]")
    console.print("[yellow]Run Method 1, 2, or 3 above![/yellow]\n")
