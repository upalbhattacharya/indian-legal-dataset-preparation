# README

Overview of scripts.

 - `create_per_target_balanced_splits.py`: Creates a train-test-validation split
  on a set of datapoints given their targets. For each target, splits the
  datapoints of the target into three splits by the given proportion and ensures
  a minimal (user-defined) value of representation of each target in the
  training and testing splits. DOES NOT ensure the same for the validation split
  due to insufficient representation for a large number of targets (for the
  advocate recommendation use-case).
 - `run_create_per_target_balanced_splits.sh`: Helper script for executing
   `create_per_target_balanced_splits.py` by passing command-line arguments.

#TODO: Update other scripts
