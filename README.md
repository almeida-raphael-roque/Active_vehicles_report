# Activated License Plates Report Project

## 1) Main Objective of the Report

- The main objective of the report is to monitor two types of information: the movement of license plates among the three existing cooperatives and the respective total number of active plates.

    - Both types of information are analyzed in the context of the previous day;
    - The report is updated daily.

<br>

1) The possible situations regarding license plate movements are described as: "New", "Renewed", "Migration," and "Cancelled."

    - All are analyzed among the three cooperatives and also as a general total.

<br>

2) The other part of the analysis is to verify how many active plates exist in the three cooperatives and in the overall total.

<br>

## 2) Main Objective of the Project

- The report already existed previously, but its processes were time-consuming and inefficient. Additionally, there were errors and redundancies in the analysis across the three areas of construction: 
    - SQL queries;
    - ETL in Python;
    - Data treatment and modeling in Power Query and DAX metrics, respectively.

- Therefore, the main objective of the project is to **make the license plate monitoring report effective**.
    
    - Effectiveness means making it efficient (performant and organized) and accurate (correctly analyzing the data).

<br>

## 3) Scope of the Project

    Problematic

1) **SQL Query**
- Cancellation information was not included; such data depended on an Excel sheet filled out manually, resulting in missing or inconsistent information on several days;

- There were unused joins in the query;

- The previous query used for composing migration information ("listagem_mestra") was not ordered by date, leading to errors where the most recent status of the plate was not considered in the composition;

- This same query was not aligned with the others, as it used the current date in its script, which is incorrect since the report always analyzes the previous day.

<br>

2) **ETL in Python**
- The Transform phase had repeated functions between cooperatives, while one cooperative's data remained untreated;

- The Load phase updated information incrementally, without considering plate movements. As a result, the initial compositions of the table became outdated over time, yet they still contributed to the overall final plate count.

<br>

3) **Data Treatment and Modeling (Power BI)**
- The treatment in Power Query was redundant, as it filtered information from the generated report and mirrored it in the "f_vendas" table by "license plate." However, this same table was built with a principle very similar to the report itself, significantly reducing dashboard update performance and causing data loss;

- The data modeling, though correct, contained too much information, disorganized metrics, and calculated columns, which not only hindered dashboard performance but also complicated report maintenance and traceability of the information flow.

<br><br>

    Solutions

1) **SQL Query**
- A SQL query was added to retrieve cancellation information directly from the database;

- Unused joins were removed;

- A new query, "placas_total_ordem," was created, ordered by date. This ensured the most recent plate status was correctly reflected;

- In this query, the current date was excluded from the script since the report always analyzes the previous day;

- For script improvement, both in SQL and Python, queries were consolidated into a single query that distinguishes data by cooperative.

<br>

2) **ETL in Python**
- The errors mentioned in the Transform phase were corrected, and the necessary adjustments to incorporate cancellation data were made;

- In the Transform phase, a query was also added to create a report that only considers plates with the most recent status, which is the correct approach for analysis;

- The Load phase now generates two datasets: one that returns the current status of plates (considering only those updated daily) and another that returns the overall total of plates with their respective status correctly updated.

<br>

3) **Data Treatment and Modeling (Power BI)**
- The treatment in Power Query was simplified, now relying on only two data sources from SharePoint;

- The metrics were reorganized and reduced, resulting in better traceability, coherence, and dashboard performance.

<br><br>

    Results

1) Adding cancellation information directly from the database reduced human errors and enabled fast, daily, and accurate updates;

2) Consolidating queries with a `UNION ALL` made the SQL queries and the code more organized and "clean";

3) Correctly ordering the query that retrieves the total plates by activation date (as well as other adjustments made) allowed the return of plates with only the most updated status, solving the issue of outdated data in the final report;

4) All errors in the ETL Python code were corrected;

5) Generating two datasets—one for plate movements and another for the total plate composition—simplified subsequent data treatment in Power Query;

6) All changes enabled the creation of a much more organized, "light," and coherent dashboard that reflects the true state of license plates;

7) All stages are now organized and easy to understand and trace;

8) These steps reduced the time required to update the complete report from 20 minutes (15' Power BI + 5' Python) to 2 minutes and 30 seconds, a total reduction of 87.5% in update time;

9) The final report accurately reflects the plate situation across the three cooperatives;

10) Management and executives can safely and confidently analyze the plate situation within the company, make better decisions based on the provided report, and consequently increase the company's revenue.

<br><br>

    Next Steps

1) Add comments to the code for knowledge management;

2) Highlight in the dashboard that the difference between daily results in the metric "Plates Portfolio Current Day" (from the previous day) and "Plates Portfolio Previous Day" (from the current day) is due to changes in plate status from active to other available statuses. 

