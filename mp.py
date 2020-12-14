# for testing multiprocess stuff

import multiprocessing as mp

def my_func(x, y):
  return(x**y)

def main():
  pool = mp.Pool(2)
  result = pool.starmap(my_func, [(4,2),(5,2),(6,2)])
  print(result)
  

if __name__ == '__main__':
    main()