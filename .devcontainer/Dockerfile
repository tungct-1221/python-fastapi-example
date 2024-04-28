FROM mcr.microsoft.com/devcontainers/python:dev-3.10-bullseye

#RUN apt-get update && apt-get install -y \
#    pipx \
#    && apt-get clean

#RUN pipx ensurepath --global && \
#    pipx install poetry

# Add a new user 'worker' with no password, add it to 'sudo' group
# RUN useradd -m worker && echo "worker:worker" | chpasswd && adduser worker sudo

# # Allow 'worker' to run sudo commands without password prompt
# RUN echo 'worker ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# # # Switch to 'worker' user
# # USER worker

# # COPY ~/.ssh/known_hosts /home/worker/.ssh/known_hosts
# WORKDIR /workspace
# RUN chown -R worker:worker /workspace

RUN pip install --upgrade pip && \
    pip install pipx && \
    pipx ensurepath && \
    pipx install poetry
