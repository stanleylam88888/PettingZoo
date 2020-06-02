#!/bin/bash

render=True
manual_control=True
bombardment=True
performance=True
save_obs=True

python3 -m pettingzoo.tests.ci_test $pz_module $render $manual_control $bombardment $performance $save_obs

python3 -m pettingzoo.tests.print_test
if [[ -z $(grep '[^[:space:]]' test_output.txt) ]]
then
    echo "Test Passed"
    exit 0
else
    echo "Test Failed"
    exit 1
fi