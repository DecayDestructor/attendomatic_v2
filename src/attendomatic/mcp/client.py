import asyncio
import os
import sys

from fastmcp import Client
from fastmcp.client.transports import StdioTransport


async def main():
    transport = StdioTransport(
        command=sys.executable,
        args=["-m", "attendomatic.mcp.server"],
        cwd=os.getcwd(),
        env=dict(os.environ),
    )

    async with Client(transport) as client:
        tools = await client.list_tools()
        print("Available tools:")
        for tool in tools:
            print(f"- {tool.name}")

        result = await client.call_tool("get_all_subjects")
        print("\nget_all_subjects result:")
        print(result)

        # Admin-only examples:
        result = await client.call_tool(
            "create_subject",
            {
                "name": "Decision Making and Business Intelligence",
                "code": "DMBI",
                "user_email": "aaryanmantri29@gmail.com",
            },
        )
        print("\ncreate_subject result:")
        print(result)
        # await client.call_tool(
        #     "update_subject",
        #     {
        #         "subject_id": 1,
        #         "name": "Advanced Physics",
        #         "user_email": "admin@example.com",
        #     },
        # )
        # await client.call_tool(
        #     "delete_subject",
        #     {"subject_id": 1, "user_email": "admin@example.com"},
        # )


if __name__ == "__main__":
    asyncio.run(main())
