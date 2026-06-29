#!/usr/bin/env python3
"""
Sentinel Agent — Run with MetaMask Integration
Connect to COTI testnet using your MetaMask wallet
"""
import asyncio
import json
from coti_integration import CotiIntegration
from sentinel_agent import SentinelAgent

async def main():
    print("\n" + "="*60)
    print("🛡️  SENTINEL AGENT — METAMASK CONNECTION")
    print("="*60 + "\n")
    
    # Load config
    with open("config.json") as f:
        config = json.load(f)
    
    # Step 1: Get MetaMask address from user
    print("📋 INSTRUCTIONS:")
    print("1. Open MetaMask & switch to COTI Testnet")
    print("2. Copy your wallet address")
    print("3. Paste it below\n")
    
    metamask_address = input("🦊 Enter your MetaMask address: ").strip()
    
    if not metamask_address or not metamask_address.startswith("0x"):
        print("❌ Invalid address! Must start with 0x")
        return
    
    print(f"\n✅ Using wallet: {metamask_address}")
    print(f"📡 Network: {config['rpc_url']}")
    print(f"🔗 Chain ID: {config['chain_id']}\n")
    
    # Step 2: Initialize COTI integration with MetaMask
    coti = CotiIntegration(
        network=config["network"],
        rpc_url=config["rpc_url"],
        chain_id=config["chain_id"]
    )
    
    # Connect MetaMask wallet
    await coti.create_account(user_address=metamask_address)
    
    # Generate encryption key
    await coti.generate_aes_key()
    
    # Request gas grant (Starter Grant)
    grant_ok = await coti.request_starter_grant()
    
    if not grant_ok:
        print("\n⚠️  WARNING: No gas grant received!")
        print("   Request faucet tokens at: https://faucet.coti.io/")
        print(f"   Format: testnet {metamask_address}\n")
    
    # Step 3: Deploy private token
    print("\n" + "-"*60)
    token = await coti.deploy_private_erc20(
        name="BugBountyToken",
        symbol="BBT",
        initial_supply=1_000_000
    )
    
    # Step 4: Run Sentinel Agent
    print("\n" + "-"*60)
    agent = SentinelAgent()
    agent.wallet = coti.account
    agent.mcp_client = coti
    
    # Scan a test contract (mock)
    target_contract = "0x1234567890abcdef"
    await agent.run(target_contract)
    
    print("\n" + "="*60)
    print("✅ SESSION COMPLETE")
    print("="*60 + "\n")
    
    # Save session info
    session_data = {
        "wallet": metamask_address,
        "network": config["network"],
        "rpc_url": config["rpc_url"],
        "token_contract": token["contract_address"],
        "timestamp": "2026-06-30T06:47:00+07:00"
    }
    
    with open("session_output.json", "w") as f:
        json.dump(session_data, f, indent=2)
    
    print(f"💾 Session saved to: session_output.json\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
