## ✅ Project Overview

**Goal**: Help users log smoking events, view their history, and track patterns to reduce or quit smoking.

---

## 📌 Phase 1: Requirements & Planning

### 🎯 Core Features:

1. User Registration & Login
2. Dashboard/Homepage
3. Log a smoke (with optional note)
4. View all logs (chronological)
5. Track metrics:

   * Total smokes
   * Last smoke time
   * Smokes per day/week
6. Logout functionality

### 📦 Tech Stack:

| Layer          | Tool                                             |
| -------------- | ------------------------------------------------ |
| Backend        | Django                                           |
| Frontend       | Django Templates (later extendable to React/Vue) |
| Database       | SQLite (for dev), PostgreSQL (for production)    |
| Authentication | Django auth system                               |
| Deployment     | PythonAnywhere / Heroku / Render / VPS           |
| Optional       | Chart.js for graphs                              |

---

## 🏗️ Phase 2: Project Structure

```bash
smoketracker/
├── smoketracker/         # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tracker/              # Main app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── templates/
│   │   └── tracker/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── log_smoke.html
│   │       ├── log_list.html
│   │       └── stats.html
├── templates/            # Global templates
│   └── registration/
│       ├── login.html
│       └── signup.html
├── static/               # CSS, JS, images
├── db.sqlite3
└── manage.py
```

---

## ⚙️ Phase 3: Implementation Plan

### 3.1 Project Setup

* [x] `django-admin startproject smoketracker`
* [x] `python manage.py startapp tracker`
* [x] Add app to `INSTALLED_APPS`
* [x] Setup base templates folder, static folder

---

### 3.2 Authentication System

* [x] Use Django's built-in login/logout
* [x] Create custom signup view
* [x] Secure views using `@login_required`

---

### 3.3 Models

#### Brand Model
```python
class Brand(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
```

#### SmokeLog Model
```python
class SmokeLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, blank=True)
```

* [ ] Create `Brand` model
* [ ] Update `SmokeLog` model
* [ ] Run migrations

---

### 3.4 Forms

#### Brand Form
```python
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'price']
```

#### SmokeLog Form
```python
class SmokeLogForm(forms.ModelForm):
    class Meta:
        model = SmokeLog
        fields = ['brand', 'note']
```

---

### 3.5 Views & Logic

| View         | URL           | Functionality                                     |
| ------------ | ------------- | ------------------------------------------------- |
| Home         | `/`           | Welcome text + navigation                         |
| Add Brand    | `/add-brand/` | Add a new brand with price                        |
| Brand List   | `/brands/`    | View all brands                                   |
| Log Smoke    | `/log/`       | Submit a new smoking log with brand selection     |
| Logs List    | `/logs/`      | Show user’s previous entries                      |
| Stats        | `/stats/`     | Count total smokes, last smoke, costs, graphs     |
| Login        | `/login/`     | Default login                                     |
| Logout       | `/logout/`    | Logout redirect to home                           |
| Signup       | `/signup/`    | Custom user registration form                     |

---

### 3.6 Templates

* Use `base.html` for layout
* Extend for each view
* Include Bootstrap (optional) for styling

---

### 3.7 Stats View (Optional)

```python
@login_required
def stats(request):
    logs = SmokeLog.objects.filter(user=request.user)
    total_smokes = logs.count()
    last_smoke = logs.order_by('-timestamp').first()
    
    total_cost = logs.aggregate(total_cost=Sum('brand__price'))['total_cost'] or 0
    
    return render(request, 'tracker/stats.html', {
        'total_smokes': total_smokes,
        'last_smoke': last_smoke,
        'total_cost': total_cost,
    })
```

---

## 🧪 Phase 4: Testing

* [x] Manually test registration, login, logout
* [x] Test smoke log creation
* [x] Test log list visibility
* [x] Test unauthorized access

---

## 🚀 Phase 5: Deployment Plan

### Prepare for Deployment:

* [x] Switch to PostgreSQL for production
* [x] Use `.env` for secret key and DB credentials
* [x] Collect static files
* [x] Set `ALLOWED_HOSTS` and `DEBUG=False`

### Deployment Options:

* **PythonAnywhere** (easiest for beginners)
* **Render.com** or **Heroku** for cloud-based app

---

## 🌱 Phase 6: Future Improvements

| Feature           | Description                                   |
| ----------------- | --------------------------------------------- |
| Cost Tracking     | Calculate and display total cost of smoking   |
| Reminder System   | Email/SMS push if no log for hours            |
| Goal Tracker      | Reduce from X/day to Y/day                    |
| Graphs & Insights | Chart.js: daily/weekly trends                 |
| Quit Tracker      | “Days without smoking” counter                |
| Mobile Version    | Convert to PWA or connect to Flutter frontend |

---

## 📝 Git Commit Plan

| Commit Message                          |
| --------------------------------------- |
| `initial commit`                        |
| `add SmokeLog model and form`           |
| `create views for log and log list`     |
| `add templates and base layout`         |
| `implement user authentication`         |
| `add stats and analytics`               |
| `final polish and ready for deployment` |

---

## ✅ Summary Checklist

* [x] Project and app created
* [x] Models and forms built
* [x] All views and templates completed
* [x] Login/logout working
* [x] Stats working
* [x] Clean HTML templates
* [x] Deployment-ready
