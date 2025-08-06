
A real-world clothing size recommendation system API inspired by SizeCharter.com.  
This Flask-based REST API provides personalized size recommendations based on detailed body measurements and morphology, with intelligent analysis and real-world sizing logic for women’s, men’s, and maternity categories.

---

## Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Getting Started](#getting-started)  
4. [API Usage](#api-usage)  
5. [Input Parameters](#input-parameters)  
6. [Response Format](#response-format)  
7. [Algorithm Highlights](#algorithm-highlights)  
8. [Examples](#examples)  
9. [Contributing](#contributing)  
10. [License](#license)  

---

## Overview

The SizeCharter Mimic API intelligently recommends clothing sizes based on:

- Comprehensive body measurements (chest, waist, hips, inseam, shoulders, neck, thigh, calf)  
- Body morphology including body shape, abdomen shape, and hip shape  
- Realistic health checks and measurement consistency warnings  
- Multi-gender support: women's, men's, and maternity sizing rules  

The API is designed for integration with any app or platform, offering JSON REST endpoints with CORS enabled.

---

## Features

- **Advanced body shape inference** using multiple body metrics  
- **Dominant measurement detection** for personalized size impact analysis  
- **Morphology-based measurement adjustments** for a tailored fit  
- **Health and consistency warnings** to alert unusual inputs  
- **Multi-category sizing**: women's, men's, maternity  
- **Lightweight Flask REST API** with CORS support  
- Ready for easy integration with web, mobile, or desktop apps  

---

## Getting Started

### Prerequisites

- Python 3.8+  
- `pip` package manager  

### Installation

```bash
git clone https://github.com/foudhilriahi/sizecharter-mimic.git
cd sizecharter-mimic
pip install -r requirements.txt  # Flask, Flask-CORS


python sizecharter_api.py


API Usage
Endpoint
bash
Copy
Edit
POST /api/size
Content-Type: application/json
Example Request
json
Copy
Edit
{
  "gender": "womens",
  "chest": 85,
  "waist": 68,
  "hips": 94,
  "shoulders": 40,
  "neck": 33,
  "thigh": 55,
  "calf": 36,
  "abdomen_shape": "hourglass",
  "hip_shape": "curved"
}
Response