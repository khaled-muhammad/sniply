# Sniply

> Only the posts worth your time

<div align="center">
  <a href="https://shipwrecked.hackclub.com/?t=ghrm" target="_blank">
    <img src="https://hc-cdn.hel1.your-objectstorage.com/s/v3/739361f1d440b17fc9e2f74e49fc185d86cbec14_badge.png" 
         alt="This project is part of Shipwrecked, the world's first hackathon on an island!" 
         style="width: 35%;">
  </a>
</div>

Sniply is an intelligent social media aggregator that scrapes content from multiple platforms, categorizes posts using AI, and delivers only the content you care about directly to your inbox.

## ✨ Features

### 🔗 Multi-Platform Support
- **Facebook** - Posts from your feed and specific pages
- **Twitter/X** - Tweets from timeline and specific users
- **Reddit** - Posts from subreddits and general feed
- **LinkedIn** - Professional posts and updates

### 🤖 AI-Powered Categorization
- **Smart Classification** - Automatically categorizes posts into:
  - News & Current Events
  - Technology & Innovation  
  - Sports & Entertainment
  - Lifestyle & Personal
  - Memes & Humor
  - Advertisements
- **Groq AI Integration** - Uses advanced language models for accurate categorization

### ⚙️ Flexible Configuration
- **Per-Account Settings** - Different email categories for each account
- **Post Limits** - Control how many posts to process per scrape
- **Scrape Intervals** - Set custom timing for automated scraping
- **Specific Targeting** - Follow specific users, pages, or subreddits
- **Enable/Disable** - Turn accounts on/off without deletion

### 📧 Email Delivery
- **Filtered Content** - Only receive posts from categories you want
- **Clean Formatting** - AI-cleaned posts optimized for reading
- **Detailed Metadata** - Username, platform, category, and timestamps

### 🎮 Demo Mode
- **No Account Required** - Test all features without real social media accounts
- **Realistic Data** - 900+ sample posts across all categories
- **Full Functionality** - Complete testing environment for evaluation

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Chrome browser (for real scraping)
- Groq API key (for AI categorization)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/khaled-muhammad/sniply.git
   cd sniply
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**
   ```bash
   # Create .env file
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

### First Time Setup

1. **Try Demo Mode** (Recommended)
   - Choose option `5` (Demo Mode)
   - Select `1` (Setup Demo Mode)
   - Explore all features risk-free

2. **Add Real Accounts**
   - Choose option `4` (Add New Account)
   - Select platform and login via browser
   - Configure settings for each account

3. **Start Scraping**
   - Choose option `1` (Start Scraping)
   - Watch as posts are processed and categorized
   - Check `sent_emails.txt` for email notifications

## 📖 Usage Guide

### Account Management

**Adding Accounts**
```bash
python main.py
# Choose: 4 (Add New Account)
# Select platform and authenticate via browser
```

**Managing Settings**
```bash
python main.py  
# Choose: 3 (Manage Accounts)
# Select account to configure:
# - Email categories
# - Post limits
# - Scrape intervals
# - Specific pages/users
```

**Viewing Status**
```bash
python main.py
# Choose: 2 (View Connected Accounts)
# See all accounts with status and settings
```

### Scraping Content

**Manual Scraping**
```bash
python main.py
# Choose: 1 (Start Scraping)
# Processes all enabled accounts
```

**Automated Scraping**
```bash
# Set up cron job or task scheduler
python start.py
```

### Configuration Options

**Email Categories**
- `news` - Breaking news and current events
- `technology` - Tech updates and innovations
- `sports` - Sports news and updates
- `entertainment` - Movies, TV, music, celebrities
- `lifestyle` - Health, wellness, travel, food
- `personal` - Personal updates from friends
- `meme` - Humor and memes
- `advertisement` - Promotional content

**Platform-Specific Settings**
- **Reddit**: Target specific subreddits
- **Facebook/X/LinkedIn**: Follow specific users/pages
- **All Platforms**: Set post limits and intervals

## 🎮 Demo Mode

Perfect for testing without real accounts!

### Setup Demo Mode
```bash
python main.py
# Choose: 5 (Demo Mode)
# Choose: 1 (Setup Demo Mode)
```

### What You Get
- **20 demo accounts** across all platforms
- **Realistic sample posts** in all categories
- **Full feature testing** without authentication
- **No rate limits** or browser requirements

### Demo Features
- ✅ Account management and settings
- ✅ Content scraping simulation
- ✅ AI categorization testing
- ✅ Email notification system
- ✅ Platform-specific configurations

See [DEMO_README.md](DEMO_README.md) for detailed demo instructions.

## 🛠️ Technical Details

### Architecture
```
Sniply/
├── main.py              # Main application entry point
├── models.py            # Account and settings data models
├── utils.py             # Core utilities and AI integration
├── add_account.py       # Account authentication flow
├── manage_accounts.py   # Account management interface
├── start.py             # Scraping orchestration
├── scrappers/           # Platform-specific scrapers
│   ├── facebook_scrapper.py
│   ├── x_scrapper.py
│   ├── reddit_scrapper.py
│   └── linkedin_scrapper.py
├── demo_mode.py         # Demo mode functionality
├── demo_scraper.py      # Demo scraping simulation
└── demo_add_account.py  # Demo account creation
```

### Data Storage
- **Account Data**: `~/sniply/sm_accs/`
- **Cookies**: `{platform}/{username}.sc`
- **Settings**: `{platform}/{username}_settings.json`
- **Email Log**: `sent_emails.txt`

### Dependencies
- **selenium** - Browser automation
- **webdriver-manager** - Chrome driver management
- **groq** - AI categorization
- **colorama** - Terminal colors

## 🔧 Configuration

### Environment Variables
```bash
# Required for AI categorization
GROQ_API_KEY=your_groq_api_key_here
```

### Account Settings Structure
```json
{
  "account_id": "platform_username",
  "platform": "facebook",
  "username": "john_doe",
  "email_categories": ["news", "technology"],
  "enabled": true,
  "max_posts_per_scrape": 100,
  "scrape_interval_minutes": 30,
  "specific_pages": ["https://example.com"],
  "subreddits": ["technology", "news"],
  "follow_users": ["user1", "user2"]
}
```

## 🚦 Getting Started Examples

### Example 1: News Aggregation
```bash
# 1. Add accounts from news sources
python main.py → 4 → Add Reddit account
# 2. Configure for news subreddits
python main.py → 3 → Select account → Edit subreddits: "news,worldnews"
# 3. Set email categories to news only
python main.py → 3 → Select account → Email categories: "news"
# 4. Start scraping
python main.py → 1
```

### Example 2: Tech Updates
```bash
# 1. Add Twitter accounts
python main.py → 4 → Add X account
# 2. Configure for tech category
python main.py → 3 → Select account → Email categories: "technology"
# 3. Follow tech influencers
python main.py → 3 → Select account → Follow users: "elonmusk,sundarpichai"
# 4. Start scraping
python main.py → 1
```

### Example 3: Multi-Platform Setup
```bash
# 1. Add accounts from all platforms
python main.py → 4 → Add Facebook, X, Reddit, LinkedIn accounts
# 2. Configure different categories per platform
# Facebook: personal, lifestyle
# X: news, technology  
# Reddit: news, entertainment
# LinkedIn: technology, news
# 3. Set different post limits
# Facebook: 50 posts
# X: 100 posts
# Reddit: 75 posts
# LinkedIn: 25 posts
# 4. Start scraping all platforms
python main.py → 1
```

## 🔍 Troubleshooting

### Common Issues

**Authentication Fails**
- Ensure Chrome browser is installed
- Check internet connection
- Try clearing browser cache
- Verify platform login credentials

**No Posts Found**
- Check account enable/disable status
- Verify email category settings
- Ensure accounts have content in feed
- Check post limit settings

**AI Categorization Not Working**
- Verify `GROQ_API_KEY` is set correctly
- Check internet connection
- Ensure Groq API quota is available
- Posts will default to "other" category if AI fails

**Performance Issues**
- Reduce `max_posts_per_scrape` setting
- Increase `scrape_interval_minutes`
- Disable unused accounts
- Close other browser instances

### Debug Mode
```bash
# Run with verbose output
python main.py --debug
```

## 📊 Performance Tips

### Optimization
- **Batch Processing**: Process multiple accounts simultaneously
- **Smart Limits**: Set appropriate post limits per platform
- **Selective Categories**: Only enable needed email categories
- **Account Management**: Disable unused accounts

### Recommended Settings
```
Facebook: 50-100 posts, 30-60 min intervals
X: 100-200 posts, 15-30 min intervals  
Reddit: 75-150 posts, 30-45 min intervals
LinkedIn: 25-50 posts, 60-120 min intervals
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with demo mode
5. Submit a pull request

### Development Setup
```bash
git clone https://github.com/khaled-muhammad/sniply.git
cd sniply
pip install -r requirements.txt
python demo_mode.py  # Setup demo environment
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq** for AI categorization capabilities
- **Selenium** for browser automation
- **Chrome WebDriver** for platform access
- **Colorama** for terminal styling

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/khaled-muhammad/sniply/issues)
<!-- - **Documentation**: [Wiki](https://github.com/khaled-muhammad/sniply/wiki) -->
- **Demo Guide**: [DEMO_README.md](DEMO_README.md)

---

**Made with ❤️ for smarter social media consumption**

*Sniply - Because your time is valuable, and not all posts are worth it.* 