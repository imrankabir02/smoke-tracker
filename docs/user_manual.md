# Smoke Tracker User Manual

Welcome to Smoke Tracker! This manual will guide you through all the features of the application, helping you to effectively track and manage your smoking habits.

## 1. Getting Started

### 1.1. Signing Up
To begin using Smoke Tracker, you need to create an account.

1.  Navigate to the [Sign Up](http://127.0.0.1:8000/signup/) page.
2.  Fill in your desired username, password, timezone, and currency.
3.  Click the "Sign Up" button.

### 1.2. The Setup Wizard
After signing up, you will be guided through a one-time setup process to personalize your experience.

-   **Step 1: Set Your Daily Goal:** Enter the maximum number of cigarettes you aim to smoke per day. This will help you track your progress.
-   **Step 2: Add Your Brands:** Add the cigarette brands you smoke and their price per stick. This is crucial for accurate cost tracking. You can add multiple brands.
-   **Step 3: Set Your Defaults:** Choose a default brand, trigger, and mood settings. These will be used for the "Quick Log" feature.

Once the setup is complete, you will be redirected to your dashboard.

## 2. The Dashboard (Home Page)

The dashboard is your main hub for at-a-glance information about your progress.

-   **Time Since Last Smoke:** Shows how long it has been since your last logged smoke.
-   **Daily Progress:** A visual representation of how many cigarettes you've smoked today compared to your daily goal.
-   **Cost Analysis:** Displays your total smoking costs for today, the last 7 days, and the last 30 days.
-   **Recent Activity:** A list of your most recently logged smokes.

## 3. Logging Smokes

There are two ways to log a smoke.

### 3.1. Standard Log
For detailed tracking:

1.  Click on the "Log Smoke" button.
2.  Select the **Brand**, **Trigger** (the reason for smoking), and your **Mood** before and after.
3.  Optionally, add a **Note**.
4.  Click "Save".

### 3.2. Quick Log
For fast and easy logging:

1.  Click the "Quick Log" button on the dashboard.
2.  This will instantly log a smoke using the default settings you configured in the setup wizard.

## 4. Viewing Your Data

### 4.1. Log History
The "Logs" page provides a complete history of your logged smokes. You can:
-   **Filter** your logs by trigger or a specific date range.
-   **Navigate** through your history using the pagination controls.

### 4.2. Statistics
The "Stats" page offers powerful insights into your smoking patterns through various charts and metrics:

-   **Summary:** Total smokes, total cost, and daily average.
-   **Time-Based Stats:** Breakdown of smokes and costs by day, week, and month.
-   **Charts:** Visual graphs showing your smoking frequency by hour, day of the week, and week of the month.
-   **Trigger Analysis:** See which triggers most commonly lead to smoking.
-   **Mood Impact:** Analyze how smoking affects your mood.

## 5. Managing Your Settings

You can update your preferences at any time.

-   **Brands:** On the "Brands" page, you can add new brands, edit the price of existing ones, or delete them from your list.
-   **Goal:** Visit the "Goal" page to update your daily smoking limit.
-   **Defaults:** Go to the "Defaults" page to change your preferences for the Quick Log feature.
-   **Profile Settings:** On the "Settings" page, you can update your timezone, currency, or change your password.

## 6. Requesting New Brands

If a brand you smoke is not in the global list, you can request for it to be added:

1.  Go to the "Brands" page and click "Request a New Brand".
2.  Enter the name of the brand and submit the form.
3.  Your request will be sent to an administrator for approval. You can view the status of your previous requests on the same page.

## 7. Admin Features (For Superusers)

If you have admin privileges, you can access the "Admin Dashboard".

-   **Site-wide Analytics:** View key metrics for all users, such as total users, total smokes, and most popular brands.
-   **Brand Requests:** Approve or reject brand requests submitted by users. Approving a request makes the brand available for all users to add to their personal list.
