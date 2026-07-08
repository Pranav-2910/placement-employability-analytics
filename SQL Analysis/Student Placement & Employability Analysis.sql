-- creating a database
create database placement_analysis_db;
use placement_analysis_db;

-- creating a table
create table students (student_id int primary key, age int, gender varchar(10), degree varchar(10),
branch varchar(10), cgpa decimal(3,2), internships int, projects int, coding_skills int, 
communication_skills int, aptitude_test_score int, soft_skills_rating int, certifications int,
backlogs int, placement_status varchar(15), placed int, avg_skill_score DECIMAL(4,2),
experience_score INT);

-- checking if data is imported
select * from students;


-- implementing sql queries

-- 1 : overall placement percentage
select round(sum(case when placed = 1 then 1 else 0 end) * 100.0 / count(*), 2) as placement_percentage
from students;

-- 2 : branch wise placement rate
select branch, round(sum(case when placed = 1 then 1 else 0 end) * 100.0 / count(*), 2) as placement_rate
from students group by branch;

-- 3 : degree wise placement rate
select degree, round(sum(case when placed = 1 then 1 else 0 end) * 100.0 / count(*), 2) as placement_rate
from students group by degree;

-- 4 : average cgpa of placed and unplaced students
select placement_status, round(avg(cgpa),2) from students group by placement_status;

-- 5 : high cgpa but not placed
select student_id, cgpa from students where cgpa >= 8.0 and placed = 0;

-- 6 : getting employability score
select student_id, round(0.4 * avg_skill_score + 0.3 * experience_score + 0.2 * aptitude_test_score +
0.1 * soft_skills_rating, 2) as employability_score from students;

-- 7 : ranking students by employability score
select *, rank() over (order by employability_score desc) as emp_rank from (select 
student_id, 0.4 * avg_skill_score + 0.3 * experience_score + 0.2 * aptitude_test_score + 
0.1 * soft_skills_rating as employability_score from students) t;

-- 8 : classification of students over chances of placement
select student_id, case when avg_skill_score >= 75 and experience_score >= 60 then 'high'
when avg_skill_score >= 60 then 'medium' else 'low' end as placement_readiness from students;

-- 9 : checking impact of internship on placements
select internships, round(sum(placed) * 100.0 / count(*), 2) as placement_rate from students
group by internships;

-- 10 : students with certifications but not placed
select student_id, certifications, avg_skill_score from students where certifications > 0
and placed = 0;

-- 11 : checking impact of backlogs on placements
select backlogs, round(sum(placed) * 100.0 / count(*), 2) as placement_rate from students
group by backlogs;

-- 12 : gender wise placement analysis
select gender, round(sum(placed) * 100.0 / count(*), 2) as placement_rate from students
group by gender;

-- 13 : getting info of top 10 students over avg_skills_score
select student_id, avg_skill_score from students order by avg_skill_score desc limit 10;

-- 14 : checking branch wise employability score
select branch, round(avg(0.4 * avg_skill_score + 0.3 * experience_score + 0.2 * aptitude_test_score +
0.1 * soft_skills_rating), 2) as avg_employability from students group by branch;

-- 15 : students above branch average skill
select s.* from students as s join (select branch, avg(avg_skill_score) as avg_branch_skill
from students group by branch) b on s.branch = b.branch 
where s.avg_skill_score > b.avg_branch_skill;

-- 16 : impact of projects on placements
select internships, projects, round(sum(placed) * 100.0 / count(*), 2) as placement_rate 
from students group by internships, projects;

-- 17 : checking students with good skills but bad communication skills
select student_id, avg_skill_score, communication_skills, aptitude_test_score from students
where avg_skill_score >= 75 and communication_skills < 60;

-- 18 : classifiying students based on placement probability
select student_id, case when avg_skill_score >= 80 and experience_score >= 70 then 'very high'
when avg_skill_score >= 65 then 'high' when avg_skill_score >= 50 then 'medium' else 'low'
end as placement_probability from students;