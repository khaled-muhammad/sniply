# Sniply Demo Mode

Welcome to Sniply Demo Mode! This allows you to test all features without needing real social media accounts.

## Quick Start

1. **Run the application**: `python main.py`
2. **Choose option 5**: Demo Mode
3. **Select option 1**: Setup Demo Mode
4. **Start testing**: Return to main menu and explore all features

## What Demo Mode Includes

### 🎭 Mock Accounts
- **Facebook**: 5 demo accounts with realistic usernames
- **Twitter/X**: 5 demo accounts with tech/news themed names  
- **Reddit**: 5 demo accounts with various interests
- **LinkedIn**: 5 demo accounts with professional profiles

### 📊 Realistic Data
- **900+ sample posts** across all categories
- **Smart categorization** using AI (news, tech, sports, etc.)
- **Platform-specific content** (subreddits, tweets, posts)
- **Realistic usernames** and post structures

### ✨ Full Feature Testing
- **Account Management**: Add, delete, enable/disable accounts
- **Settings Configuration**: Email categories, post limits, intervals
- **Scraping Simulation**: See how posts are processed and categorized
- **Email System**: Test email notifications (saved to `sent_emails.txt`)

## How to Use Demo Mode

### 1. Setup Demo Mode
```bash
python main.py
# Choose: 5 (Demo Mode)
# Choose: 1 (Setup Demo Mode)
```

This creates:
- 20 demo accounts across all platforms
- Randomized settings for variety
- Mock authentication cookies
- Sample subreddit/user follows

### 2. Test Account Management
```bash
# From main menu: 3 (Manage Accounts)
```

You can:
- View all demo accounts
- Edit settings (email categories, post limits)
- Enable/disable accounts
- Delete accounts
- Test re-authentication flow

### 3. Test Scraping
```bash
# From main menu: 1 (Start Scraping)
```

Demo scraping will:
- Process 20-50 posts per account
- Categorize posts using AI
- Send relevant posts to email
- Show realistic progress output
- Complete without browser automation

### 4. Add New Demo Accounts
```bash
# From main menu: 4 (Add New Account)
```

In demo mode, this will:
- Simulate account creation
- Let you choose platform and username
- Configure settings interactively
- No real authentication required

### 5. View Account Status
```bash
# From main menu: 2 (View Connected Accounts)
```

See all your demo accounts with:
- Platform and username
- Enable/disable status
- Email categories
- Post limits and intervals

## Demo Data Categories

### News Posts
- Breaking news about climate, politics, economics
- Local election results and policy changes
- Healthcare breakthroughs and research

### Technology Posts  
- AI developments and breakthroughs
- New smartphone and gadget releases
- Quantum computing milestones
- Privacy and security updates

### Sports Posts
- Championship games and tournaments
- Player trades and retirements
- Olympic preparations
- Record-breaking performances

### Entertainment Posts
- Movie releases and box office records
- TV show renewals and cancellations
- Music festival announcements
- Celebrity news and events

### Lifestyle Posts
- Health and wellness trends
- Sustainable living tips
- Urban gardening and minimalism
- Travel and food experiences

### Personal Posts
- Marathon training and achievements
- Career milestones and job changes
- Pet adoption stories
- Moving and life changes

## Testing Scenarios

### Scenario 1: News Aggregation
1. Set up accounts with "news" category enabled
2. Run scraping to see news posts processed
3. Check `sent_emails.txt` for email notifications
4. Adjust settings and test again

### Scenario 2: Multi-Platform Management
1. Enable accounts across all platforms
2. Configure different categories per platform
3. Test scraping with various post limits
4. Compare results across platforms

### Scenario 3: Account Lifecycle
1. Add new demo account
2. Configure specific settings
3. Test scraping functionality
4. Modify settings and re-test
5. Disable/delete account

### Scenario 4: Reddit Subreddit Testing
1. Configure Reddit accounts with specific subreddits
2. Test scraping with subreddit filtering
3. Compare general feed vs specific subreddits
4. Adjust subreddit lists and re-test

## Demo Mode Files

When demo mode is active, these files are created:
- `~/sniply/sm_accs/*/demo_*.sc` - Demo account cookies
- `~/sniply/sm_accs/*/*_settings.json` - Account settings
- `sent_emails.txt` - Email notifications log

## Cleanup

To remove all demo data:
```bash
python main.py
# Choose: 5 (Demo Mode)  
# Choose: 2 (Cleanup Demo Mode)
```

This will:
- Delete all demo accounts
- Remove demo settings files
- Clear email log
- Return to clean state

## Tips for Testers

### 🔍 What to Test
- **Account management workflow**
- **Settings persistence across sessions**
- **Email category filtering**
- **Post limit and interval controls**
- **Platform-specific features**
- **Error handling and edge cases**

### 🎯 Focus Areas
- **User interface clarity**
- **Settings organization**
- **Error messages and feedback**
- **Performance with multiple accounts**
- **Data accuracy and consistency**

### 📝 Feedback Areas
- **Menu navigation ease**
- **Settings configuration flow**
- **Output clarity and formatting**
- **Feature discoverability**
- **Overall user experience**

## Troubleshooting

### Demo Mode Not Working?
1. Check if `GROQ_API_KEY` is set (for AI categorization)
2. Ensure write permissions in home directory
3. Run cleanup and setup again
4. Check for Python package dependencies

### Missing Posts?
- Demo posts are randomly generated
- Check account enable/disable status
- Verify email category settings
- Look for posts in `sent_emails.txt`

### Settings Not Saving?
- Check file permissions
- Ensure demo mode is active
- Try cleanup and re-setup
- Verify account exists before configuring

## Real vs Demo Mode

| Feature | Real Mode | Demo Mode |
|---------|-----------|-----------|
| Authentication | Browser login required | Simulated instantly |
| Post Data | Live social media feeds | Curated sample posts |
| Processing Time | Minutes per account | Seconds per account |
| Browser Usage | Chrome/Selenium required | No browser needed |
| Rate Limits | Platform-specific limits | No limits |
| Data Variety | Unpredictable content | Consistent test data |

## Next Steps

After testing with demo mode:
1. **Provide feedback** on user experience
2. **Report any bugs** or issues found
3. **Suggest improvements** for workflows
4. **Test edge cases** and error conditions
5. **Verify all features** work as expected

Ready to test? Run `python main.py` and choose option 5! 