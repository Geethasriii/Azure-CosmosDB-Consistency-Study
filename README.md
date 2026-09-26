# Azure Cosmos DB Consistency Level Selection Study

## Project Overview
This project studies different consistency levels in Azure Cosmos DB and compares their read performance using Python.

## Objectives
- Connect Python to Azure Cosmos DB.
- Perform CRUD operations on student records.
- Test different consistency levels.
- Measure and compare read response times.
- Develop a simple admin dashboard.

## Technologies Used
- Python
- Azure Cosmos DB for NoSQL
- Azure Portal
- Visual Studio Code
- Git and GitHub

## Consistency Levels
The project explores these five consistency levels:
- Strong
- Bounded Staleness
- Session
- Consistent Prefix
- Eventual

## Database Configuration
- Database: ConsistencyDB
- Container: studentDB
- Partition Key: /studentId

## Features
- Connect to Azure Cosmos DB
- View student records
- Add student records
- Update student records
- Delete student records
- Measure read response time
- Compare consistency-level test results

## How to Run

1. Install Python.
2. Install the required packages:

   pip install azure-cosmos python-dotenv

3. Create a `.env` file in the project folder.
4. Add your Azure Cosmos DB endpoint and key, along with the database and container names.
5. Run the Python program:

   python cosmos_test.py

## Results
The project records read response times for different consistency levels and compares their average performance.

## Author
Geetha Sri  
B.Tech - Computer Science and Engineering  
KL University