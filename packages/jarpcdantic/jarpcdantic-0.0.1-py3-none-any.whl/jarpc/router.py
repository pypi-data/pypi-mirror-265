from jarpc import JarpcResponse, JarpcClient, AsyncJarpcClient


class JarpcClientRouter:
    def __init__(
        self,
        prefix: str | None = None,
        client: AsyncJarpcClient | JarpcClient | None = None,
    ):
        self._client: AsyncJarpcClient | JarpcClient | None = client
        self._prefix: str | None = prefix

    def __getattribute__(self, item):
        attr = object.__getattribute__(self, item)

        # if is router module
        # then add parent prefix
        if isinstance(attr, JarpcClientRouter):
            if attr._prefix is None:
                attr._prefix = item

            if self._prefix is None:
                self._prefix = ""

            if not attr._prefix.startswith(self._prefix):
                attr._prefix = (
                    self._prefix
                    + ("." if self._prefix and attr._prefix else "")
                    + attr._prefix
                )

            # provide arpcClient to child
            if attr._client is None and self._client is not None:
                attr._client = self._client

        # if is rpc method
        if (
            hasattr(attr, "__annotations__")
            and "return" in attr.__annotations__
            and attr.__annotations__["return"] is not None
            and issubclass(attr.__annotations__["return"], JarpcResponse)
        ):
            method = self._prefix + ("." if self._prefix else "") + item

            async def wrapped(data, **kwargs):
                print(f"call method {method} with {kwargs}")
                await self._client(method=method, params=data, **kwargs)

            wrapped.__annotations__ = attr.__annotations__

            return wrapped

        return attr


if __name__ == "__main__":
    import asyncio

    class PassportRouter(JarpcClientRouter):
        async def register(self, data: str, **kwargs) -> JarpcResponse[None]:
            ...

        async def get_status(self, **kwargs) -> JarpcResponse[None]:
            ...

        async def invalidate(self, data: str, **kwargs) -> JarpcResponse[None]:
            ...


    class MvdRouter(JarpcClientRouter):
        passport = PassportRouter(prefix="hello")
        test = PassportRouter(prefix="hell")

        async def get_status(self) -> JarpcResponse[None]:
            ...


    async def main():
        router = MvdRouter(prefix="mvd")
        await router.get_status()
        await router.passport.register("22")
        await router.passport.invalidate("22")
        await router.test.invalidate("22")


    asyncio.run(main())
