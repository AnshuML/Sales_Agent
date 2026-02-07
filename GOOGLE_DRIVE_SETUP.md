# Google Drive Setup Guide

Follow these steps to set up Google Drive integration for the Multi-Agent Sales Analysis System.

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Select a Project** → **New Project**
3. Name it (e.g., "Sales Analysis Agent")
4. Click **Create**

## Step 2: Enable Google Drive API

1. In your project, go to **APIs & Services** → **Library**
2. Search for "Google Drive API"
3. Click on it and press **Enable**

## Step 3: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **+ Create Credentials** → **OAuth client ID**
3. If prompted, configure the **OAuth consent screen**:
   - User Type: **External**
   - App name: "Sales Analysis Agent"
   - User support email: Your email
   - Developer contact: Your email
   - Click **Save and Continue**
   - Scopes: Skip (click **Save and Continue**)
   - Test users: Add your Gmail address
   - Click **Save and Continue**

4. Back to Create OAuth client ID:
   - Application type: **Desktop app**
   - Name: "Sales Analysis Desktop"
   - Click **Create**

5. **Download** the JSON file
6. Rename it to `credentials.json`
7. Move it to the `credentials/` folder in your project

## Step 4: First-Time Authentication

When you run the system for the first time and select Google Drive:

1. A browser window will open
2. Select your Google account
3. Click **Continue** (it may warn "Google hasn't verified this app" - that's okay for personal use)
4. Click **Continue** again
5. Grant access to Google Drive
6. The system will create a `token.pickle` file for future use

## Step 5: Test It!

```bash
python main.py
```

Try the query: "Show me this quarter's sales"
Select: Google Drive
Paste one of your Google Sheets links!

## Troubleshooting

**Error: "Access blocked: This app's request is invalid"**
- Make sure you added yourself as a test user in the OAuth consent screen

**Error: "Invalid grant"**
- Delete `credentials/token.pickle` and re-authenticate

**Error: "File not found: credentials.json"**
- Make sure `credentials.json` is in the `credentials/` folder

## Your Google Drive Links

You provided these links - they'll work once authentication is set up!

1. https://docs.google.com/spreadsheets/d/1zhJsMuoBBN_AlHVjHFoX_QM_qJHUUBDL/edit
2. https://docs.google.com/spreadsheets/d/1PDqFfEa8GpLYAKD5vzZBZJ9_XG7Sts0y/edit  
3. https://docs.google.com/spreadsheets/d/1McOKrNqLnOHNfJQ47ldaHW8LsAkzHSax/edit

---

Need help? Check the [Google Drive API Python Quickstart](https://developers.google.com/drive/api/quickstart/python)
