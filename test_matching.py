#!/usr/bin/env python3
"""
Test Order Matching Logic
"""

import asyncio
import aiohttp

async def test_order_matching():
    """Test actual order matching between different users"""
    print("🧪 Testing Order Matching...")
    
    async with aiohttp.ClientSession() as session:
        # Create two users
        async with session.post("http://localhost:8000/users/", 
                            json={"name": "Alice", "balance": 100000.0}) as resp:
            alice = await resp.json()
        
        async with session.post("http://localhost:8000/users/", 
                            json={"name": "Bob", "balance": 100000.0}) as resp:
            bob = await resp.json()
        
        print(f"✅ Created users: Alice (ID: {alice['id']}), Bob (ID: {bob['id']})")
        
        # Get initial trades
        async with session.get("http://localhost:8000/orders/trades/all") as resp:
            initial_trades = await resp.json()
            initial_count = len(initial_trades)
        
        # Place matching orders
        tasks = [
            session.post("http://localhost:8000/orders/", 
                      json={"user_id": alice['id'], "symbol": "BTC", "side": "BUY", "price": 50000.0, "quantity": 2}),
            session.post("http://localhost:8000/orders/", 
                      json={"user_id": bob['id'], "symbol": "BTC", "side": "SELL", "price": 49500.0, "quantity": 1})
        ]
        
        results = await asyncio.gather(*tasks)
        print(f"📝 Placed {len(results)} orders")
        
        # Check results
        await asyncio.sleep(0.5)
        async with session.get("http://localhost:8000/orders/trades/all") as resp:
            final_trades = await resp.json()
            new_trades = len(final_trades) - initial_count
        
        # Check order book
        async with session.get("http://localhost:8000/orders/orderbook/BTC") as resp:
            order_book = await resp.json()
        
        print(f"💱 New trades executed: {new_trades}")
        print(f"📊 Order book - Buy orders: {len(order_book['buy_orders'])}, Sell orders: {len(order_book['sell_orders'])}")
        
        if new_trades > 0:
            print("✅ Order matching WORKING - Trades executed")
            return True
        else:
            print("❌ Order matching FAILED - No trades")
            return False

async def main():
    print("🚀 Order Matching Test")
    print("=" * 30)
    
    try:
        result = await test_order_matching()
        print(f"\nResult: {'✅ PASS' if result else '❌ FAIL'}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
