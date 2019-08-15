#!/bin/bash

pod_name=$(kubectl get pod -n take-on | awk '{print $1;}' | egrep "*$1*")
deployment_name=$(kubectl get deployment -n take-on | awk '{print $1;}' | egrep "*$1*")

if [ $2 == "delete" ];
    then
    deployment="deployment.apps/"$deployment_name
    echo $deployment_name
    kubectl delete deployment $deployment_name -n take-on
fi

if [ $2 == "build" ];
    then
    docker build -t 014669633018.dkr.ecr.eu-west-2.amazonaws.com/take-on-ui:test .
    docker push 014669633018.dkr.ecr.eu-west-2.amazonaws.com/take-on-ui:test
fi

if [ $2 == "deploy" ];
    then
    kubectl apply -f ~/Downloads/takeon-ui-test.yaml -n take-on
fi

if [ $2 == "logs" ];
    then
    pod="pod/"$pod_name 
    echo $pod
    kubectl logs $pod -n take-on
fi
