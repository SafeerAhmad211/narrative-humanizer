# syntax=docker/dockerfile:1

# --- builder: install the package + deps into an isolated venv -------------
FROM python:3.13-slim-bookworm AS builder

WORKDIR /build

# Copy only what's needed to resolve/install dependencies and the package
# itself, so Docker's layer cache survives edits to files outside cli/.
COPY pyproject.toml README.md ./
COPY narrative_humanizer ./narrative_humanizer

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

# --- runtime: minimal image, no build toolchain, non-root user -------------
FROM python:3.13-slim-bookworm AS runtime

RUN groupadd --system app && useradd --system --gid app --create-home app
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

USER app
WORKDIR /home/app

# ANTHROPIC_API_KEY must be supplied at `docker run` time (-e ANTHROPIC_API_KEY=...);
# it is intentionally not baked into the image. `check` needs it, `list-checklist` doesn't.
ENTRYPOINT ["narrative-humanizer"]
CMD ["list-checklist"]
