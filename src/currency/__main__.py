

import uvicorn

import currency
from currency.config import Config
from currency.service import get_app
from currency.util.log import log


def main() -> None:
    config = Config()
    config.verify()

    log.info(
        f"Starting service {currency.__version__ or '???'} on port {config.PORT}",
    )
    app = get_app()
    if config.DEBUG == 'enabled':
        uvicorn.run(
            'currency.service:get_app',
            host="0.0.0.0",
            port=config.PORT,
            workers=1,
            reload=True
        )
    else:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=config.PORT,
            workers=1,
        )


if __name__ == "__main__":
    main()
