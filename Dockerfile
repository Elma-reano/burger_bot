
FROM ghcr.io/astral-sh/uv:python:3.12-bookworm-slim

# create nonroot user
RUN groupadd --system --gid 999 nonroot && \
    useradd --system --gid 999 --uid 999 --create-home nonroot

# Work directory
WORKDIR /app

# Enable bytecode compilation, set link mode to copy, and set tool binary directory
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_TOOL_BIN_DIR=/usr/local/bin

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

# Use the non-root user to run our application
USER nonroot

# Command to run the application
CMD ["python", "main.py"]
