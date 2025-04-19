#!/usr/bin/env python3
"""
1. **Coroutines**: `fetch_data` and `process_data` are defined as coroutines with `async def`.
2. **await**: The `await` keyword pauses the coroutine, allowing the event loop to run other tasks.
3. **asyncio.run()**: This function starts the event loop and runs the `main` coroutine until it completes.
4. **asyncio.create_task()**: This schedules `fetch_data` and `process_data` to run concurrently.
"""

import asyncio

async def fetch_data():
    print( "Fetching data..." )
    await asyncio.sleep( 3 )  # Simulates a network request
    print( "Data fetched!" )
    return "Sample data"


async def process_data():
    print( "Processing data..." )
    await asyncio.sleep( 1 )  # Simulates a time-consuming computation
    print( "Data processed!" )


async def main():
    # Schedule both tasks to run concurrently
    fetch_task = asyncio.create_task( fetch_data() )
    process_task = asyncio.create_task( process_data() )

    # Wait for both tasks to complete
    print("Await allows us to pause here, but process task can run independently, so we'll likely get Processing print statements before Data fetched!")
    await fetch_task
    await process_task
    print("By awaiting on both tasks, we've ensured both are finished before we continue in this main loop task.")


# Run the event loop
asyncio.run( main() )