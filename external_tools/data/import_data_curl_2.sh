#!/bin/bash

# REST API deployment details
protocol="http"
host="127.0.0.1"
port=80
if [ $# -ne 3 ];
then
	echo "Script Usage is as follow: "
	echo "./import_data_curl.sh <protocol> <host> <port>"
	exit -1
else
	protocol=$1
	host=$2
	port=$3
fi

key="id"
line=0
id=0

function check_status()
{
	num_args=0
        id_received=0
	if if [ "$#" == 2 ]; then ! [ "$#" == 5 ]; else [ "$#" == 5 ]; fi;
	then
		num_args=$#
	else
		echo " error in number of args: $#"
		echo 0
	fi
	# Functionality for 3 parameter
	let "line=$1+1"
	local response=""
	response=$2
	#echo "response-1: $response"
	#echo $response | ( read body; read code; )
	#echo "$body, $code"
	response_a=(${response[@]}) # convert to array
	#echo "response-2: $response_a"
	code=${response_a[-1]} # get last element (last line)
	body=${response_a[@]::${#response_a[@]}-1} # get all elements except last
	#echo "$body, $code"
	if [ "$code" -gt 399 ] && [ "$code" -lt 600 ];
	then
		echo "$line, $body, $code"
		id_received=0
	fi
	if [ "$#" == 2 ]; then return 0; fi

	       # Functionality for 5 parameters
        keyword=$3
        id_expected=$4
        object=$5
        #echo "1 id_expected: $id_expected, id_received: $id_received"
        if [ "$keyword" == "id" ];
        then
	#	echo "$(echo $body | jq '.id')"
                id_received=$(echo $body | jq '.id')
        elif [ "$keyword" == "user" ];
        then
		re='^[0-9]+$'
                user_body=$(echo $body | jq '.user')
		if ! [[ $user_body =~ $re ]];
		then
			echo "user: $user_body"
			id_received=$(echo $user_body | jq '.id')
		else
			id_received=$user_body
		fi
        else
                id_received=0
        fi

        if [ -z "$id_received" ];
        then
                id_received=0
        fi
        #echo "2 id_expected: $id_expected, id_received: $id_received"
        if [ "$id_expected" != "$id_received" ];
        then
                echo "$object ID value is not same: expected: $id_expected, actual: $id_received"
        fi
        #echo "3 id_expected: $id_expected, id_received: $id_received"
        let "id=$id_received"
        #echo "line: $line, id: $id"
        if [ $id == 0 ];
        then
                echo "Exit due to error in the script"
        fi
}

echo "========= Answers Started ========================="
# Answers Post operations
url="$protocol://$host:$port/match-api/v0/answers"
	# "What is your background?" "answers:" [1,2,3,4,5]
curl_out=$(curl -s -w "\n%{http_code}" -d '{"text" : "Natural Science (Eg. Physics, Chemistry, Biology, etc)"}' -X POST $url)
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -d '{"text" : "Mathematician"}' -X POST $url)
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -d '{"text" : "Computer Programmer"}' -X POST $url)
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -d '{"text" : "Data Scientist"}' -X POST $url)
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -d '{"text" : "Business & Sales"}' -X POST $url)
check_status "$line" "$curl_out"

	# "How do you know hidalgo project?" "answers:" [6,7]
curl_out=$(curl -s -w "\n%{http_code}" -d '{"text" : "Internet"}' -X POST $url)
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "Referal from my friends"}')
check_status "$line" "$curl_out"

	# "What is your profession?" "answers:" [5,8,9,10]
curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "Student"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "Industry Researcher (Corporate Professionals)"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "Academic Researcher (Phd, Postdoc, Professors)"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "11 Dummy Answer"}')
check_status "$line" "$curl_out"

	# "What is an interest with hidalgo" "answers:" [12,13,14,15]
curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "HPC Simulation Programming"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "Mathematical Model"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "Visualization Programming"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "Small & Medium scale HPC business model"}')
check_status "$line" "$curl_out"

	# "Do you need help from HiDALGO project professionals?"
	# "Are you part of HiDALGO project?"
	# Do you need help from HiDALGO to improve your small and medium scale business?
	# Are you familiar with the coupled simulation?
	# "answers:" [16,17]
curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "Yes"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "No"}')
check_status "$line" "$curl_out"

	# "In which topic do you need a help?" "answers:" [18,19,20,21]
curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "Matchematical Model for Coupled Simulation"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "HPC Programming for Coupled Simulation"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "Run Use Case in the HiDALGO infrastructure"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "Run Use Case in a custom infrastructure"}')
check_status "$line" "$curl_out"

	# "What is your HPC experience?"  "answers:" [22,23,24,25,26]
curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "Install & Benchmark HPC application"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "HPC programming to develop scientific models"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "Optimize performance of the HPC code"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "HPC Visualization tools to export results"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "Very Beginner"}')
check_status "$line" "$curl_out"

	# Which HiDALGO use case is interesting for you? "answers:" [27,28,29,30]
curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "Urban Air Pollution (UAP) Pilot"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "Social Networks (SN) Pilot"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "Migraton Pilot"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "Generic Usecase"}')
check_status "$line" "$curl_out"

curl -s -w "\n%{http_code}" $url

echo "========================= Answers creation test is done ==================================="
id=31
key="id"
curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text" : "Yess"}')
check_status "$line" "${curl_out}" "$key" "$id" "Answer"
echo "Answer id-$id is created: {'text' : 'Yess'} "

curl_out=$(curl -s -w "\n%{http_code}" "$url/$id")
check_status "$line" "$curl_out"
echo "Answer id-$id is queried: "

curl_out=$(curl -s -w "\n%{http_code}" -X PUT $url/$id -d '{"text" : "Yes Yes"}')
check_status "$line" "$curl_out"
echo "Answer id-$id is changed: {'text' : 'Yes Yes'}"

curl_out=$(curl -s -w "\n%{http_code}" "$url/$id")
check_status "$line" "$curl_out"
echo "Answer id-$id is queried after changes"

curl_out=$(curl -s -w "\n%{http_code}" -X PUT $url/$id -d '{"text" : "Yes"}')
check_status "$line" "$curl_out"
echo "Answer id-$id is creating duplicate answers with same value & violating uniqueness"

curl_out=$(curl -s -w "\n%{http_code}" "$url/$id")
echo "Answer id-$id is queried after violation"

curl_out=$(curl -s -w "\n%{http_code}" -X DELETE "$url/$id")
check_status "$line" "$curl_out"
echo "Answer id-$id is deleted"

curl_out=$(curl -s -w "\n%{http_code}" "$url/$id")
check_status "$line" "$curl_out"
echo "Answer id-$id is queried & failed to get, because it is already deleted"

curl -s -w "\n%{http_code}" $url

echo "========================= Answer's updation test is done for $id ==========================="
line=0
echo "========= Users Started ========================="
url="$protocol://$host:$port/match-api/v0/users"
curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"username": "test1"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"username": "test2"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"username": "test3"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"username": "test4"}')
check_status "$line" "$curl_out"

curl -s -w "\n%{http_code}" $url

echo "========================= Users are created ======================================"
id=5
curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"username": "test"}')
key="id"
check_status "$line" "${curl_out}" "$key" "$id" "User"
echo "User id-$id is created with value 'test'"

curl_out=$(curl -s -w "\n%{http_code}" -X PUT "$url/$id" -d '{"username": "test11" }')
check_status "$line" "$curl_out"
echo "User id-$id is changed to test11"

curl_out=$(curl -s -w "\n%{http_code}" "$url/$id")
check_status "$line" "$curl_out"
echo "User id-$id is retrived after the updation"

curl_out=$(curl -s -w "\n%{http_code}" -X PUT "$url/$id" -d '{"username": "test1" }')
check_status "$line" "$curl_out"
echo "User id-$id is created by violating user uniqueness & updating with previous user name"

curl_out=$(curl -s -w "\n%{http_code}" -X DELETE "$url/$id")
check_status "$line" "$curl_out"
echo "User id-$id is deleted"

curl_out=$(curl -s -w "\n%{http_code}" "$url/$id")
check_status "$line" "$curl_out"
echo "User id-$id is retrived, it would be failed after deleting"

curl -s -w "\n%{http_code}" $url

echo "========================= User is updated for $id ================================"
	# "What is your background?" "answers:" [1,2,3,4,5]
	# "How do you know hidalgo project?" "answers:" [6,7]
	# "What is your profession?" "answers:" [5,8,9,10]
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
curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text": "What is your background?", "answers":[1,2,3,4,5]}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text": "How do you know hidalgo project?", "answers": [6,7]}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text": "What is your profession?", "answers": [5,8,9,10]}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text": "What is an interest with hidalgo", "answers": [12,13,14,15]}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text": "Do you need help from HiDALGO project professionals?", "answers": [16,17]}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text": "Are you part of HiDALGO project?", "answers": [16,17]}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text": "Do you need help from HiDALGO to improve your small and medium scale business?", "answers": [16,17]}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text": "Are you familiar with the coupled simulation?", "answers": [16,17]}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text": "In which topic do you need a help?", "answers": [18,19,20,21]}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text": "What is your HPC experience?", "answers": [22,23,24,25,26]}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text": "Which HiDALGO use case is interesting for you?", "answers": [27,28,29,30]}')
check_status "$line" "$curl_out"

curl -s -w "\n%{http_code}" $url

id=12
echo "======================== Questions are created perfectly =========================="
curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"text": "Which HiDALGO use case is interesting for UUU?", "answers": [27,28,29,30]}')
key="id"
check_status "$line" "${curl_out}" "$key" "$id" "Question"
echo "Question ID-$id is created"

curl_out=$(curl -s -w "\n%{http_code}" "$url/$id")
check_status "$line" "$curl_out"
echo "Question ID-$id is queried after the creation"

curl_out=$(curl -s -w "\n%{http_code}" -X PUT "$url/$id" -d '{"text": "Which", "ans-remove":"27,28", "ans-add":"11,12"}')
check_status "$line" "$curl_out"
echo "Question id-$id is changed to 'Which' ans-add:'31,32', ans-remove:'27,28'"

curl_out=$(curl -s -w "\n%{http_code}" "$url/$id")
check_status "$line" "$curl_out"
echo "Question id-$id is retrived after the updation"

curl_out=$(curl -s -w "\n%{http_code}" -X DELETE "$url/$id")
check_status "$line" "$curl_out"
echo "Question id-$id is deleted"

curl -s -w "\n%{http_code}" $url

echo "======================== Questions are updated perfectly =========================="
line=0
echo "========= User Answers Started ========================="
url="$protocol://$host:$port/match-api/v0/user-answers"
curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":1,"question":1,"my_answer":1,"my_answer_importance":"Mandatory","their_answer": 1,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":1,"question":2,"my_answer":6,"my_answer_importance":"Mandatory","their_answer": 6,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":1,"question":3,"my_answer":8,"my_answer_importance":"Mandatory","their_answer": 8,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":1,"question":4,"my_answer":12,"my_answer_importance":"Mandatory","their_answer": 12,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":1,"question":5,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":1,"question":6,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":1,"question":7,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":1,"question":8,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":1,"question":9,"my_answer":18,"my_answer_importance":"Mandatory","their_answer": 18,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":1,"question":10,"my_answer":22,"my_answer_importance":"Mandatory","their_answer": 22,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":1,"question":11,"my_answer":27,"my_answer_importance":"Mandatory","their_answer": 27,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":2,"question":1,"my_answer":2,"my_answer_importance":"Mandatory","their_answer": 1,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":2,"question":2,"my_answer":7,"my_answer_importance":"Mandatory","their_answer": 6,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":2,"question":3,"my_answer":8,"my_answer_importance":"Mandatory","their_answer": 8,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":2,"question":4,"my_answer":12,"my_answer_importance":"Mandatory","their_answer": 12,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":2,"question":5,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":2,"question":6,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":2,"question":7,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":2,"question":8,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":2,"question":9,"my_answer":18,"my_answer_importance":"Mandatory","their_answer": 18,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":2,"question":10,"my_answer":22,"my_answer_importance":"Mandatory","their_answer": 22,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":2,"question":11,"my_answer":27,"my_answer_importance":"Mandatory","their_answer": 27,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":3,"question":1,"my_answer":3,"my_answer_importance":"Mandatory","their_answer": 1,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":3,"question":2,"my_answer":6,"my_answer_importance":"Mandatory","their_answer": 6,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":3,"question":3,"my_answer":10,"my_answer_importance":"Mandatory","their_answer": 8,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":3,"question":4,"my_answer":12,"my_answer_importance":"Mandatory","their_answer": 12,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":3,"question":5,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":3,"question":6,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":3,"question":7,"my_answer":17,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":3,"question":8,"my_answer":17,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":3,"question":9,"my_answer":18,"my_answer_importance":"Mandatory","their_answer": 18,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":3,"question":10,"my_answer":22,"my_answer_importance":"Mandatory","their_answer": 22,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":3,"question":11,"my_answer":27,"my_answer_importance":"Mandatory","their_answer": 27,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":4,"question":1,"my_answer":2,"my_answer_importance":"Mandatory","their_answer": 1,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":4,"question":2,"my_answer":7,"my_answer_importance":"Mandatory","their_answer": 6,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":4,"question":3,"my_answer":8,"my_answer_importance":"Mandatory","their_answer": 8,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":4,"question":4,"my_answer":12,"my_answer_importance":"Mandatory","their_answer": 12,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":4,"question":5,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":4,"question":6,"my_answer":17,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":4,"question":7,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":4,"question":8,"my_answer":16,"my_answer_importance":"Mandatory","their_answer": 16,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":4,"question":9,"my_answer":18,"my_answer_importance":"Mandatory","their_answer": 18,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":4,"question":10,"my_answer":24,"my_answer_importance":"Mandatory","their_answer": 22,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":4,"question":11,"my_answer":29,"my_answer_importance":"Mandatory","their_answer": 27,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"

curl -s -w "\n%{http_code}" $url

echo "================= User Answers are created ========================================"
curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user":1,"question":11,"my_answer":27,"my_answer_importance":"Mandatory","their_answer": 27,"their_importance":"Mandatory"}')
id=45
key="id"
check_status "$line" "${curl_out}" "$key" "$id" "User Answers"
echo "user answer is created for id: $id"

curl_out=$(curl -s -w "\n%{http_code}" -X PUT $url/$id -d '{"user":2,"question":11,"my_answer":27,"my_answer_importance":"Mandatory","their_answer": 27,"their_importance":"Mandatory"}')
check_status "$line" "$curl_out"
echo "user answer is updated for id: $id"

curl_out=$(curl -s -w "\n%{http_code}" $url/$id)
check_status "$line" "$curl_out"
echo "user answer is retrived after the updation"

curl_out=$(curl -s -w "\n%{http_code}" -X DELETE "$url/$id")
check_status "$line" "$curl_out"
echo "user answer is deleted"

curl_out=$(curl -s -w "\n%{http_code}" $url/$id)
check_status "$line" "$curl_out"
echo "user answer is retrived after deleting"

curl -s -w "\n%{http_code}" $url

echo "================= User Answers $id is updated and deleted ========================="
line=0
echo "========= Matches Started ========================="
url="$protocol://$host:$port/match-api/v0/matches"
curl_out=$(curl -s -w "\n%{http_code}" $url)
check_status "$line" "$curl_out"

id=1
key="id"
curl_out=$(curl -s -w "\n%{http_code}" "$url/$id")
check_status "$line" "${curl_out}" "$key" "$id" "Matches"
echo "Match-Id : $id details"

curl -s -w "\n%{http_code}" $url

echo "================= User Match detail is queried    =========================="
line=0
echo "========= User Likes Started ========================="
url="$protocol://$host:$port/match-api/v0/user-likes"
curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user": 1, "liked_users": [2,3]}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user": 2, "liked_users": [1,3]}')
check_status "$line" "$curl_out"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user": 3, "liked_users": [2,4]}')
check_status "$line" "$curl_out"

curl -s -w "\n%{http_code}" $url

echo "================= User Likes detail is created ===================================="
id=4
curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user": 4, "liked_users": [2,3]}')
key="user"
check_status "$line" "${curl_out}" "$key" "$id" "User Likes"
echo "user likes is created for id: $id"

curl_out=$(curl -s -w "\n%{http_code}" $url/$id)
check_status "$line" "$curl_out"
echo "user likes is queried"

curl_out=$(curl -s -w "\n%{http_code}" -X PUT $url/$id -d '{"add": "1,4", "remove": "2,3"}')
check_status "$line" "$curl_out"
echo "user likes is updated"

curl_out=$(curl -s -w "\n%{http_code}" $url/$id)
check_status "$line" "$curl_out"
echo "user likes is queried after the updation"

curl_out=$(curl -s -w "\n%{http_code}" -X DELETE "$url/$id")
check_status "$line" "$curl_out"
echo "user likes is deleted"

curl_out=$(curl -s -w "\n%{http_code}" $url/$id)
check_status "$line" "$curl_out"
echo "user likes is queried after deleting"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user": 4, "liked_users": [2,3]}')
check_status "$line" "$curl_out"
echo "user likes is created once again after deleting"

curl_out=$(curl -s -w "\n%{http_code}" -X POST $url -d '{"user": 4, "liked_users": [2,3]}')
check_status "$line" "$curl_out"
echo "user likes is created by violating the duplication"

curl -s -w "\n%{http_code}" $url

echo "================= User Likes $id is updated and deleted =============================="
