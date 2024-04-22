import aiohttp
import asyncio
import time
import argparse


async def send_request(session, url):
    start_time = time.time()
    async with session.get(url) as response:
        await response.read()
        response.raise_for_status()
    response_time = time.time() - start_time
    return response_time


async def run(url, total_requests, concurrent_requests):
    start_time = time.time()
    ok_count, ok_time = 0, 0
    err_count, err_time = 0, 0
    connector = aiohttp.TCPConnector(limit_per_host=concurrent_requests)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [send_request(session, url) for _ in range(total_requests)]
        for future in asyncio.as_completed(tasks):
            try:
                response_time = await future
                ok_count += 1
                ok_time += response_time
            except Exception as exc:
                err_count += 1
                err_time += 1
                print('%s generated an exception: %s' % (url, exc))

    total_time = time.time() - start_time
    average_time = ok_time / ok_count if ok_count else 0
    error_rate = err_count / total_requests

    print(f"Total Time: {total_time} seconds")
    if ok_count:
        print(f"Average Time: {average_time} seconds")
    print(f"Error rate: {error_rate}")


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
    asyncio.run(run(args.url, args.requests, args.concurrent))
