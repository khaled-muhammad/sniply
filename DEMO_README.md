# Sniply Demo Mode - Tester Guide

Welcome to Sniply Demo Mode! This guide matches the tester mode setup from our landing page and allows you to test all features without needing real social media accounts.

## Quick Setup Guide

Follow these 6 steps to get started with demo mode:

### Step 1: Clone Repository
Clone the project and set up the development environment:
```bash
git clone https://github.com/khaled-muhammad/sniply.git
cd sniply
```

### Step 2: Install Dependencies
Install development dependencies and set up virtual environment:
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Setup Environment
Create a .env file in the project root and add your GROQ API key:
```bash
GROQ_API_KEY=your_api_key_here
```

### Step 4: Start Development
Run in development mode with debugging enabled:
```bash
python demo_mode.py
```

### Step 5: Choose Demo Mode
Select demo mode options (1 on, 2 off, 3 status): Enter **1** to turn on the mode:
```
1
```

### Step 6: Run Main & Start Scraping
Execute the main script and select option 1 to start scraping:
```bash
python main.py
```

When the main menu appears, you'll see:
```
Welcome to Sniply, Only the posts worth your time
🎮 DEMO MODE ACTIVE

Please choose an option:
1- Start Scraping
2- View Connected Accounts
3- Manage Accounts (Settings, Delete, Re-auth)
4- Add New Account
5- Demo Mode
6- Exit

Enter your choice: 1
```

→ **(Visual Demo Only - Please test do the steps on real device)**

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

## Main Menu Options

### 1. Start Scraping
Demo scraping will:
- Process 20-50 posts per account
- Categorize posts using AI
- Send relevant posts to email
- Show realistic progress output
- Complete without browser automation

### 2. View Connected Accounts
See all your demo accounts with:
- Platform and username
- Enable/disable status
- Email categories
- Post limits and intervals

### 3. Manage Accounts
You can:
- View all demo accounts
- Edit settings (email categories, post limits)
- Enable/disable accounts
- Delete accounts
- Test re-authentication flow

### 4. Add New Account
In demo mode, this will:
- Simulate account creation
- Let you choose platform and username
- Configure settings interactively
- No real authentication required

### 5. Demo Mode
Access demo mode settings:
- Toggle demo mode on/off
- Check current status
- Cleanup demo data

### 6. Exit
Exit the application

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

### Scenario 1: First Time Setup
1. Follow steps 1-6 above
2. Choose option 1 to start scraping
3. Watch demo posts being processed
4. Check `sent_emails.txt` for results

### Scenario 2: Account Management
1. Choose option 2 to view accounts
2. Choose option 3 to manage accounts
3. Modify settings for different platforms
4. Test scraping with new settings

### Scenario 3: Adding New Accounts
1. Choose option 4 to add new account
2. Select platform and configure settings
3. Test scraping with new account
4. Verify account appears in account list

### Scenario 4: Demo Mode Management
1. Choose option 5 for demo mode settings
2. Test toggling demo mode on/off
3. Check status and cleanup options
4. Verify demo data management

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
1. Ensure you followed all 6 steps in order
2. Check if `GROQ_API_KEY` is set (for AI categorization)
3. Ensure write permissions in home directory
4. Run cleanup and setup again
5. Check for Python package dependencies

### Missing Posts?
- Demo posts are randomly generated
- Check account enable/disable status
- Verify email category settings
- Look for posts in `sent_emails.txt`

### Settings Not Saving?
- Check file permissions
- Ensure demo mode is active (🎮 DEMO MODE ACTIVE should show)
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

Ready to test? Follow the 6 steps above and start with `python demo_mode.py`! 