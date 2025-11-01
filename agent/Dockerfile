FROM debian:12-slim

ARG LLM_API_URL
ARG LLM_API_KEY
ARG MODEL
ARG PORT
ARG SEED
ARG NAME
ARG MAILBOX
ARG RATE_LIMIT_CALLS
ARG RATE_LIMIT_PERIOD
ARG HOME_PATH
ARG GEM_PATH
ARG GEM_HOME
ARG RUBY_PATH
ARG NODE_PATH

ENV LLM_API_URL=${LLM_API_URL}
ENV LLM_API_KEY=${LLM_API_KEY}
ENV MODEL=${MODEL}
ENV PORT=${PORT}
ENV SEED=${SEED}
ENV NAME=${NAME}
ENV MAILBOX=${MAILBOX}
ENV RATE_LIMIT_CALLS=${RATE_LIMIT_CALLS}
ENV RATE_LIMIT_PERIOD=${RATE_LIMIT_PERIOD}
ENV HOME_PATH=${HOME_PATH}
ENV GEM_PATH=${GEM_PATH}
ENV GEM_HOME=${GEM_HOME}
ENV RUBY_PATH=${RUBY_PATH}
ENV NODE_PATH=${NODE_PATH}

# Common tools and build deps
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    wget \
    git \
    gnupg \
    lsb-release \
    build-essential \
    ca-certificates \
    unzip \
    zip \
    procps \
    pkg-config \
    python3 \
    python3-pip \
    locales \
    sudo \
    libssl-dev \
    zlib1g-dev \
    libreadline-dev \
    libyaml-dev \
    libsqlite3-dev \
    sqlite3 \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    libgmp-dev \
    default-mysql-client \
 && rm -rf /var/lib/apt/lists/*

# Enable locale
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen

WORKDIR /app

COPY . /app

# --------------------
# Django 
# --------------------
RUN python3 --version
RUN pip install Django --break-system-packages

# --------------------
# Node.js + npm + yarn + pnpm
# --------------------
ARG NODE_VERSION=20
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
RUN \. "/root/.nvm/nvm.sh"
RUN echo $HOME
SHELL ["bash", "-lc"]
RUN nvm install 24
RUN corepack enable pnpm
RUN corepack enable yarn

# --------------------
# PHP & Composer & common PHP extensions
# --------------------
# Use Debian php packages for wide compatibility
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    php-cli php-zip php-xml php-mbstring php-curl php-intl php-json php-gd php-pgsql php-sqlite3 php-mysql \
 && rm -rf /var/lib/apt/lists/*

# Install Composer
RUN php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
RUN php -r "if (hash_file('sha384', 'composer-setup.php') === 'c8b085408188070d5f52bcfe4ecfbee5f727afa458b2573b8eaaf77b3419b0bf2768dc67c86944da1544f06fa544fd47') { echo 'Installer verified'.PHP_EOL; } else { echo 'Installer corrupt'.PHP_EOL; unlink('composer-setup.php'); exit(1); }"
RUN php composer-setup.php
RUN php -r "unlink('composer-setup.php');"
RUN mv composer.phar /usr/local/bin/composer
RUN composer --version

# --------------------
# Ruby, rails
# --------------------
RUN sudo apt update
RUN sudo apt install -y build-essential rustc libssl-dev libyaml-dev zlib1g-dev libgmp-dev git
RUN curl https://mise.run | sh
RUN echo 'eval "$(~/.local/bin/mise activate)"' >> ~/.bashrc
RUN source ~/.bashrc
RUN mise use -g ruby@3
RUN gem install rails



# --------------------
# Clean up apt caches to reduce image size
# --------------------
RUN apt-get clean || true && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


EXPOSE 5000

CMD ["python", "-m", "src.forge"]
