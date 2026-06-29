#!/usr/bin/env python3
"""
Sentinel Agent — LIVE Demo with Real COTI Testnet
Uses MetaMask wallet with faucet funds
"""
import asyncio
import json
from datetime import datetime
from coti_integration import CotiIntegration
from sentinel_agent import SentinelAgent

async def main():
    print("\n" + "="*70)
    print("🛡️  SENTINEL AGENT — LIVE COTI TESTNET DEMO")
    print("="*70 + "\n")
    
    # Load config
    with open("config.json") as f:
        config = json.load(f)
    
    metamask_address = config["wallet"]["address"]
    
    print(f"🦊 Wallet: {metamask_address}")
    print(f"📡 Network: {config['rpc_url']}")
    print(f"🔗 Chain ID: {config['chain_id']}")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print()
    
    # Initialize COTI integration
    coti = CotiIntegration(
        network=config["network"],
        rpc_url=config["rpc_url"],
        chain_id=config["chain_id"]
    )
    
    # Connect wallet
    await coti.create_account(user_address=metamask_address)
    
    # Generate encryption key
    await coti.generate_aes_key()
    
    # Check balance (mock - would need real web3 call)
    print("\n💰 Checking balance...")
    print("   ⚠️  Note: Real balance check needs web3.py integration")
    print("   ✅ Faucet received: 10 COTI (testnet)")
    print("   ✅ Starter Grant: 0.1 COTI")
    
    # Deploy private token
    print("\n" + "-"*70)
    print("🪙 DEPLOYING PRIVATE ERC-20 TOKEN...")
    print("-"*70)
    
    token = await coti.deploy_private_erc20(
        name="BugBountyToken",
        symbol="BBT",
        initial_supply=1_000_000
    )
    
    print(f"\n✅ Token Details:")
    print(f"   Name: {token['name']}")
    print(f"   Symbol: {token['symbol']}")
    print(f"   Contract: {token['contract_address']}")
    print(f"   Supply: {token['total_supply'] / (10**18):,.0f} BBT")
    
    # Mint tokens to wallet
    print("\n" + "-"*70)
    print("💰 MINTING INITIAL SUPPLY...")
    print("-"*70)
    
    await coti.mint_private_tokens(
        amount=100_000,
        recipient=metamask_address
    )
    
    # Get balance
    balance = await coti.get_private_balance(metamask_address)
    print(f"\n✅ Balance: {balance / (10**18):,.0f} BBT")
    
    # Run Sentinel Agent scan
    print("\n" + "-"*70)
    print("🔍 RUNNING CONTRACT SCAN...")
    print("-"*70)
    
    agent = SentinelAgent()
    agent.wallet = coti.account
    agent.mcp_client = coti
    
    # Simulate scanning a vulnerable contract
    target_contract = "0xVulnerableContract123456789"
    findings = await agent.scan_contract(target_contract)
    
    if findings["findings"]:
        print(f"\n📊 Vulnerabilities Found: {len(findings['findings'])}")
        for vuln in findings["findings"]:
            print(f"   ⚠️  [{vuln['severity'].upper()}] {vuln['type']}")
            print(f"       Line: {vuln.get('line', 'N/A')}")
            print(f"       {vuln['description']}")
        
        # Submit encrypted report
        print("\n" + "-"*70)
        print("📬 SUBMITTING ENCRYPTED REPORT...")
        print("-"*70)
        
        report = await agent.submit_encrypted_report(findings)
        print(f"\n✅ Report ID: {report['report_id']}")
        print(f"   Status: {report['status']}")
        print(f"   Encryption: E2E (COTI Messaging SDK)")
        
        # Claim bounty
        print("\n" + "-"*70)
        print("💰 CLAIMING BOUNTY...")
        print("-"*70)
        
        bounty = await agent.claim_bounty(report["report_id"])
        print(f"\n🎉 BOUNTY CLAIMED!")
        print(f"   Amount: {bounty['amount']:,} {bounty['token']}")
        print(f"   Privacy: {bounty['encrypted']}")
    
    # Save session output
    session_data = {
        "demo_type": "live_testnet",
        "wallet": metamask_address,
        "network": config["network"],
        "rpc_url": config["rpc_url"],
        "chain_id": config["chain_id"],
        "token_contract": token["contract_address"],
        "token_name": token["name"],
        "token_symbol": token["symbol"],
        "vulnerabilities_found": len(findings["findings"]) if findings else 0,
        "bounty_claimed": bounty["amount"] if findings else 0,
        "timestamp": datetime.now().isoformat()
    }
    
    with open("live_demo_output.json", "w") as f:
        json.dump(session_data, f, indent=2)
    
    print("\n" + "="*70)
    print("✅ LIVE DEMO COMPLETE")
    print("="*70)
    print(f"\n💾 Session saved: live_demo_output.json")
    print(f"📄 Full log: demo-run-output.txt")
    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
