-- USE healthcare_project;

SELECT p.name, p.age, p.gender, a.medical_condition, a.billing_amount FROM patients p
JOIN admission a ON p.patient_id = a.patient_id LIMIT 10;

SELECT medical_condition,COUNT(medical_condition) AS count_of_patients, ROUND(AVG(billing_amount), 2) AS avg_bill_amount FROM admission
GROUP BY medical_condition ORDER BY avg_bill_amount DESC;

SELECT p.name, ROUND(billing_amount, 2) FROM patients p
JOIN admission a ON p.patient_id = a.patient_id
WHERE a.billing_amount > (SELECT AVG(billing_amount) FROM admission);

SELECT DISTINCT doctor, ROUND(billing_amount, 2) AS bill_amount FROM admission
WHERE billing_amount > 40000;

SELECT AVG(p.age) AS avg_age, a.hospital, ROUND(SUM(a.billing_amount), 2) AS total_revenue FROM patients p
JOIN admission a ON p.patient_id = a.patient_id
GROUP BY a.hospital;

SELECT MAX(YEAR(date_of_admission)) AS max_admission , COUNT(admission_type) AS admission_count FROM admission
GROUP BY YEAR(date_of_admission) ORDER BY admission_count DESC

