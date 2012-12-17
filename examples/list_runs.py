from pyAMI.client import AMIClient
from pyAMI.query import get_runs, get_periods_for_run

client = AMIClient()

runs = get_runs(client, periods=['B', 'K2'], year=11)
print runs
periods = get_periods_for_run(client, 201351)
print periods
