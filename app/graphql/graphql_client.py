from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from app.common.constants import api_gateway_url

class GraphQLClient:
    def __init__(self, headers=None):
        self.url = api_gateway_url
        self.headers = headers
        self.transport = AIOHTTPTransport(
            url=self.url,
            headers=self.headers
        )
        self.client = Client(
            transport=self.transport,
            fetch_schema_from_transport=True,
        )

    async def execute(self, query, variable_values=None):
        async with self.client as session:
            return await session.execute(
                gql(query),
                variable_values=variable_values
            )