#!/usr/bin/env python3
"""
COTI MCP Client — Python wrapper for COTI MCP Server
Enables Python agents to call COTI blockchain tools via MCP protocol
"""
import asyncio
import json
import subprocess
from typing import Any, Dict, Optional, List

class CotiMCPClient:
    """Python client for COTI MCP Server"""
    
    def __init__(self, server_path: str = "coti-mcp/index.ts", debug: bool = False):
        self.server_path = server_path
        self.debug = debug
        self.process: Optional[asyncio.subprocess.Process] = None
        self.request_id = 0
        
    async def start_server(self):
        """Start MCP server as subprocess"""
        print(f"🔌 Starting COTI MCP Server...")
        
        # Start server directly with tsx (TypeScript executor)
        self.process = await asyncio.create_subprocess_exec(
            "npx", "tsx", "index.ts",
            cwd="coti-mcp",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Wait for server to initialize
        await asyncio.sleep(2)
        
        print("✅ MCP Server started")
    
    async def call_tool(self, tool_name: str, params: Dict[str, Any] = None) -> Any:
        """Call MCP tool with parameters"""
        if not self.process:
            await self.start_server()
        
        self.request_id += 1
        
        # Build JSON-RPC request
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": params or {}
            }
        }
        
        # Send request
        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json.encode())
        await self.process.stdin.drain()
        
        # Read response
        response_line = await self.process.stdout.readline()
        response = json.loads(response_line.decode())
        
        if "error" in response:
            raise Exception(f"MCP Error: {response['error']}")
        
        return response.get("result")
    
    async def create_account(self) -> Dict[str, str]:
        """Create new COTI account"""
        result = await self.call_tool("create_account", {})
        return result
    
    async def generate_aes_key(self) -> str:
        """Generate AES encryption key"""
        result = await self.call_tool("generate_aes_key", {})
        return result.get("aes_key")
    
    async def deploy_private_erc20(
        self, 
        name: str, 
        symbol: str, 
        initial_supply: int
    ) -> Dict[str, Any]:
        """Deploy Private ERC-20 contract"""
        params = {
            "name": name,
            "symbol": symbol,
            "initial_supply": str(initial_supply)
        }
        result = await self.call_tool("deploy_private_erc20_contract", params)
        return {
            "contract_address": result.get("address"),
            "name": name,
            "symbol": symbol,
            "total_supply": initial_supply
        }
    
    async def mint_private_tokens(
        self, 
        contract_address: str, 
        amount: int, 
        recipient: str
    ) -> str:
        """Mint private tokens"""
        params = {
            "contract_address": contract_address,
            "amount": str(amount),
            "recipient": recipient
        }
        result = await self.call_tool("mint_private_erc20_token", params)
        return result.get("transaction_hash")
    
    async def get_private_balance(
        self, 
        contract_address: str, 
        address: str
    ) -> int:
        """Get private token balance"""
        params = {
            "contract_address": contract_address,
            "address": address
        }
        result = await self.call_tool("get_private_erc20_balance", params)
        return int(result.get("balance", 0))
    
    async def transfer_private_tokens(
        self,
        contract_address: str,
        to: str,
        amount: int,
        memo: Optional[str] = None
    ) -> str:
        """Transfer private tokens"""
        params = {
            "contract_address": contract_address,
            "to": to,
            "amount": str(amount),
            "memo": memo or ""
        }
        result = await self.call_tool("transfer_private_erc20", params)
        return result.get("transaction_hash")
    
    async def send_encrypted_message(
        self,
        recipient: str,
        content: str,
        epoch_id: Optional[int] = None
    ) -> str:
        """Send encrypted message via COTI messaging"""
        # Note: This requires coti-agent-messaging MCP server
        params = {
            "recipient": recipient,
            "content": content,
            "epoch_id": epoch_id or 0
        }
        result = await self.call_tool("send_encrypted_message", params)
        return result.get("message_id")
    
    async def get_native_balance(self, address: str) -> int:
        """Get native COTI balance"""
        params = {"address": address}
        result = await self.call_tool("get_native_balance", params)
        return int(result.get("balance", 0))
    
    async def close(self):
        """Stop MCP server"""
        if self.process:
            self.process.terminate()
            await self.process.wait()
            print("🔌 MCP Server stopped")


# Test function
async def test_mcp_client():
    """Test MCP client with actual server"""
    print("\n🧪 Testing COTI MCP Client\n")
    
    client = CotiMCPClient()
    
    try:
        # Create account
        print("[1/5] Creating account...")
        account = await client.create_account()
        print(f"  ✅ Account: {account.get('address', 'N/A')}")
        
        # Generate AES key
        print("\n[2/5] Generating AES key...")
        aes_key = await client.generate_aes_key()
        print(f"  ✅ AES Key: {aes_key[:20]}...")
        
        # Deploy token
        print("\n[3/5] Deploying Private ERC-20...")
        token = await client.deploy_private_erc20(
            name="BugBountyToken",
            symbol="BBT",
            initial_supply=1_000_000
        )
        print(f"  ✅ Token: {token['contract_address']}")
        
        # Mint tokens
        print("\n[4/5] Minting tokens...")
        tx_hash = await client.mint_private_tokens(
            contract_address=token["contract_address"],
            amount=100_000,
            recipient=account["address"]
        )
        print(f"  ✅ Minted: {tx_hash}")
        
        # Check balance
        print("\n[5/5] Checking balance...")
        balance = await client.get_private_balance(
            contract_address=token["contract_address"],
            address=account["address"]
        )
        print(f"  ✅ Balance: {balance / (10**18):,.0f} BBT")
        
        print("\n✅ All tests passed!\n")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}\n")
        print("Note: Make sure COTI MCP server is built and configured correctly")
        
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(test_mcp_client())
