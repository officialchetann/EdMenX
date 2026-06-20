import pandas as pd


def evaluate_cities(budget, priority, city_size, part_time):

    df = pd.read_csv("data/cities.csv")
    df.columns = df.columns.str.strip().str.lower()

    recommendations = []

    for _, row in df.iterrows():

        city = row["city"]

        monthly_expenses = row["monthly_expenses"]

        job_score = row["job_score"]

        student_score = row["student_score"]

        current_city_size = row["city_size"]

        difference = budget - monthly_expenses

        # Financial Score (0-40)

        if difference >= 400:
            financial_score = 40
        elif difference >= 250:
            financial_score = 35
        elif difference >= 100:
            financial_score = 30
        elif difference >= 0:
            financial_score = 20
        else:
            financial_score = 5

        # Job Score (0-30)

        job_points = (job_score / 100) * 30

        # Student Score (0-30)

        student_points = (student_score / 100) * 30

        total_score = (
            financial_score
            + job_points
            + student_points
        )

        if priority == "Affordability":
            total_score += financial_score * 0.10

        elif priority == "Career Opportunities":
            total_score += job_points * 0.15

        elif priority == "Student Life":
            total_score += student_points * 0.15

        if current_city_size == city_size:
            total_score += 10

        if part_time == "Yes":
            total_score += (job_points * 0.20)

        total_score = round(total_score, 1)

        reasons = []

        # Financial explanation
        if difference >= 300:
            reasons.append("Very affordable for your budget")
        elif difference >= 100:
            reasons.append("Comfortably within your budget")
        elif difference >= 0:
            reasons.append("Fits your budget with limited savings")
        else:
            reasons.append("May exceed your budget")

        # Job explanation
        if job_score >= 90:
            reasons.append("Excellent job market")
        elif job_score >= 75:
            reasons.append("Strong job market")
        elif job_score >= 60:
            reasons.append("Moderate job market")
        else:
            reasons.append("Developing job market")

        # Student explanation
        if student_score >= 90:
            reasons.append("Outstanding student environment")
        elif student_score >= 75:
            reasons.append("Excellent student environment")
        elif student_score >= 60:
            reasons.append("Good student environment")
        else:
            reasons.append("Average student environment")

        if total_score >= 85:
            confidence = "High"
        elif total_score >= 70:
            confidence = "Medium"
        else:
            confidence = "Low"

        recommendations.append({
            "city" : city,
            "score" : total_score,
            "confidence" : confidence,
            "reasons" : reasons
        })

    recommendations = sorted(

        recommendations,

        key=lambda x: x["score"],

        reverse=True

    )

    return recommendations