import os
from dotenv import load_dotenv

load_dotenv()

CATEGORY_WEIGHTS={
    "Market Manipulation": 50,
    "Market Bribery": 45,
    "Employee Ethics": 35,
    "Secrecy": 25,
    "Complaints" : 15,
    "Change in Communication": 10
}