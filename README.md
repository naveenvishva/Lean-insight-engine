# 📘 Lean Insight Engine  
**Memory-Efficient Analysis of 3M+ Amazon Book Reviews using Pandas, NumPy & Tableau**

> A portfolio-ready project showcasing scalable data processing, visualization, and performance optimization on large-scale retail datasets.

---

## 🚀 Project Overview

This project processes a **2.8 GB dataset** of 3 million Amazon book reviews to extract insights in a **memory-efficient** and **scalable** manner using Python. It avoids the traditional pitfalls of large CSV analysis by implementing:

- **Chunk-based processing** for efficient row-wise aggregation
- **Dtype optimization** to reduce memory footprint (~85% lower)
- **Lazy evaluation techniques** for on-demand statistics
- **Data visualization** using both Python (Matplotlib/Seaborn) and Tableau

---

## 🔍 Dataset Source

The dataset contains over **3 million book reviews** from Amazon users with metadata including title, price, user ID, review score, helpfulness, timestamps, and text reviews.

📥 **Download from Kaggle**:  
https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews

> Note: Data is not included in this repo due to size. Download manually and place inside the `data/` folder.

---

## 📊 Features & Analysis Goals

- ✅ **Dtype optimization** for memory (e.g., float64 → float32, string → category)
- ✅ **Chunk-based summary** (mean rating, review count per book)
- ✅ **Time trend analysis** (review volume over time)
- ✅ **Sentiment word clouds** from review text
- ✅ **Genre-based score comparison** (using second file from Kaggle)
- ✅ **Export to CSV for Power BI / Tableau visualization**

---

## 🧪 Tech Stack

- Python 3.x
- Pandas, NumPy
- Matplotlib, Seaborn, WordCloud, TextBlob
- Tableau Public (for dashboard)

---
