import time
import xmlrpc.client
from loguru import logger
from natpmp import NATPMP
from app.core.config import settings, Config


logger.remove()
logger.add(f"{settings.log_dir}/rtorrent-natpmp.log", level=settings.log_level, rotation="12:00", retention="1 week")


@logger.catch(reraise=True)
def _request_tcp_port_forward(cfg: Config) -> int:
    response = NATPMP.map_tcp_port(public_port=0, private_port=0, lifetime=60, gateway_ip=cfg.gateway_ip)
    logger.debug(f"received NAT-PMP mapping: {response}")
    return response.public_port


@logger.catch(reraise=True)
def _update_rtorrent_port(tcp_port: int):
    proxy = xmlrpc.client.ServerProxy(settings.rtorrent_xmlrpc_url)
    logger.info(f"re-configuring on the fly rtorrent. remote tcp: {tcp_port}")
    proxy.network.port_range.set("", f"{tcp_port}-{tcp_port}")
    if settings.allow_dht:
        # Some gateway will open udp port at same time using same number.
        # This allow us to use DHT if really want it especially for public trackers.
        logger.info(f"re-configuring on the fly rtorrent. dht: auto. remote udp: {tcp_port}")
        proxy.dht.mode.set("on")
        proxy.dht.port.set(f"{tcp_port}")
    # This is required to ask rtorrent to honor new tcp/udp ports binding.
    proxy.network.bind_address.set("", settings.bind_address)


def main():
    current_tcp_port = None
    while True:
        try:
            logger.debug("requesting tcp port forwarding using nat-pmp...")
            tcp_port = _request_tcp_port_forward(settings)
            logger.debug(f"nat-pmp request processed. TCP: {tcp_port}...")
            if tcp_port != current_tcp_port:
                logger.debug("updating rtorrent settings...")
                _update_rtorrent_port(tcp_port)
                current_tcp_port = tcp_port
                logger.debug("rtorrent settings updated.")
        except:  # pylint: disable=bare-except
            logger.error("Failed to refresh NAT-PMP.")
        finally:
            time.sleep(settings.refresh_interval)


if __name__ == "__main__":
    main()
