"""
This module is an entrypoint to AgentQL service
"""

import logging
from typing import Any

from agentql.async_api.web import InteractiveItemTypeT, PageTypeT, PlaywrightWebDriver, WebDriver

from .session import Session

log = logging.getLogger(__name__)


async def start_async_session(
    url: str = "",
    *,
    web_driver: WebDriver[InteractiveItemTypeT, PageTypeT] = PlaywrightWebDriver(),
    user_auth_session: Any = None,
) -> Session[InteractiveItemTypeT, PageTypeT]:
    """Start a new asynchronous AgentQL session with the given URL, web driver and user authentication session. By default, session will use Playwright Web Driver.

    Parameters:
    ----------
    url (str): URL to navigate session to. To navigate after a session has already started, users could start session with an initialized web driver and invoke `driver.open_url()` method.
    web_driver (webDriver) (optional): Web driver is responsible for interacting with the browser and page. Defaults to Playwright web driver, which is built on top of the [Playwright framework](https://playwright.dev/python/).
    user_auth_session (dict) (optional): The user authentication session that contains previous login session. Users could retrieve authentication session by starting a session, logging into desired website, and calling `session.get_user_auth_session()`, which will return a `auth_session` object defined in web driver.

    Returns:
    -------
    Session: An instance of AgentQL Session class for asynchronous environment.
    """
    log.debug(f"Starting asynchronous session with {url}")

    await web_driver.start_browser(user_auth_session=user_auth_session)
    if url:
        await web_driver.open_url(url)
    session = Session[InteractiveItemTypeT, PageTypeT](web_driver)
    return session
