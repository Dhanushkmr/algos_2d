# Comparing the performance of the two algorithms
import logging
import argparse 

from deterministic_dfs import deterministic_dfs
from random_dfs import randomized_dfs

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str,
                        help='Path to CNF file', default='largeSat.cnf')
    args = parser.parse_args()

    logging.basicConfig(handlers=[logging.FileHandler(filename="test.log",
                                                      encoding='utf-8', mode='w')],
                        format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                        datefmt="%F %A %T",
                        level=logging.DEBUG)

    
    # comaparing time
    time_deterministic = deterministic_dfs(args.path)
    time_randomized = randomized_dfs(args.path)

    print("Deterministic: {}".format(time_deterministic))
    print("Randomized: {}".format(time_randomized))

    logging.info("Deterministic: {}".format(time_deterministic))
    logging.info("Randomized: {}".format(time_randomized))
    logging.info("Deterministic is {} times faster than randomized".format(
        time_deterministic / time_randomized))
