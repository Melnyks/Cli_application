import argparse
import requests 
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL_EVER = "https://newsapi.org/v2/everything"
BASE_URL_TOP = "https://newsapi.org/v2/top-headlines"

def fetch_news(args):
    params_ever = {
        "q": args.keyword or "technology",
        "apiKey": API_KEY,
        "pageSize": args.num,
        "page": 1,
    }

    params_top = {
        "q": args.keyword,
        "apiKey": API_KEY,
        "pageSize": args.num,
    }

    if 'uptodate' in vars(args) and args.uptodate:
        params_ever["sortBy"] = "publishedAt"
    elif 'relevance' in vars(args) and args.relevance:
        params_ever["sortBy"] = "relevancy"

    if args.command == 'source':
        params_ever["sources"] = args.keyword
        params_ever["q"] = None

    if args.date:
        params_ever["from"] = args.date
        params_ever["to"] = args.date

    articles = []
    while len(articles) < args.num:

        response = requests.get(
            BASE_URL_EVER if args.command != 'category' else BASE_URL_TOP, 
            params = params_ever if args.command != 'category' else params_top
        )

        if response.status_code != 200:
            print(f"Error fetching news: {response.status_code}")
            break

        data = response.json()
        new_articles = [
            article for article in data.get("articles", [])
            if article.get("title") != '[Removed]'
            and article.get("description") != '[Removed]'
            and article.get("source", {}).get("name") != '[Removed]'
        ]

        articles.extend(new_articles)
        if len(data.get("articles", [])) < params_ever["pageSize"]:
            break

        params_ever["page"] += 1 

    return articles[:args.num]


def show_news(articles, brief=False):
    if not articles:
        print("No news available.")
        return

    filtered_articles = [
        article for article in articles
        if article.get('title') != '[Removed]'
        and article.get('description') != '[Removed]'
        and article.get('source', {}).get('name') != '[Removed]'
    ]

    if not filtered_articles:
        print("No relevant news articles found.")
        return

    for i, article in enumerate(filtered_articles, 1):
        # จัดการกรณีข้อมูลว่าง
        author = article.get('author') or 'No Author'
        title = article.get('title') or 'No Title'
        description = article.get('description') or 'No Description'
        source = article.get('source', {}).get('name') or 'Unknown Source'
        url = article.get('url') or 'No URL Available'
        publishedAt = article.get('publishedAt') or 'No publishedAt'

        print()
        print(f"{i}. Title: {title}")

        if not brief:
            print(f"   Author: {author}")
        print(f"   Description: {description}")

        if not brief:
            print(f"   Source: {source}")
            print(f"   publishedAt: {publishedAt}")
            print(f"   URL: {url}")

def list_data():
    print("Available types of data:")
    print("1. Trend News")
    print("   - This subcommand allows you to fetch the latest trending news articles.")
    print("   - You can filter by keyword, number of articles, date range, and display options (brief or full details).")
    
    print("2. Search News")
    print("   - This subcommand lets you search for news articles based on a specific keyword.")
    print("   - You can customize the number of articles, sort by relevance or publication date, and specify a date range.")
    
    print("3. Category News")
    print("   - This subcommand allows you to search for news articles in a specific category (e.g., technology, business, etc.).")
    print("   - You can filter the results by keyword, number of articles, date range, and sorting criteria.")
    
    print("4. Source News")
    print("   - This subcommand helps you fetch news articles from a specific source (e.g., BBC, CNN, etc.).")
    print("   - You can customize the number of articles, apply a date range, and sort the results.")

def main():
    parser = argparse.ArgumentParser(description="CLI for searching news articles")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help="List the available types of data (e.g., categories, sources).")
    
    # trend subcommand
    trend_parser = subparsers.add_parser('trend', help="Get trending news.")
    trend_parser.add_argument('-n', '--num', type=int, default=5, help="Number of news articles to display.")
    trend_parser.add_argument('-d','--date', type=str, help="Specify the date range: from which date to which date (format: YYYY-MM-DD,YYYY-MM-DD).")
    trend_parser.add_argument('-b','--brief', action='store_true', help="Show only title and description.")
    trend_parser.add_argument('keyword', type=str, nargs='?', default='technology', help="Keyword to search news articles.")

    # search subcommand
    search_parser = subparsers.add_parser("search", help="Search news articles by keyword.")
    search_parser.add_argument("keyword", type=str, help="Keyword to search news articles.")
    search_parser.add_argument("-n", "--num", type=int, default=5, help="Number of news articles to display.")
    search_parser.add_argument("-d", "--date", type=str, help="Specify the date range: from which date to which date (format: YYYY-MM-DD,YYYY-MM-DD).")
    search_parser.add_argument("-u", "--uptodate", action="store_true", help="Sort by latest date first.")
    search_parser.add_argument("-b", "--brief", action="store_true", help="Show only title and description.")
    search_parser.add_argument("-r", "--relevance", action="store_true", help="Sort by most relevant.")

    # category subcommand
    cate_parser = subparsers.add_parser("category", help="Search news articles by Category.")
    cate_parser.add_argument("keyword", type=str, help="Keyword to search category news articles.")
    cate_parser.add_argument("-n", "--num", type=int, default=5, help="Number of news articles to display.")
    cate_parser.add_argument("-d", "--date", type=str, help="Specify the date range: from which date to which date (format: YYYY-MM-DD,YYYY-MM-DD).")
    cate_parser.add_argument("-u", "--uptodate", action="store_true", help="Sort by latest date first.")
    cate_parser.add_argument("-b", "--brief", action="store_true", help="Show only title and description.")
    cate_parser.add_argument("-r", "--relevance", action="store_true", help="Sort by most relevant.")

    # source subcommand
    source_parser = subparsers.add_parser("source", help="Search news articles by Source.")
    source_parser.add_argument("keyword", type=str, help="Keyword to search source news articles.")
    source_parser.add_argument("-n", "--num", type=int, default=5, help="Number of news articles to display.")
    source_parser.add_argument("-d", "--date", help="Specify the date range: from which date to which date (format: YYYY-MM-DD,YYYY-MM-DD).")
    source_parser.add_argument("-u", "--uptodate", action="store_true", help="Sort by latest date first.")
    source_parser.add_argument("-b", "--brief", action="store_true", help="Show only title and description.")
    source_parser.add_argument("-r", "--relevance", action="store_true", help="Sort by most relevant.")

    # help subcommand
    help_parser = subparsers.add_parser("help", help="Show detailed information about all subcommands.")

    args = parser.parse_args()

    if args.command == "help":
        print("Available subcommands and options:\n")
        print("trend    - Get trending news.")
        print("  -n, --num       Number of news articles to display (default: 5).")
        print("  -d, --date      Specify the date range (format: YYYY-MM-DD,YYYY-MM-DD).")
        print("  -b, --brief     Show only title and description.")
        print("  [keyword]       Keyword to search news articles (default: 'technology').\n")
        print("search   - Search news articles by keyword.")
        print("  <keyword>       Keyword to search news articles.")
        print("  -n, --num       Number of news articles to display (default: 5).")
        print("  -d, --date      Specify the date range (format: YYYY-MM-DD,YYYY-MM-DD).")
        print("  -u, --uptodate  Sort by latest date first.")
        print("  -b, --brief     Show only title and description.")
        print("  -r, --relevance Sort by most relevant.\n")
        print("category - Search news articles by category.")
        print("  <keyword>       Keyword to search category news articles.")
        print("  -n, --num       Number of news articles to display (default: 5).")
        print("  -d, --date      Specify the date range (format: YYYY-MM-DD,YYYY-MM-DD).")
        print("  -u, --uptodate  Sort by latest date first.")
        print("  -b, --brief     Show only title and description.")
        print("  -r, --relevance Sort by most relevant.\n")
        print("source   - Search news articles by source.")
        print("  <keyword>       Keyword to search source news articles.")
        print("  -n, --num       Number of news articles to display (default: 5).")
        print("  -d, --date      Specify the date range (format: YYYY-MM-DD,YYYY-MM-DD).")
        print("  -u, --uptodate  Sort by latest date first.")
        print("  -b, --brief     Show only title and description.")
        print("  -r, --relevance Sort by most relevant.")
        return

    if args.command == "list":
        list_data()

    if args.command in ["category","trend","search","source"]:
        articles = fetch_news(args)
        show_news(articles, brief=args.brief)
    
if __name__ == "__main__":
    main()