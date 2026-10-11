FROM ros:humble

RUN apt update && apt install -y --no-install-recommends \
    ros-humble-turtlesim \
    ros-humble-rqt ros-humble-rqt-common-plugins \
    qt6-wayland \
    bash-completion \
    && rm -rf /var/lib/apt/lists/*

# Add uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Env not tied to project (part of the container)
ENV UV_PROJECT_ENVIRONMENT=/opt/venv

USER root
WORKDIR /pampas

# venv can see system ROS packages (rclpy)
RUN uv venv --system-site-packages /opt/venv

# dependency layer: only rebuilds when these files change
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-install-project

RUN echo 'source /opt/ros/humble/setup.bash' >> /root/.bashrc \
    && echo "alias ls='ls --color=auto'; alias grep='grep --color=auto'" >> /root/.bashrc \
    && echo 'PS1="\[\e[32m\]\u@\h\[\e[0m\]:\[\e[34m\]\w\[\e[0m\]\$ "' >> /root/.bashrc

CMD ["bash"]
