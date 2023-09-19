FROM rust AS planner
RUN mkdir /app
WORKDIR /app
RUN cargo install cargo-chef
COPY . .
RUN cargo chef prepare --recipe-path recipe.json

FROM rust as cacher
RUN mkdir /app
WORKDIR /app
RUN cargo install cargo-chef
COPY --from=planner /app/recipe.json recipe.json
RUN cargo chef cook --release --recipe-path recipe.json

FROM rust as builder
WORKDIR app
RUN apt-get update && \
        apt-get install -y libpam-dev libseccomp-dev && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
COPY . .
COPY --from=cacher /app/target target
COPY --from=cacher /usr/local/cargo /usr/local/cargo
RUN cargo build --release

FROM ubuntu:20.04
RUN apt-get update && \
    apt-get install -y openssh-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN mkdir /var/run/sshd
RUN useradd -M -d / -s /bin/bash user
COPY ./config/sshd_config /etc/ssh/sshd_config
COPY ./config/sshd /etc/pam.d/sshd
COPY --from=builder /app/target/release/libpam_code_auth.so /usr/lib/x86_64-linux-gnu/security/pam_code_auth.so
RUN echo HV{49daa679d462924b210dc841439a4806} > /flag.txt && chmod 0444 /flag.txt
EXPOSE 22
ENTRYPOINT ["/usr/sbin/sshd", "-D", "-e"]
