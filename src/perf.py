import requests
import time
import argparse
from concurrent import futures


def send_request(url):
    start_time = time.time()
    response = requests.get(url)
    response.raise_for_status()
    response_time = time.time() - start_time
    return response_time


def run(url, total_requests, concurrent_requests):
    start_time = time.time()
    ok_count, ok_time = 0, 0
    err_count, err_time = 0, 0
    with futures.ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
        future_to_time = {
            executor.submit(send_request, url): url for _ in range(total_requests)
        }
        for future in futures.as_completed(future_to_time):
            url = future_to_time[future]
            try:
                response_time = future.result()
                ok_count += 1
                ok_time += response_time
            except Exception as exc:
                err_count += 1
                err_time += 1
                print('%r generated an exception: %s' % (url, exc))
    print("Total Time: %s seconds" % (time.time() - start_time))
    print("Average Time: %s seconds" % (ok_time / ok_count))
    print("Error rate: %s" % (err_count / total_requests))


def cmd_parse():
    parser = argparse.ArgumentParser(
        description="Simple HTTP Performance Testing Tool")
    parser.add_argument("url", help="URL to test")
    parser.add_argument("-r", "--requests", type=int, default=100,
                        help="Total number of requests")
    parser.add_argument("-c", "--concurrent", type=int, default=4,
                        help="Number of concurrent requests")
    return parser.parse_args()


if __name__ == "__main__":
    args = cmd_parse()
    run(args.url, args.requests, args.concurrent)
