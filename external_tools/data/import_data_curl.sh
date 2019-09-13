#!/bin/bash

# REST API deployment details
protocol="http"
host="127.0.0.1"
port=80

protocol=$1
host=$2
port=$3

line=0
echo "========= Answers Started ========================="
# Answers Post operations
url="$protocol://$host:$port/match-api/v0/answers"
	# "What is your background?" "answers:" [1,2,3,4,5]
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Natural Science (Eg. Physics, Chemistry, Biology, etc)"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Mathematician"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Computer Programmer"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Data Scientist"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Business & Sales"}')
let "line++"
echo "$line,$status_code"
	# "How do you know hidalgo project?" "answers:" [6,7]
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Internet"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Referal from my friends"}')
let "line++"
echo "$line,$status_code"
	# "What is your profession?" "answers:" [8,9,10,11]
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Student"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Industry Researcher (Corporate Professionals)"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Academic Researcher (Phd, Postdoc, Professors)"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Business & Sales"}')
let "line++"
echo "$line,$status_code"
	# "What is an interest with hidalgo" "answers:" [12,13,14,15]
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "HPC Simulation Programming"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Mathematical Model"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Visualization Programming"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Small & Medium scale HPC business model"}')
let "line++"
echo "$line,$status_code"
	# "Do you need help from HiDALGO project professionals?"
	# "Are you part of HiDALGO project?"
	# Do you need help from HiDALGO to improve your small and medium scale business?
	# Are you familiar with the coupled simulation?
	# "answers:" [16,17]
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Yes"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "No"}')
let "line++"
echo "$line,$status_code"
	# "In which topic do you need a help?" "answers:" [18,19,20,21]
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Matchematical Model for Coupled Simulation"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "HPC Programming for Coupled Simulation"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Run Use Case in the HiDALGO infrastructure"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Run Use Case in a custom infrastructure"}')
let "line++"
echo "$line,$status_code"
	# "What is your HPC experience?"  "answers:" [22,23,24,25,26]
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Install & Benchmark HPC application"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "HPC programming to develop scientific models"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Optimize performance of the HPC code"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "HPC Visualization tools to export results"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Very Beginner"}')
let "line++"
echo "$line,$status_code"
	# Which HiDALGO use case is interesting for you? "answers:" [27,28,29,30]
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Urban Air Pollution (UAP) Pilot"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Social Networks (SN) Pilot"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Migraton Pilot"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Generic Usecase"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent $url)
let "line++"
echo "$line,$status_code"
id=31
echo "========================= Answers are created ==================================="
echo "Answer id-$id is created: {'text' : 'Yes'} "
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text" : "Yes"}')
let "line++"
echo "$line,$status_code"
echo "Answer id-$id is quering: "
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent "$url/$id")
let "line++"
echo "$line,$status_code"

echo "Answer id-$id is changed: {'text' : 'Yes Yes'} "
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X PUT $url -d '{"text" : "Yes Yes"}')
let "line++"
echo "$line,$status_code"
echo "Answer id-$id is quering: "
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent "$url/$id")
let "line++"
echo "$line,$status_code"
echo "Answer id-$id changes reverted: {'text' : 'Yes'} "
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X PUT $url -d '{"text" : "Yes"}')
let "line++"
echo "$line,$status_code"
echo "Answer id-$id is quering: "
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent "$url/$id")
let "line++"
echo "$line,$status_code"

echo "Answer id-$id is deleted: {'text' : 'Yes'} "
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X DELETE "$url/$id")
let "line++"
echo "$line,$status_code"
echo "Answer id-$id is quering & failed to get"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent "$url/$id")
let "line++"
echo "$line,$status_code"
echo "========================= Answer are updated for $id ==========================="
line=0
echo "========= Users Started ========================="
url="$protocol://$host:$port/match-api/v0/users"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"username": "test1"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"username": "test2"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"username": "test3"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"username": "test4"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent $url)
let "line++"
echo "$line,$status_code"
id=5
echo "========================= Users are created ======================================"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"username": "test1"}')
let "line++"
echo "$line,$status_code"
echo "User id-$id is changed to test11"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X PUT "$url/$id" -d '{"username": "test11" }')
let "line++"
echo "$line,$status_code"
echo "User id-$id is udated"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent "$url/$id")
let "line++"
echo "$line,$status_code"
let "line++"
echo "$line,$status_code"
echo "User id-$id is reverted"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X PUT "$url/$id" -d '{"username": "test1" }')
let "line++"
echo "$line,$status_code"
echo "User id-$id is deleted"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X DELETE "$url/$id")
let "line++"
echo "$line,$status_code"
let "line++"
echo "$line,$status_code"
echo "========================= User is updated for $id ================================"
	# "What is your background?" "answers:" [1,2,3,4,5]
	# "How do you know hidalgo project?" "answers:" [6,7]
	# "What is your profession?" "answers:" [8,9,10,11]
	# "What is an interest with hidalgo" "answers:" [12,13,14,15]
		# Yes or No Questions
	# "Do you need help from HiDALGO project professionals?"
	# "Are you part of HiDALGO project?"
	# Do you need help from HiDALGO to improve your small and medium scale business?
	# Are you familiar with the coupled simulation?
		# "answers:" [16,17]
	# "In which topic do you need a help?" "answers:" [18,19,20,21]
	# "What is your HPC experience?"  "answers:" [22,23,24,25,26]
	# Which HiDALGO use case is interesting for you? "answers:" [27,28,29,30]

line=0
echo "========= Questions Started ========================="
url="$protocol://$host:$port/match-api/v0/questions"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text": "What is your background?", "answers":[1,2,3,4,5]}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text": "How do you know hidalgo project?", "answers": [6,7]}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text": "What is your profession?", "answers": [8,9,10,11]}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text": "What is an interest with hidalgo", "answers": [12,13,14,15]}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text": "Do you need help from HiDALGO project professionals?", "answers": [16,17]}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text": "Are you part of HiDALGO project?", "answers": [16,17]}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text": "Do you need help from HiDALGO to improve your small and medium scale business?", "answers": [16,17]}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text": "Are you familiar with the coupled simulation?", "answers": [16,17]}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text": "In which topic do you need a help?", "answers": [18,19,20,21]}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text": "What is your HPC experience?", "answers": [22,23,24,25,26]}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text": "Which HiDALGO use case is interesting for you?", "answers": [27,28,29,30]}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent $url)
let "line++"
echo "$line,$status_code"
id=12
echo "======================== Questions are created perfectly =========================="
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"text": "Which HiDALGO use case is interesting for you?", "answers": [27,28,29,30]}')
let "line++"
echo "$line,$status_code"
echo "Question ID-$id is created"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent "$url/$id")
let "line++"
echo "$line,$status_code"
let "line++"
echo "$line,$status_code"
echo "Question id-$id is changed to 'Which' ans-add:'31,32', ans-remove:'27,28'"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X PUT "$url/$id" -d '{"text": "Which", "ans-remove":"27,28", "ans-add":"31,32"}')
let "line++"
echo "$line,$status_code"
echo "Question id-$id is updated"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent "$url/$id")
let "line++"
echo "$line,$status_code"
let "line++"
echo "$line,$status_code"
echo "Question id-$id is deleted"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X DELETE "$url/$id")
let "line++"
echo "$line,$status_code"
let "line++"
echo "$line,$status_code"

echo "======================== Questions are updated perfectly =========================="
line=0
echo "========= User Answers Started ========================="
url="$protocol://$host:$port/match-api/v0/user-answers"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":1,"question":1,"my_answer":1,"my_answer_importance":"Mandatory","their_answer": 1,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":1,"question":2,"my_answer":6,"my_answer_importance":"Mandatory","their_answer": 6,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":1,"question":3,"my_answer":8,"my_answer_importance":"Mandatory","their_answer": 8,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":1,"question":4,"my_answer":12,"my_answer_importance":"Mandatory","their_answer": 12,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":1,"question":5,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":1,"question":6,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":1,"question":7,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":1,"question":8,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":1,"question":9,"my_answer":18,"my_answer_importance":"Mandatory","their_answer": 18,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":1,"question":10,"my_answer":22,"my_answer_importance":"Mandatory","their_answer": 22,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":1,"question":11,"my_answer":27,"my_answer_importance":"Mandatory","their_answer": 27,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":2,"question":1,"my_answer":2,"my_answer_importance":"Mandatory","their_answer": 1,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":2,"question":2,"my_answer":7,"my_answer_importance":"Mandatory","their_answer": 6,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":2,"question":3,"my_answer":8,"my_answer_importance":"Mandatory","their_answer": 8,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":2,"question":4,"my_answer":12,"my_answer_importance":"Mandatory","their_answer": 12,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":2,"question":5,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":2,"question":6,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":2,"question":7,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":2,"question":8,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":2,"question":9,"my_answer":18,"my_answer_importance":"Mandatory","their_answer": 18,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":2,"question":10,"my_answer":22,"my_answer_importance":"Mandatory","their_answer": 22,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":2,"question":11,"my_answer":27,"my_answer_importance":"Mandatory","their_answer": 27,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":3,"question":1,"my_answer":3,"my_answer_importance":"Mandatory","their_answer": 1,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":3,"question":2,"my_answer":6,"my_answer_importance":"Mandatory","their_answer": 6,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":3,"question":3,"my_answer":10,"my_answer_importance":"Mandatory","their_answer": 8,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":3,"question":4,"my_answer":12,"my_answer_importance":"Mandatory","their_answer": 12,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":3,"question":5,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":3,"question":6,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":3,"question":7,"my_answer":17,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":3,"question":8,"my_answer":17,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":3,"question":9,"my_answer":18,"my_answer_importance":"Mandatory","their_answer": 18,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":3,"question":10,"my_answer":22,"my_answer_importance":"Mandatory","their_answer": 22,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":3,"question":11,"my_answer":27,"my_answer_importance":"Mandatory","their_answer": 27,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":4,"question":1,"my_answer":2,"my_answer_importance":"Mandatory","their_answer": 1,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":4,"question":2,"my_answer":7,"my_answer_importance":"Mandatory","their_answer": 6,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":4,"question":3,"my_answer":8,"my_answer_importance":"Mandatory","their_answer": 8,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":4,"question":4,"my_answer":12,"my_answer_importance":"Mandatory","their_answer": 12,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":4,"question":5,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":4,"question":6,"my_answer":17,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":4,"question":7,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":4,"question":8,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":4,"question":9,"my_answer":18,"my_answer_importance":"Mandatory","their_answer": 18,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":4,"question":10,"my_answer":24,"my_answer_importance":"Mandatory","their_answer": 22,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":4,"question":11,"my_answer":29,"my_answer_importance":"Mandatory","their_answer": 27,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
id=45
echo "================= User Answers are created ========================================"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user":1,"question":11,"my_answer":27,"my_answer_importance":"Mandatory","their_answer": 27,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X PUT $url/$id -d '{"user":2,"question":11,"my_answer":27,"my_answer_importance":"Mandatory","their_answer": 27,"their_importance":"Mandatory"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent $url/$id)
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X DELETE $url/$id)
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent $url/$id)
let "line++"
echo "$line,$status_code"
echo "================= User Answers $id is updated and deleted ========================="
line=0
echo "========= Matches Started ========================="
url="$protocol://$host:$port/match-api/v0/matches"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent $url)
let "line++"
echo "$line,$status_code"
echo "================= User Match detail is gathered          =========================="
line=0
echo "========= User Likes Started ========================="
url="$protocol://$host:$port/match-api/v0/user-likes"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user": 1, "liked_users": [2,3]}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user": 2, "liked_users": [1,3]}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user": 3, "liked_users": [2,4]}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user": 4, "liked_users": [2,3]}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent $url)
let "line++"
echo "$line,$status_code"
id=5
echo "================= User Likes detail is created ===================================="
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X POST $url -d '{"user": 4, "liked_users": [2,3]}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent $url/$id)
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X PUT $url/$id -d '{"add": "1,4", "remove": "2,3"}')
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent $url/$id)
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent -X DELETE $url/$id)
let "line++"
echo "$line,$status_code"
status_code=$(curl --write-out %{http_code} -Ls --out /dev/null --silent $url/$id)
let "line++"
echo "$line,$status_code"
echo "================= UsLikes $id is updatd and deleted =============================="
