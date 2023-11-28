# Working on Rust project cheat sheet

## Faster linking

### Linux

- Install linker

        sudo apt-get install lld clang

- Create a `.cargo/config.toml` file with 

        [target.x86_64-unknown-linux-gnu]
        rustflags = ["-C", "linker=clang", "-C", "link-arg=-fuse-ld=lld"]

### MacOS

- Install linker

        brew install llvm

    > follow steps in: `brew info llvm`

- Create a `.cargo/config.toml` file with 

        [target.x86_64-apple-darwin]
        rustflags = ["-C", "link-arg=-fuse-ld=lld"]
        [target.aarch64-apple-darwin]
        rustflags = ["-C", "link-arg=-fuse-ld=/opt/homebrew/opt/llvm/bin/ld64.ll

## Continuous check

To avoid running the cargo check / cargo run.

    cargo install cargo-watch

To monitor source code to trigger commands every time a file changes

    cargo watch -x check

We can chain as well (ex. run tests if check succeeds)

    cargo watch -x check -x

## Continuous integration

### Running tests

    cargo test

> Note it builds the project beforehand

### Code coverage

Install

    cargo install cargo-tarpaulin

Run

    cargo tarpaulin --ignore-tests
