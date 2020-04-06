# Command line comparisons on dt361

python ../sim_chime_scenario_runner.py dt361.cfg --scenario runner_cli_dt361 --output-path ./output/

penn_chime --file dt361.cfg
# Need to rename and move the output files to avoid overwriting
mv *_projected_admits.csv ./output/dt361_projected_admits.csv
mv *_projected_census.csv ./output/dt361_projected_census.csv
mv $(date +'%Y-%m-%d')_sim_sir_w_date.csv ./output/dt361_sim_sir_w_date.csv

# Command line comparisons on fd0220

python ../sim_chime_scenario_runner.py fd0220.cfg --scenario runner_cli_fd0220 --output-path ./output/

penn_chime --file fd0220.cfg
mv *_projected_admits.csv ./output/fd0220_projected_admits.csv
mv *_projected_census.csv ./output/fd0220_projected_census.csv
mv $(date +'%Y-%m-%d')_sim_sir_w_date.csv ./output/fd0220_sim_sir_w_date.csv

# diff the output files to compare
echo 'diff dt361_admits'
diff output/runner_cli_dt361_admits.csv output/dt361_projected_admits.csv
echo 'diff dt361_census'
diff output/runner_cli_dt361_census.csv output/dt361_projected_census.csv
echo 'diff dt361_sim_sir_w_date'
diff output/runner_cli_dt361_sim_sir_w_date.csv output/dt361_sim_sir_w_date.csv

# diff the output files to compare
echo 'diff fd0220_admits'
diff output/runner_cli_fd0220_admits.csv output/fd0220_projected_admits.csv
echo 'diff fd0220_census'
diff output/runner_cli_fd0220_census.csv output/fd0220_projected_census.csv
echo 'diff fd0220_sim_sir_w_date'
diff output/runner_cli_fd0220_sim_sir_w_date.csv output/fd0220_sim_sir_w_date.csv
