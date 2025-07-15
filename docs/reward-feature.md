Below is a **step-by-step feature implementation plan** for adding the **Reward-Based System** to your Django Smoke Tracker project.

---

# 🚀 **Smoke Tracker Rewards System Implementation Plan**

---

## **1️⃣ Models Design**

### **1.1 Points Model**

Tracks total points per user.

```python
class UserPoints(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
```

### **1.2 Achievements Model**

Tracks which achievements the user has unlocked.

```python
class Achievement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    points_reward = models.IntegerField(default=0)
    icon = models.ImageField(upload_to='achievement_icons/')
    
    def __str__(self):
        return self.title


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_earned = models.DateTimeField(auto_now_add=True)
```

---

## **2️⃣ Signals / Business Logic Integration**

Automatically award points and achievements when users hit specific actions.

### Example Signal on Logging Smoke

```python
@receiver(post_save, sender=SmokeLog)
def update_points_on_log(sender, instance, created, **kwargs):
    if created:
        points = 10  # Example: 10 points per logged smoke for consistency
        user_points, _ = UserPoints.objects.get_or_create(user=instance.user)
        user_points.points += points
        user_points.save()
```

### Example Signal on Streak Completion

You can create a scheduled task (using Celery) to calculate daily streaks and award bonus points.

---

## **3️⃣ Admin Panel (Optional)**

Create achievements dynamically via Django Admin:

* Title: `7-Day Streak`
* Description: `Smoke-free for 7 days`
* Reward: `+300 points`
* Icon: Upload file

---

## **4️⃣ UI/UX Suggestions**

### Dashboard Updates:

* Show **Points Balance** prominently.
* Show **Next Achievement** progress.
* Display **Recently Unlocked Achievements**.

### New Pages:

1. **My Achievements:** List unlocked with date and points earned.
2. **Rewards Store / Progress Page:** For future growth.

---

## **5️⃣ Feature Scope for Initial Release**

### 🎯 Focus On:

✅ Points on streak
✅ Points on reduction
✅ Points on logging consistency
✅ Achievements (Badges)
✅ Admin control for achievements

---

## **6️⃣ Example Achievements (Seed Data)**

| Title                | Points | Criteria                  |
| -------------------- | ------ | ------------------------- |
| First Log            | 10     | Log your first smoke      |
| First Smoke-Free Day | 50     | Complete 1 smoke-free day |
| 7-Day Streak         | 300    | 7 smoke-free days         |
| 30-Day Streak        | 1000   | 30 smoke-free days        |

---

## **7️⃣ Future Integration Ideas (Not for Now)**

* Store to redeem points for coupons
* API integration with wellness partners
* Social leaderboard

---

If you want, I can now write:
✅ Django Models
✅ Example views/templates
✅ Admin configurations
✅ Signal handlers