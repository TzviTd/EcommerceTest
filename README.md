# 🧩 E-Commerce QA Automation Project

Automated UI testing for Automation training website [SauceDemo](https://www.saucedemo.com/) that imitates online shop built with **Python**, **Selenium**, **unittest**, **Allure**, and **uv**.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Selenium](https://img.shields.io/badge/Selenium-4-green)
![Allure](https://img.shields.io/badge/Allure-Report-orange)
![uv](https://img.shields.io/badge/uv-Dependency_Manager-purple)


---

## 📁 Project Structure

```
EcommerceTest/
├─ src/
│  ├─ base_test.py               # Base TestCase (headless/visible mode, Allure screenshots)
│  ├─ pages/                     # Page Object Model
│  │  ├─ login_page.py
│  │  ├─ main_page.py
│  │  ├─ cart_page.py
│  │  └─ checkout_page.py        # Step One / Step Two / Complete pages
├─ tests/
│  ├─ test_1.py … test_4.py      # Test suites
│  └─ conftest.py                # Adds src to sys.path automatically
├─ pyproject.toml                # uv + pytest configuration and dependencies
└─ README.md                     # this file
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/EcommerceTest.git
cd EcommerceTest
```

### 2️⃣ Install dependencies using uv

```bash
uv sync
```

### 3️⃣ Check Allure installation

```bash
allure --version
```

If Allure is not found, install it:

```powershell
# Windows (PowerShell)
scoop install allure
# or
choco install allure-commandline
```

---

## 🧠 Headless vs. Visible Browser Mode

Control Chrome visibility using the `HEADLESS` environment variable:

| Mode | Environment variable | Description |
|------|----------------------|--------------|
| 🧩 Headless | `HEADLESS=true` | runs in background (default for CI/CD) |
| 👀 Visible | `HEADLESS=false` | opens real Chrome window (for debugging) |

---

## 🚀 Running Tests

### PowerShell (Windows)
```powershell
cd C:\QA39\Python\Workspace\EcommerceTest
$env:PYTHONPATH = "$PWD"           # only if you don't have tests/conftest.py
$env:HEADLESS = "false"            # run with visible browser
uv run pytest -v --alluredir=allure-results
```

### Command Prompt (cmd)
```cmd
set PYTHONPATH=%CD%
set HEADLESS=false
uv run pytest -v --alluredir=allure-results
```

---

## 📊 Allure Reports

### Temporary report (auto-opens in browser)
```bash
allure serve allure-results
```

### Static HTML report
```bash
allure generate allure-results -o allure-report --clean
start allure-report\index.html   # Windows
```

---

## 🧱 Tech Stack

| Component | Purpose |
|------------|----------|
| **Python 3.13** | Core language |
| **Selenium 4** | UI automation |
| **unittest / pytest** | Test framework & runner |
| **Allure 2** | Test reports, steps, screenshots |
| **uv** | Environment & dependency manager |
| **Page Object Model (POM)** | Clean test architecture |

---

## 🧩 Key Features

- ✅ **Headless & visible browser support** via `HEADLESS` env variable  
- 📸 **Automatic screenshots** attached to Allure on failure  
- 🧱 **Page Object Model** for maintainable test design  
- 🧩 **Explicit waits only** — no implicit waits to avoid flakiness  
- 💬 **Allure steps** and diagnostic URLs for better report traceability  
- 🔄 **Cross-platform**: works in Windows, macOS, and Linux environments  

---

## 🧪 Example Commands

| Goal | Command |
|------|----------|
| Run tests in headless mode | `$env:HEADLESS="true"; uv run pytest -v --alluredir=allure-results` |
| Run tests with GUI | `$env:HEADLESS="false"; uv run pytest -v --alluredir=allure-results` |
| Generate report | `allure serve allure-results` |
| Reset variable | `Remove-Item Env:\HEADLESS` |

---

## 🧾 Diagnostics & Debugging

Each test includes diagnostic steps like:

```python
with allure.step(f"URL: {self.driver.current_url}"): pass
```

Failures automatically attach:
- Screenshot  
- Current URL  
- (Optionally) full DOM snapshot  

This helps identify where and why a test failed, especially in headless mode.

---

## ⚡ Tips for Stability

- Always use **explicit waits** (`WebDriverWait` + `expected_conditions`).
- Before each click: `scrollIntoView()` + `element_to_be_clickable`.
- For headless runs: window size is fixed to `1920x1080`.
- On failure: screenshots are attached before quitting the browser.

---

## 💡 Author Notes

This project is a full working QA Automation framework for educational use.  
It demonstrates:
- real-world Page Object design,
- stable multi-step UI flows (login → cart → checkout),
- Allure integration for professional reporting.
