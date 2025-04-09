# GitHub Setup Guide

This guide will help you push your RockPaperScissors Bot project to GitHub.

## Prerequisites

1. [GitHub account](https://github.com/signup)
2. Git installed on your machine
3. Basic understanding of Git commands

## Steps to Push to GitHub

### 1. Create a New Repository on GitHub

1. Log in to your GitHub account
2. Click the "+" icon in the top right corner of the page, then select "New repository"
3. Enter "RockPaperScissors-Bot" as the repository name
4. Add a description: "A dynamic Telegram bot for playing Rock Paper Scissors with engaging multiplayer interactions and comprehensive game statistics."
5. Choose whether the repository should be public or private
6. Do NOT initialize the repository with a README, .gitignore, or license file
7. Click "Create repository"

### 2. Initialize Git in Your Local Project (if not already done)

Open a terminal/command prompt in your project directory and run:

```bash
git init
```

### 3. Add Your Files to Git

```bash
git add .
```

### 4. Commit Your Files

```bash
git commit -m "Initial commit: Rock Paper Scissors Telegram Bot"
```

### 5. Link Your Local Repository to GitHub

Replace `YOUR_USERNAME` with your GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/RockPaperScissors-Bot.git
```

### 6. Push Your Code to GitHub

```bash
git push -u origin main
```

If your default branch is called "master" instead of "main", use:

```bash
git push -u origin master
```

## Important Notes

1. Make sure your `.gitignore` file is properly set up to exclude sensitive information like:
   - Bot tokens and API keys (`.env` file)
   - Database files
   - User-specific configuration files
   - Log files

2. NEVER push your actual `.env` file to GitHub. Only push the `.env.example` template. Your `.gitignore` should have:
   ```
   # Environment variables
   .env
   .env.*
   !.env.example
   ```

3. NEVER push your `TELEGRAM_TOKEN` or any API keys to GitHub

4. For deployment, consider:
   - Setting up environment variables on your hosting platform
   - Using GitHub Actions for continuous deployment

## Troubleshooting

- If you get an authentication error, you may need to:
  - Use a personal access token instead of your password
  - Set up SSH authentication for GitHub

- If you have issues with the default branch name:
  - Check your current branch with `git branch`
  - Create a main branch with `git branch -M main` if needed

## Next Steps

After pushing your code to GitHub, you can:

1. Add collaborators to your repository
2. Set up GitHub Actions for continuous integration
3. Create releases for major updates
4. Add more detailed documentation in your README.md