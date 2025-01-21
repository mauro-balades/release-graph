import requests
from datetime import datetime
from collections import defaultdict
import sys

# Function to fetch release stats
def fetch_release_stats(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    print(f"Fetching release stats from {url}")
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)
    releases = response.json()
    
    monthly_downloads = defaultdict(int)
    
    for release in releases:
        print(f"Processing release: {release['name']}")
        release_date = datetime.strptime(release['published_at'], "%Y-%m-%dT%H:%M:%SZ")
        month_key = release_date.strftime("%Y-%m")
        
        for asset in release['assets']:
            print(f"\tAsset: {asset['name']} - {asset['download_count']} downloads")
            monthly_downloads[month_key] += asset['download_count']
    
    return dict(sorted(monthly_downloads.items()))

# Plotting the graph
def plot_downloads(downloads):
    months = list(downloads.keys())
    counts = list(downloads.values())

    max_count = max(counts)
    
    # Show it on a text-based graph
    print("\n\nMonthly Downloads\n")
    for month, count in downloads.items():
        print(f"{month}: {'#' * (count * 50 // max_count)} ({count})")
    print("\nTotal Downloads: ", sum(counts))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <owner> <repo>")
        sys.exit(1)
    owner = sys.argv[1]  # Pass the owner name as a command-line argument
    repo = sys.argv[2]  # Pass the repo name as a command-line argument
    stats = fetch_release_stats(owner, repo)
    plot_downloads(stats)
