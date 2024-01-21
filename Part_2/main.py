from multiprocessing import cpu_count, Pool
from time import time


def factorize(*number):
    result = []
    for num in number:
        res = []
        for i in range(1, num + 1):
            if num % i == 0:
                res.append(i)
        result.append(res)
    return result


def callback(result):
    print(f'Result: {result}')


if __name__ == '__main__':
    print(f'CPU count: {cpu_count()}\n')

    a, b, c, d = (128, 255, 99999, 10651060)

    # Synchronous code execution with 1 process
    timer = time()
    result_1_process = factorize(a, b, c, d)
    print(f'Result: {result_1_process}')
    print(f'Done by 1 process: {round(time() - timer, 4)} sec.\n')

    # Parallel code execution with 4 processes
    with Pool(4) as pool:
        pool.apply_async(factorize, (a, b, c, d), callback=callback)
        pool.close()
        pool.join()
    print(f'Done by 4 processes: {round(time() - timer, 4)} sec.\n')

    # Parallel code execution by (cpu_count()) processes
    timer = time()
    with Pool(cpu_count()) as pool:
        pool.apply_async(factorize, (a, b, c, d), callback=callback)
        pool.close()
        pool.join()
    print(f'Done by {cpu_count()} processes: {round(time() - timer, 4)} sec.')
