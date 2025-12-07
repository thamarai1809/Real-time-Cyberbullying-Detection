# Real-time-Cyberbullying-Detection

AI-Based Real-Time Cyberbullying Detection for Online Classrooms
Overview

This project focuses on detecting and preventing cyberbullying in virtual classroom environments using artificial intelligence. As online learning becomes increasingly widespread, students are more exposed to harmful digital interactions. Manual monitoring of online communications is often inefficient and impractical.

This system leverages AI-driven text analysis to monitor chat messages in real time, identify toxic or harmful content, and alert moderators or teachers for timely intervention. The goal is to establish a safer and more respectful digital learning environment.

# Objectives

The primary objective of this project is to build an intelligent, automated framework capable of:

Monitoring online classroom chats in real time

Detecting bullying, threats, insults, and harmful expressions

Sending instant alerts to educators or administrators

Supporting early intervention and improving student well-being

# Key Features
### 1. Real-Time Monitoring

Continuously captures and processes chat messages from online classroom platforms or simulated chat environments.

### 2. Toxicity Detection

Utilizes AI models to identify bullying-related patterns, including threats, insults, abusive language, and aggressive behavior.

### 3. Instant Alerts

Generates real-time notifications for teachers or moderators when high-risk messages are detected.

### 4. Sentiment and Emotion Analysis

Analyzes tone, sentiment, and emotion to detect indirect, subtle, or context-dependent forms of cyberbullying.

### 5. Auto Prioritization

Classifies incidents based on severity using a dynamic risk score, helping educators prioritize high-risk interactions.

### 6. Moderator Dashboard

Displays flagged messages, user information, timestamps, and severity levels for efficient review and response.

# Technology Stack
### Frontend

React.js (User Interface)

### Backend

Flask (API and server-side processing)

### AI / NLP Models

Google Perspective API (toxicity detection)

TextBlob / VADER (sentiment analysis)

BERT (optional for advanced NLP and context understanding)

### Preprocessing

NLTK (natural language processing and text cleaning)

### Database

SQL (storage of messages, flagged incidents, and user metadata)

### Alert System

Email notifications (SMTP)

In-app alerts (optional)

### Deployment

Hosted on Render

# Significance

Online learning environments expose students to increasing risks of digital harassment.
Manual monitoring of classroom chats is often inadequate.
This system provides an automated and intelligent solution to detect, classify, and report cyberbullying incidents.
It supports educators in maintaining a safe, positive digital classroom experience.
