from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
import json
from pywebpush import webpush

app = Flask(__name__)

JOB_URL = "https://www.indeed.ca/jobs?q=IT&l=Ottawa"
JOBS_FILE = "jobs.json"

# IMPORTANT: paste your VAPID keys here before deploying
VAPID_PRIVATE_KEY = "mNqatX3_eOyYCqVgujjQ0b3oE4rATitCgmDL_O01i9k"
VAPID_PUBLIC_KEY = "Jmes3V9pKUWGsKC0VmCSYl4cyplQ0AGC5Y3J-3F55vXBr8j5ghVkW37kXsUPNINGlu2TGHQY580UjSlzuFSq15c"

subscriptions = []

def fetch_jobs():
    jobs_list = []
    try:
        response = requests.get(JOB_URL, timeout=10, headers={ "User-Agent": "Mozilla/5.0 (compatible)" })
        soup = BeautifulSoup(response.text, 'html.parser')
        # This selector targets job cards on Indeed; if site changes you'll need to update selectors.
        for job_card in soup.find_all('div', class_='job_seen_beacon'):
            title_tag = job_card.find('h2')
            company_tag = job_card.find('span', class_='companyName')
            location_tag = job_card.find('div', class_='companyLocation')
            title = title_tag.get_text(strip=True) if title_tag else 'No title'
            company = company_tag.get_text(strip=True) if company_tag else 'Unknown'
            location = location_tag.get_text(strip=True) if location_tag else 'Ottawa'
            jobs_list.append({
                'title': title,
                'company': company,
                'location': location
            })
    except Exception as e:
        print("Error fetching jobs:", e)
    return jobs_list

def load_old_jobs():
    try:
        with open(JOBS_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return []

def save_jobs(jobs):
    with open(JOBS_FILE, 'w') as f:
        json.dump(jobs, f)

def send_push(subscription_info, message):
    try:
        webpush(
            subscription_info=subscription_info,
            data=message,
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={ "sub": "mailto:youremail@example.com" }
        )
    except Exception as e:
        print("Push error:", e)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    # simple in-memory store (for demo). For production persist subscriptions.
    subscriptions.append(data)
    return jsonify({"status": "success"}), 201

@app.route('/jobs')
def jobs():
    new_jobs = fetch_jobs()
    old_jobs = load_old_jobs()
    if new_jobs != old_jobs:
        save_jobs(new_jobs)
        for sub in subscriptions:
            send_push(sub, "New IT jobs available in Ottawa!")
    return jsonify(new_jobs)

@app.route('/')
def index():
    return render_template('index.html', vapid_public_key=VAPID_PUBLIC_KEY)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)