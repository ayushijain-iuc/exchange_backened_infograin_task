#!/usr/bin/env python3
"""
Quick Concurrency Test
"""

import asyncio
import aiohttp
import json

async def test_self_matching():
    """Test self-matching prevention"""
    print("🧪 Testing Self-Matching Prevention...")
    
    async with aiohttp.ClientSession() as session:
        # Create user
        async with session.post("http://localhost:8000/users/", 
                            json={"name": "Alice", "balance": 200000.0}) as resp:
            user = await resp.json()
            print(f"✅ Created user: {user['name']} (ID: {user['id']})")
        
        # Get initial trades
        async with session.get("http://localhost:8000/orders/trades/all") as resp:
            initial_trades = await resp.json()
            initial_count = len(initial_trades)
        
        # Place buy and sell for same user
        tasks = [
            session.post("http://localhost:8000/orders/", 
                      json={"user_id": user['id'], "symbol": "BTC", "side": "BUY", "price": 50000.0, "quantity": 2}),
            session.post("http://localhost:8000/orders/", 
                      json={"user_id": user['id'], "symbol": "BTC", "side": "SELL", "price": 50000.0, "quantity": 1})
        ]
        
        results = await asyncio.gather(*tasks)
        print(f"📝 Placed {len(results)} orders")
        
        # Check trades
        await asyncio.sleep(0.5)
        async with session.get("http://localhost:8000/orders/trades/all") as resp:
            final_trades = await resp.json()
            new_trades = len(final_trades) - initial_count
        
        if new_trades == 0:
            print("✅ Self-matching PREVENTED - No new trades")
            return True
        else:
            print(f"❌ Self-matching OCCURRED - {new_trades} new trades")
            return False

async def test_balance_validation():
    """Test balance validation"""
    print("\n🧪 Testing Balance Validation...")
    
    async with aiohttp.ClientSession() as session:
        # Create user with low balance
        async with session.post("http://localhost:8000/users/", 
                            json={"name": "Bob", "balance": 10000.0}) as resp:
            user = await resp.json()
            print(f"✅ Created user: {user['name']} (ID: {user['id']}, Balance: {user['balance']})")
        
        # Try to place order exceeding balance
        order_data = {
            "user_id": user['id'], 
            "symbol": "BTC", 
            "side": "BUY", 
            "price": 50000.0, 
            "quantity": 1  # Requires 50000, user has 10000
        }
        
        async with session.post("http://localhost:8000/orders/", json=order_data) as resp:
            if resp.status == 400:
                error = await resp.text()
                print("✅ Balance validation WORKED - Order rejected")
                print(f"   Error: {error}")
                return True
            else:
                print("❌ Balance validation FAILED - Order accepted")
                return False

async def test_race_condition():
    """Test race condition with identical orders"""
    print("\n🧪 Testing Race Condition Prevention...")
    
    async with aiohttp.ClientSession() as session:
        # Create users
        users = []
        for i in range(3):
            async with session.post("http://localhost:8000/users/", 
                                json={"name": f"User{i}", "balance": 100000.0}) as resp:
                user = await resp.json()
                users.append(user)
        
        print(f"✅ Created {len(users)} users")
        
        # Place identical orders simultaneously
        tasks = []
        for user in users:
            for i in range(2):  # 2 orders per user
                task = session.post("http://localhost:8000/orders/", 
                                 json={"user_id": user['id'], "symbol": "BTC", "side": "BUY", 
                                       "price": 50000.0, "quantity": 1})
                tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Check for unique order IDs
        successful = [r for r in results if hasattr(r, 'status') and r.status == 201]
        order_ids = []
        
        for result in successful:
            data = await result.json()
            order_ids.append(data['id'])
        
        unique_ids = set(order_ids)
        
        print(f"📝 Placed {len(successful)} orders")
        print(f"🆔 Order IDs: {order_ids}")
        
        if len(order_ids) == len(unique_ids):
            print("✅ Race condition PREVENTED - All order IDs unique")
            return True
        else:
            print("❌ Race condition DETECTED - Duplicate order IDs")
            return False

async def main():
    print("🚀 Quick Concurrency Test Suite")
    print("=" * 40)
    
    try:
        # Check server
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8000/health") as resp:
                if resp.status != 200:
                    print("❌ Server not running!")
                    return
        
        # Run tests
        test1 = await test_self_matching()
        test2 = await test_balance_validation()
        test3 = await test_race_condition()
        
        print("\n" + "=" * 40)
        print("📊 Results:")
        print(f"Self-matching prevention: {'✅ PASS' if test1 else '❌ FAIL'}")
        print(f"Balance validation: {'✅ PASS' if test2 else '❌ FAIL'}")
        print(f"Race condition prevention: {'✅ PASS' if test3 else '❌ FAIL'}")
        
        passed = sum([test1, test2, test3])
        print(f"\nOverall: {passed}/3 tests passed")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
