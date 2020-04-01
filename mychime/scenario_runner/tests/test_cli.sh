# Command line comparisons on dt361

python ../sim_chime_scenario_runner.py cli_inputs_semi_dt3.61.cfg --scenario runner_cli_dt361 --output-path ./output/

penn_chime --file cli_inputs_semi_dt3.61.cfg
# Need to rename and move the output files to avoid overwriting
mv *_projected_admits.csv ./output/dt361_projected_admits.csv
mv *_projected_census.csv ./output/dt361_projected_census.csv
mv $(date +'%Y-%m-%d')_sim_sir_w_date.csv ./output/dt361_sim_sir_w_date.csv

# Command line comparisons on cli_inputs_semi_fd2020-02-20

python ../sim_chime_scenario_runner.py cli_inputs_semi_fd2020-02-20.cfg --scenario runner_cli_fd2020-02-20 --output-path ./output/

penn_chime --file cli_inputs_semi_fd2020-02-20.cfg
mv *_projected_admits.csv ./output/fd2020-02-20_projected_admits.csv
mv *_projected_census.csv ./output/fd2020-02-20_projected_census.csv
mv $(date +'%Y-%m-%d')_sim_sir_w_date.csv ./output/fd2020-02-20_sim_sir_w_date.csv

# diff the output files to compare
echo 'diff dt361_admits'
diff output/runner_cli_dt361_admits.csv output/dt361_projected_admits.csv
echo 'diff dt361_census'
diff output/runner_cli_dt361_census.csv output/dt361_projected_census.csv
echo 'diff dt361_sim_sir_w_date'
diff output/runner_cli_dt361_sim_sir_w_date.csv output/dt361_sim_sir_w_date.csv

# diff the output files to compare
echo 'diff fd2020-02-20_admits'
diff output/runner_cli_fd2020-02-20_admits.csv output/fd2020-02-20_projected_admits.csv
echo 'diff fd2020-02-20_census'
diff output/runner_cli_fd2020-02-20_census.csv output/fd2020-02-20_projected_census.csv
echo 'diff fd2020-02-20_sim_sir_w_date'
diff output/runner_cli_fd2020-02-20_sim_sir_w_date.csv output/fd2020-02-20_sim_sir_w_date.csv
