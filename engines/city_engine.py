import pandas as pd


def evaluate_cities(budget):

    df = pd.read_csv("data/cities.csv")

    recommendations = []

    for _, row in df.iterrows():

        city = row["city"]

        monthly_expenses = row["monthly_expenses"]

        job_score = row["job_score"]

        student_score = row["student_score"]

        # Financial Score (40)

        difference = budget - monthly_expenses
        if difference >= 300:
            financial_score = 50
        elif difference >= 100:
            financial_score = 45
        elif difference >= 0:
            financial_score = 30
        else:
            financial_score = 5

        # Job Score (25)

        job_points = (job_score / 100) * 25

        # Student Score (25)

        student_points = (student_score / 100) * 25

        total_score = round(
            financial_score
            + job_points
            + student_points,
            1
        )

        recommendations.append({

            "city": city,

            "score": total_score

        })

    recommendations = sorted(

        recommendations,

        key=lambda x: x["score"],

        reverse=True

    )

    return recommendations