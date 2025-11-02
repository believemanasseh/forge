FROM debian:12-slim AS builder

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

# --------------------
# Django 
# --------------------
RUN pip install Django --break-system-packages

# --------------------
# Node.js + npm + yarn + pnpm
# --------------------
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash && \
    export NVM_DIR="$HOME/.nvm" && \
    \. "$NVM_DIR/nvm.sh" && \
    nvm install 24 && \
    nvm use 24 && \
    corepack enable pnpm && corepack prepare pnpm@latest --activate && \
    corepack enable yarn && corepack prepare yarn@latest --activate 

# --------------------
# PHP & Composer & common PHP extensions
# --------------------
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    php-cli php-zip php-xml php-mbstring php-curl php-intl php-json php-gd php-pgsql php-sqlite3 php-mysql \
 && rm -rf /var/lib/apt/lists/*
# Install Composer
RUN php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" && \
    php -r "if (hash_file('sha384', 'composer-setup.php') === 'c8b085408188070d5f52bcfe4ecfbee5f727afa458b2573b8eaaf77b3419b0bf2768dc67c86944da1544f06fa544fd47') { echo 'Installer verified'.PHP_EOL; } else { echo 'Installer corrupt'.PHP_EOL; unlink('composer-setup.php'); exit(1); }" && \
    php composer-setup.php && \
    php -r "unlink('composer-setup.php');" && \
    mv composer.phar /usr/local/bin/composer

# --------------------
# Ruby, rails
# --------------------
# Install dependencies
RUN apt update && \
    apt install -y curl git build-essential rustc libssl-dev libyaml-dev zlib1g-dev libgmp-dev
# Install mise and Ruby + Rails
RUN curl https://mise.run | sh
RUN echo 'eval "$(~/.local/bin/mise activate bash)"' >> ~/.bashrc
SHELL ["/bin/bash", "-lc"]
RUN mise use -g ruby@3 
RUN gem install rails
ENV GEM_HOME="/root/.local/share/mise/installs/ruby/3.4.7/lib/ruby/gems/3.4.0"
ENV PATH="$GEM_HOME/bin:/root/.local/share/mise/installs/ruby/3.4.7/bin:/root/.local/share/mise/shims:$PATH"

FROM debian:12-slim AS runtime

# Install ONLY runtime dependencies (no build-essential, no rustc, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl wget git procps \
    python3 python3-pip locales python3.11-venv \
    # Ruby runtime dependencies
    libssl3 zlib1g libreadline8 libyaml-0-2 \
    libsqlite3-0 sqlite3 libxml2 libxslt1.1 \
    libffi8 libgmp10 \
    # PHP runtime
    php-cli php-zip php-xml php-mbstring php-curl \
    php-intl php-json php-gd php-pgsql php-sqlite3 php-mysql \
    # MySQL client
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Enable locale
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen

# --------------------
# Copy Python packages
# --------------------
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11

# --------------------
# Copy Node.js
# --------------------
COPY --from=builder /root/.nvm /root/.nvm
ENV NVM_DIR=/root/.nvm
ENV NODE_VERSION=24
ENV PATH="${NVM_DIR}/versions/node/v${NODE_VERSION}.11.0/bin:${PATH}"

# --------------------
# Copy Composer
# --------------------
COPY --from=builder /usr/local/bin/composer /usr/local/bin/composer

# --------------------
# Copy Ruby & Rails (via mise)
# --------------------
COPY --from=builder /root/.local/share/mise /root/.local/share/mise
COPY --from=builder /root/.local/bin/mise /root/.local/bin/mise
COPY --from=builder /root/.config/mise /root/.config/mise

ENV MISE_RUBY_VERSION=3.4.7
ENV PATH="/root/.local/share/mise/installs/ruby/${MISE_RUBY_VERSION}/bin:/root/.local/share/mise/shims:/root/.local/bin:${PATH}"

# Add mise activation to bashrc
RUN echo 'eval "$(~/.local/bin/mise activate bash)"' >> ~/.bashrc

# Verify installations
RUN python3 --version && \
    node -v && npm -v && yarn -v && pnpm -v && \
    php -v && composer --version && \
    ruby -v && rails -v

# --------------------
# Application setup
# --------------------
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt --break-system-packages && \
    mkdir -p ~/.aws && \
    mv ./credentials ~/.aws 2>/dev/null || true

EXPOSE 5000

CMD ["/bin/bash", "-lc", "python3 -m src.forge"]

