
import logging

if __name__ == '__main__':

    log = logging.getLogger('example')
    log.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)

    log.addHandler(ch)

    log.debug("debug message")
    log.info("info message")
    log.warn("warn message")
    log.error("error message")
    log.critical("critical message")

