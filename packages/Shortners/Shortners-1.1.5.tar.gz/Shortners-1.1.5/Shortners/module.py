import aiohttp

class Shortner:
    def __init__(self, api, site):
        self.apis = api
        self.site = site
        self.seon = aiohttp.ClientSession

#========================================================================

    async def shortlink(self, recived):
        async with self.seon() as seion:
            param = {'api': self.apis, 'url': recived}
            async with seion.get(self.site, params=param) as res:
                if res.status == "success" or res.status == 200:
                    dataes = await res.json()
                    reurns = dataes["shortenedUrl"]
                    ruerns = reurns if reurns else None
                    return ruerns
                else:
                    return None

#========================================================================

    async def clinton(self, recived):
        try: outgoing = await self.shortlink(recived)
        except Exception: outgoing = recived
        return outgoing

#========================================================================
