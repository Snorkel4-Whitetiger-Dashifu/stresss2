FROM public.ecr.aws/docker/library/python:3.13-slim-bookworm@sha256:01f42367a0a94ad4bc17111776fd66e3500c1d87c15bbd6055b7371d39c124fb

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        tmux \
        asciinema \
        cron \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.lock /tmp/requirements.lock
RUN python3 -m pip install --no-cache-dir --no-deps \
        -r /tmp/requirements.lock

WORKDIR /app

COPY app/ /app/
RUN cp /app/workflow/compile_outages.py /app/workflow/.compile_outages.original \
    && chmod a-w /app/workflow/.compile_outages.original

# Operational wiring left behind by the failed pager-policy rollout:
# a non-executable wrapper pointing at a path that no longer exists, a stale
# compile lock, no schedule entry, and a world-writable output directory.
RUN printf '#!/bin/sh\nexec python3 /app/workflow/compile_outages.py.legacy "$@"\n' > /usr/local/bin/compile-outages \
    && chmod 0644 /usr/local/bin/compile-outages \
    && mkdir -p /var/lock \
    && printf '4711\n' > /var/lock/outage-compile.lock \
    && rm -f /etc/cron.d/outage-compile \
    && mkdir -p /app/output \
    && chmod 0777 /app/output
