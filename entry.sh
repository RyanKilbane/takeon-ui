#! /bin/ash
	eurekaIp=$(getent hosts eurekaserver | awk '{ print $1}')
	export localEurekaServerURL="http://$eurekaIp:8761"
	echo $localEurekaServerURL
	python application.py runserver
