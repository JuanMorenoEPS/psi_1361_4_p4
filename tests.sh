#!/bin/bash


python3 manage.py test datamodel.tests_models

echo
echo "Executing tests_function from logic. . ."
echo

python3 manage.py test logic.tests_function

echo
echo "Executing tests_services from logic. . ."
echo

python3 manage.py test logic.tests_services

echo
echo "COMPLETED!"
echo
